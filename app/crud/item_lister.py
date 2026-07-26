from random import shuffle
import logging

from sqlalchemy.orm import Session, joinedload, selectin_polymorphic

from app.constants import PageTypes, ActivitySettings, PageSubTypes
from app.crud.models.page_dto import PageForm, PagedResult
from app.database import models
from app.helpers import get_descendants
from app.render.renderer import PageRenderer

logger = logging.getLogger(__name__)


class CompareResult:
    def __init__(self, added, removed) -> None:
        self.added = added
        self.removed = removed
        super().__init__()

    def __repr__(self) -> str:
        return f"CompareResult(Added=[{self.added}], Removed=[{self.removed}])"


def compare_sets(old: set, new: set):
    new_set = set(new)
    old_set = set(old)
    inter = new_set & old_set
    return CompareResult(new_set - inter, old_set - inter)


class ItemLister:

    def __init__(self, db: Session, limit: int = 20) -> None:
        self.db = db
        self.pagination_limit = limit

        self.filter_taxonomies: list[int] = []
        self.filter_sub_types: list[int] = []
        self.filter_page_types: list[int] = []
        self.filter_name: str = ""
        self.render_enabled = True

    def set_from_form(self, item: models.Page | models.QuizPage | models.CalendarPage, form: PageForm):
        item.title = form.title
        item.document = form.document
        item.note = form.note
        item.description = form.description
        item.id_type = form.id_type
        item.id_sub_type = form.id_sub_type
        # item.order_no = form.order_no

        current_taxonomy_ids = [tax.id_taxonomy for tax in item.taxonomies]
        form_taxonomy_ids = [tax.id_taxonomy for tax in form.taxonomies]

        difference = compare_sets(set(current_taxonomy_ids), set(form_taxonomy_ids))

        for tax in [taxonomy for taxonomy in item.taxonomies if taxonomy.id_taxonomy in difference.removed]:
            self.db.delete(tax)

        for taxonomy_id in difference.added:
            item.taxonomies.append(models.MapPageTaxonomy(id_taxonomy=taxonomy_id))

        if item.id_type == PageTypes.QuizPage:
            current_answers = {(answer.answer.answer, answer.is_correct) for answer in item.map_answers}
            form_answers = {(answer.answer, answer.is_correct) for answer in form.answers}

            difference = compare_sets(current_answers, form_answers)

            for map_answer_to_remove in [map_answer for map_answer in item.map_answers
                                         if (map_answer.answer.answer, map_answer.is_correct) in difference.removed]:
                self.db.delete(map_answer_to_remove)

            for new_answer in difference.added:
                text, is_correct = new_answer
                answer_entry = models.Answer(answer=text)
                map_answer_entry = models.MapPageAnswer(answer=answer_entry, is_correct=is_correct)
                self.db.add(answer_entry)
                self.db.add(map_answer_entry)
                item.map_answers.append(map_answer_entry)

        if item.id_type == PageTypes.CalendarPage:
            if item.date is not None:
                item.date.date_number = form.date.date_number
                item.date.date_text = form.date.date_text
            else:
                new_date = models.Date(date_text=form.date.date_text, date_number=form.date.date_number)
                item.date = new_date
                self.db.add(new_date)

        return item

    def post_item(self, form):
        if form.id_type == PageTypes.QuizPage:
            item = models.QuizPage()
        elif form.id_type == PageTypes.CalendarPage:
            item = models.CalendarPage()
        else:
            item = models.Page()
        self.db.add(item)
        item = self.set_from_form(item, form)
        self.db.commit()
        return item

    def put_item(self, page_id: int, form):
        item = self.get_item(page_id)
        item = self.set_from_form(item, form)
        self.db.commit()
        return item

    def delete_item(self, page_id: int):
        try:
            item = self.get_item(page_id)
            self.db.delete(item)
            self.db.commit()
            return True
        except Exception:
            logger.exception(f"Error deleting item {page_id}")
            return False

    def get_item(self, page_id: int) -> models.Page | models.QuizPage | models.CalendarPage | models.DictionaryPage | models.CharacterPage:
        renderer = PageRenderer()

        item = (self.db.query(models.Page)
                .options(
            selectin_polymorphic(models.Page, [models.QuizPage, models.DocumentPage, models.CalendarPage]),
            joinedload(models.QuizPage.answers)
            .load_only(models.PageAnswer.id, models.PageAnswer.id_answer, models.PageAnswer.answer,
                       models.PageAnswer.is_correct)  # todo: is_correct, only for frontend
            ,
            joinedload(models.DocumentPage.media),
            joinedload(models.CalendarPage.date),
            joinedload(models.Page.taxonomies).joinedload(models.MapPageTaxonomy.taxonomy))
                .filter(models.Page.id == page_id).first())

        if not item:
            raise ValueError("Page not found")

        if self.render_enabled:
            user_activity = models.UserActivity()
            user_activity.id_user = 1
            user_activity.id_page = item.id
            user_activity.knowledge = ActivitySettings.page_read
            self.db.add(user_activity)
            self.db.commit()
            if item.document:
                item.document = renderer.render(item.document)

        return item

    def get_items(self, pagination_no: int = 1) -> PagedResult[models.Page]:
        if not pagination_no > 0:
            raise ValueError("Page cannot be less than 1")
        offset = pagination_no - 1

        query = (self.db.query(models.Page)  # noqa
        .join(models.Page.taxonomies)
        .join(models.CalendarPage.date, isouter=True)
        .join(models.QuizPage.answers, isouter=True)
        .options(
            selectin_polymorphic(models.Page, [models.QuizPage, models.DocumentPage, models.CalendarPage]),
            joinedload(models.QuizPage.answers)
            .load_only(models.PageAnswer.id, models.PageAnswer.id_answer, models.PageAnswer.answer),
            joinedload(models.DocumentPage.media),
            joinedload(models.CalendarPage.date),
            joinedload(models.Page.taxonomies)))

        if len(self.filter_taxonomies) > 0:
            taxonomies = [get_descendants(self.db, [taxonomy]) for taxonomy in self.filter_taxonomies][0]
            query = query.filter(
                models.MapPageTaxonomy.id_taxonomy.in_(taxonomies),
            )

        if len(self.filter_page_types) > 0:
            query = query.filter(models.Page.id_type.in_(self.filter_page_types))

        if len(self.filter_sub_types) > 0:
            query = query.filter(models.Page.id_sub_type.in_(self.filter_sub_types))

        if len(self.filter_name) > 0:
            query = query.filter(
                # or_(
                # models.Page.title.match(self.filter_name),
                models.Page.title.like(f'%{self.filter_name}%')
                # )
            )

        if len(self.filter_sub_types) == 1:
            page_type = self.filter_sub_types[0]
            if page_type == PageSubTypes.Date:
                query = query.order_by(models.Date.date_number)
            elif page_type == PageSubTypes.Character or page_type == PageSubTypes.Dictionary:
                query = query.order_by(models.Page.title)
            else:
                query = query.order_by(models.MapPageTaxonomy.order_no, models.Page.title)
        else:
            query = query.order_by(models.Page.title)

        query = query.distinct(models.Page.id).from_self()

        total_number = query.count()

        results = query.offset(self.pagination_limit * offset).limit(self.pagination_limit).all()
        for page in results:
            if page.id_type == PageTypes.QuizPage:
                shuffle(page.answers)

        return PagedResult(items=results, total_number=total_number)
