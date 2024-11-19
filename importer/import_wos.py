import json
import logging
from pprint import pprint
from typing import TypeVar, Any

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ChapterTaxonomy, DocumentPage, MapPageTaxonomy, CharacterPage, Date, CalendarTaxonomy, \
    Media, ScriptPage, MindmapPage, QAPage, QuizTaxonomy, QuizPage, Answer, MapPageAnswer, CalendarPage, DictionaryPage, \
    QATaxonomy
from importer.models_wos import Character, Dictionary, Document, Lesson, Page, Question, Quiz

T = TypeVar('T')


def open_file_read_objects(file_name: str, class_type: T) -> dict[int, T]:
    item_dict = {}

    with open(file_name, encoding='utf-8', mode='r') as file:
        j = json.loads(file.read())
        for entry in j:
            u = class_type(**entry)
            item_dict[int(u.id)] = u
        return item_dict


characters = open_file_read_objects('./dump/wos_characters.json', Character)
dictionary = open_file_read_objects('./dump/wos_dictionary.json', Dictionary)
documents = open_file_read_objects('./dump/wos_documents.json', Document)
lessons = open_file_read_objects('./dump/wos_video.json', Lesson)
pages = open_file_read_objects('./dump/wos_pages.json', Page)
questions = open_file_read_objects('./dump/wos_questions.json', Question)
quizzes = open_file_read_objects('./dump/wos_question_sets.json', Quiz)

map_modules_id = {
    1: 21,
    2: 22,
    3: 23,
    4: 24,
    5: 25,
    6: 26,
    7: 27,
    8: 28,
    9: 29,
    10: 30,
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
