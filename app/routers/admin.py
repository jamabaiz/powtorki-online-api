from fastapi import APIRouter, UploadFile, Form, Depends
from fastapi_permissions import Allow, All
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from app.auth.permissions import Permission
from app.constants import PageSubTypes
from app.database import models
from app.database.database import get_db
from app.routers import Admin
from app.tools.importing import process_documents, process_pdf, process_qa, process_dates, process_characters, \
    process_dictionary, process_quiz

router = APIRouter()

page_type_to_model = {
    PageSubTypes.VideoScriptPage: models.DocumentPage,
    PageSubTypes.MindmapPage: models.DocumentPage,
    PageSubTypes.Lesson: models.DocumentPage,
    PageSubTypes.DocumentPage: models.DocumentPage,
    PageSubTypes.Character: models.CharacterPage,
    PageSubTypes.Date: models.CalendarPage,
    PageSubTypes.Dictionary: models.DictionaryPage,
    PageSubTypes.QA: models.QAPage,
    PageSubTypes.Quiz: models.QuizPage
}


@router.post("/import_from_file/", dependencies=[Permission("view", [(Allow, Admin, All)])])
def import_from_file(files: list[UploadFile], taxonomy: int = Form(), page_type: int = Form(),
                     db: Session = Depends(get_db)):
    new_pages = []

    page_type_enum = page_type

    tax = db.query(models.ChapterTaxonomy).filter(models.ChapterTaxonomy.id == taxonomy).first()

    if page_type_enum in [PageSubTypes.DocumentPage, PageSubTypes.Lesson]:
        new_pages += process_documents(page_type_enum, files)
    elif page_type_enum in [PageSubTypes.MindmapPage]:
        new_pages += process_pdf(page_type_to_model[page_type_enum], files)
    elif page_type_enum in [PageSubTypes.QA]:
        for file in files:
            qa_tax = models.Taxonomy(name=file.filename, id_parent=tax.id)
            db.add(qa_tax)
            for quiz_page in process_qa(file):
                map_page_tax = models.MapPageTaxonomy()
                map_page_tax.taxonomy = qa_tax
                quiz_page.taxonomies.append(map_page_tax)
                db.add(map_page_tax)
                db.add(quiz_page)
    elif page_type_enum in [PageSubTypes.Date]:
        for file in files:
            new_pages += process_dates(file, db)
    elif page_type_enum in [PageSubTypes.Character]:
        for file in files:
            new_pages += process_characters(file)
    elif page_type_enum in [PageSubTypes.Dictionary]:
        for file in files:
            new_pages += process_dictionary(file)
    elif page_type_enum in [PageSubTypes.Quiz]:
        for file in files:
            process_quiz(file, db, tax)
    else:
        raise Exception(f"Unhandled typeId: {page_type}")

    for page in new_pages:
        map_page_tax = models.MapPageTaxonomy()
        map_page_tax.taxonomy = tax
        page.taxonomies.append(map_page_tax)
        db.add(page)
        db.add(map_page_tax)

    print(f"Flushing")
    db.flush()
    db.commit()

    return {"filenames": (file.filename for file in files), "taxonomy": taxonomy, "page_type": page_type}


@router.get("/admin/", dependencies=[Permission("view", [(Allow, Admin, All)])])
async def main():
    content = """
<!DOCTYPE html>
<html>
<body>
<form action="/import_from_file/" enctype="multipart/form-data" method="post">
<label>Files: <input name="files" type="file" multiple></label><br>
<label>Type: <select name="page_type" required>
  <option value="1">Lekcja Video</option>
  <option value="4">Mapa Mysli</option>
  <option value="5">Skrypt Lekcji</option>
  <option value="6">Materiały do nauki</option>
  <option value="7">Postacie</option>
  <option value="8">Kalendarz</option>
  <option value="9">Pojęcia</option>
  <option value="10">Pytania i odpowiedzi</option>
  <option value="11">Quiz</option>
</select></label><br>
<label>Taxonomy: <select name="taxonomy" required>
  <option value="713">I Podstawy prawa </option>
  <option value="714">II Obywatel w sądzie</option>
  <option value="715">III Unia Europejska</option>
</select></label></br>
<input type="submit">
</form>
</body>
</html>
    """
    return HTMLResponse(content=content)
