import json
import logging
from pprint import pprint
from typing import TypeVar, Any

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ChapterTaxonomy, DocumentPage, MapPageTaxonomy, CharacterPage, Date, CalendarTaxonomy, \
    Media, ScriptPage, MindmapPage, QAPage, QuizTaxonomy, QuizPage, Answer, MapPageAnswer, CalendarPage, DictionaryPage, \
    QATaxonomy
from importer.models import Calendar, Character, Dictionary, Document, Image, Lesson, MindMap, Page, Question, Quiz, \
    QuestionAnswer

T = TypeVar('T')


def open_file_read_objects(file_name: str, class_type: T) -> dict[int, T]:
    item_dict = {}

    with open(file_name, encoding='utf-8', mode='r') as file:
        j = json.loads(file.read())
        for entry in j:
            u = class_type(**entry)
            item_dict[int(u.id)] = u
        return item_dict


calendar = open_file_read_objects('./dump/his_calendar.json', Calendar)
characters = open_file_read_objects('./dump/his_characters.json', Character)
dictionary = open_file_read_objects('./dump/his_dictionary.json', Dictionary)
documents = open_file_read_objects('./dump/his_documents.json', Document)
images = open_file_read_objects('./dump/his_images.json', Image)
lessons = open_file_read_objects('./dump/his_lessons.json', Lesson)
mind_maps = open_file_read_objects('./dump/his_mind_maps.json', MindMap)
pages = open_file_read_objects('./dump/his_pages.json', Page)
questions = open_file_read_objects('./dump/his_questions.json', Question)
question_answers = open_file_read_objects('./dump/his_question_answer.json', QuestionAnswer)
quizzes = open_file_read_objects('./dump/his_quiz.json', Quiz)

map_modules_id = {
    1: 4,
    2: 5,
    3: 6,
    4: 8,
    5: 9,
    6: 10,
    7: 11,
    8: 12,
    9: 13,
    10: 15,
    11: 16,
    12: 17,
    13: 18,
    14: 19,
    15: 20,
}

ses: Session = next(get_db())


def get_chapter_by_id(index: int) -> ChapterTaxonomy:
    return ses.query(ChapterTaxonomy).filter(ChapterTaxonomy.id == index).first()


def get_chapters() -> dict[int | Any, ChapterTaxonomy]:
    chapters_dict = {}
    for index, value in map_modules_id.items():
        chapter = get_chapter_by_id(value)
        chapters_dict[index] = chapter
    return chapters_dict


def head_print(var):
    pprint({k: var[k] for k in list(var)[:10]})


stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    handlers=[logging.FileHandler("my_log.log", mode='w'),
                              stream_handler])

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    chapters = get_chapters()

    logger.info("Inserting Documents")
    for index, old_doc in documents.items():
        new_page = DocumentPage()
        new_page.title = old_doc.name
        new_page.description = old_doc.description
        new_page.document = pages[int(old_doc.document)].document

        map_chapter_tax = MapPageTaxonomy()
        map_chapter_tax.taxonomy = chapters[int(old_doc.module)]
        new_page.taxonomies.append(map_chapter_tax)

        new_page.time_creation = old_doc.time_creation
        new_page.time_edited = old_doc.time_edited

        ses.add(new_page)
        ses.add(map_chapter_tax)
    ses.flush()

    logger.info("Inserting Characters")
    for index, old_character in characters.items():
        new_page = CharacterPage()
        new_page.title = old_character.name
        new_page.document = old_character.description

        new_page.note = old_character.note

        map_chapter_tax = MapPageTaxonomy()
        map_chapter_tax.taxonomy = chapters[int(old_character.module)]
        new_page.taxonomies.append(map_chapter_tax)

        new_page.time_creation = old_character.time_creation
        new_page.time_edited = old_character.time_edited

        ses.add(new_page)
        ses.add(map_chapter_tax)
    ses.flush()

    logger.info("Inserting Dates")
    calendar_sets = {}
    for index, old_date in calendar.items():
        new_page = CalendarPage()
        new_page.title = old_date.tittle
        new_page.document = old_date.note

        # new_character.note = date.note

        map_chapter_tax = MapPageTaxonomy()
        map_chapter_tax.taxonomy = chapters[int(old_date.module)]
        new_page.taxonomies.append(map_chapter_tax)

        date = Date()
        date.page = new_page
        date.date_text = old_date.date_text
        date.date_number = old_date.date

        if old_date.calendar_set is not None:
            if old_date.calendar_set not in calendar_sets:
                new_calendar_taxonomy = CalendarTaxonomy()
                new_calendar_taxonomy.name = old_date.calendar_set
                new_calendar_taxonomy.id_parent = chapters[int(old_date.module)].id
                calendar_sets[old_date.calendar_set] = new_calendar_taxonomy
                ses.add(new_calendar_taxonomy)

            map_calendar_tax = MapPageTaxonomy()
            map_calendar_tax.taxonomy = calendar_sets[old_date.calendar_set]
            new_page.taxonomies.append(map_calendar_tax)
            ses.add(map_calendar_tax)

        new_page.time_creation = old_date.time_creation
        new_page.time_edited = old_date.time_edited

        ses.add(date)
        ses.add(new_page)
        ses.add(map_chapter_tax)
    ses.flush()

    logger.info("Inserting Dictionary")
    for index, old_dictionary in dictionary.items():
        new_page = DictionaryPage()
        new_page.title = old_dictionary.name
        new_page.document = old_dictionary.description
        new_page.note = old_dictionary.note

        map_chapter_tax = MapPageTaxonomy()
        map_chapter_tax.taxonomy = chapters[int(old_dictionary.module)]
        new_page.taxonomies.append(map_chapter_tax)

        new_page.time_creation = old_dictionary.time_creation
        new_page.time_edited = old_dictionary.time_edited

        ses.add(new_page)
        ses.add(map_chapter_tax)
    ses.flush()

    logger.info("Inserting Images")
    for index, old_image in images.items():
        new_image = Media()
        new_image.name = old_image.tittle
        new_image.slug = old_image.id_str
        new_image.path = old_image.source
        new_image.licence = old_image.copyright
        new_image.time_creation = old_image.time_creation
        new_image.time_edited = old_image.time_edited
        ses.add(new_image)
    ses.flush()

    logger.info("Inserting Lessons")
    for index, old_lesson in lessons.items():
        new_page = ScriptPage()
        new_page.title = old_lesson.name
        new_page.description = old_lesson.description

        if old_lesson.document is not None:
            new_page.document = pages[int(old_lesson.document)].document

        map_chapter_tax = MapPageTaxonomy()
        map_chapter_tax.taxonomy = chapters[int(old_lesson.module)]
        new_page.taxonomies.append(map_chapter_tax)

        new_page.time_creation = old_lesson.time_creation
        new_page.time_edited = old_lesson.time_edited

        ses.add(new_page)
        ses.add(map_chapter_tax)
    ses.flush()

    logger.info("Inserting MindMaps")
    for index, old_mindmap in mind_maps.items():
        new_page = MindmapPage()
        new_page.title = old_mindmap.name
        new_page.document = pages[int(old_mindmap.document)].document

        map_chapter_tax = MapPageTaxonomy()
        map_chapter_tax.taxonomy = chapters[int(old_mindmap.module)]
        new_page.taxonomies.append(map_chapter_tax)

        new_page.time_creation = old_mindmap.time_creation
        new_page.time_edited = old_mindmap.time_edited

        ses.add(new_page)
        ses.add(map_chapter_tax)
    ses.flush()

    logger.info("Inserting QA")
    qa_set = {}
    for index, old_qa in question_answers.items():
        new_page = QAPage()
        new_page.title = old_qa.question
        new_page.document = old_qa.answer

        map_chapter_tax = MapPageTaxonomy()
        map_chapter_tax.taxonomy = chapters[int(old_qa.module)]
        new_page.taxonomies.append(map_chapter_tax)

        if old_qa.question_set is not None:
            if old_qa.question_set not in qa_set:
                new_calendar_taxonomy = QATaxonomy()
                new_calendar_taxonomy.name = old_qa.question_set
                new_calendar_taxonomy.id_parent = chapters[int(old_qa.module)].id
                qa_set[old_qa.question_set] = new_calendar_taxonomy
                ses.add(new_calendar_taxonomy)

            map_qa_tax = MapPageTaxonomy()
            map_qa_tax.taxonomy = qa_set[old_qa.question_set]
            new_page.taxonomies.append(map_qa_tax)
            ses.add(map_qa_tax)

        new_page.time_creation = old_qa.time_creation
        new_page.time_edited = old_qa.time_edited

        ses.add(new_page)
        ses.add(map_chapter_tax)
    ses.flush()

    logger.info("Inserting Quiz Sets")
    quiz_sets = {}
    for index, old_quiz_set in quizzes.items():
        tax = QuizTaxonomy()
        tax.name = old_quiz_set.name
        tax.description = old_quiz_set.description
        tax.time_creation = old_quiz_set.time_creation
        tax.time_edited = old_quiz_set.time_edited
        tax.id_parent = chapters[int(old_quiz_set.module)].id

        quiz_sets[int(old_quiz_set.id)] = tax
        ses.add(tax)
    ses.flush()

    logger.info("Inserting Quizzes")
    for index, old_quiz in questions.items():
        quiz = QuizPage()
        quiz.title = old_quiz.question

        wrong_answers = []
        for old_answer in old_quiz.get_wrong_answers():
            answer = Answer()
            answer.answer = old_answer
            wrong_answers.append(answer)

            map_answer = MapPageAnswer()
            map_answer.page = quiz
            map_answer.answer = answer
            map_answer.is_correct = 0

            ses.add(answer)
            ses.add(map_answer)

        answer = Answer()
        answer.answer = old_quiz.answer
        wrong_answers.append(answer)

        map_answer = MapPageAnswer()
        map_answer.page = quiz
        map_answer.answer = answer
        map_answer.is_correct = 1

        ses.add(answer)
        ses.add(map_answer)

        map_quiz_tax = MapPageTaxonomy()
        map_quiz_tax.taxonomy = quiz_sets[int(old_quiz.question_set)]
        ses.add(map_quiz_tax)

        quiz.taxonomies.append(map_quiz_tax)
        quiz.time_creation = old_quiz.time_creation
        quiz.time_edited = old_quiz.time_edited

        ses.add(quiz)
    ses.flush()
    ses.commit()
