import json
from datetime import datetime


class Character:
    id: int
    name: str
    description: str
    note: str
    time_creation: datetime
    time_edited: datetime
    image: None
    module: int

    def __init__(self, id: int, name: str, description: str, note: str, time_creation: datetime, time_edited: datetime,
                 image: None, module: int) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.note = note
        self.time_creation = time_creation
        self.time_edited = time_edited
        self.image = image
        self.module = module

    def __repr__(self):
        return json.dumps(self.__dict__)


class Dictionary:
    id: int
    name: str
    description: str
    note: str
    time_creation: datetime
    time_edited: datetime
    module: None

    def __init__(self, id: int, name: str, description: str, note: str, time_creation: datetime, time_edited: datetime,
                 module: None) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.note = note
        self.time_creation = time_creation
        self.time_edited = time_edited
        self.module = module

    def __repr__(self):
        return json.dumps(self.__dict__)


class Document:
    id: int
    name: str
    description: str
    document: int
    module: int
    time_creation: datetime
    time_edited: datetime

    def __init__(self, id: int, name: str, description: str, document: int, module: int, time_creation: datetime,
                 time_edited: datetime) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.document = document
        self.module = module
        self.time_creation = time_creation
        self.time_edited = time_edited

    def __repr__(self):
        return json.dumps(self.__dict__)


class Lesson:
    id: int
    name: str
    url: str
    description: str
    time_creation: datetime
    time_edited: datetime
    module: int
    document: int

    def __init__(self, id: int, name: str, url: str, description: str, time_creation: datetime, time_edited: datetime,
                 module: int, document: int) -> None:
        self.id = id
        self.name = name
        self.url = url
        self.description = description
        self.time_creation = time_creation
        self.time_edited = time_edited
        self.module = module
        self.document = document

    def __repr__(self):
        return json.dumps(self.__dict__)


class Page:
    id: int
    name: str
    document: str
    document_rendered: str
    time_creation: datetime
    time_edited: datetime
    time_rendered: datetime

    def __init__(self, id: int, name: str, document: str, document_rendered: str, time_creation: datetime,
                 time_edited: datetime, time_rendered: datetime) -> None:
        self.id = id
        self.name = name
        self.document = document
        self.document_rendered = document_rendered
        self.time_creation = time_creation
        self.time_edited = time_edited
        self.time_rendered = time_rendered

    def __repr__(self):
        return json.dumps(self.__dict__)


import re


class Question:
    id: int
    question: str
    answer: str
    answers_other: str
    image: None
    question_set: int
    time_creation: datetime
    time_edited: datetime

    def get_wrong_answers(self):
        # self.answers_other = self.answers_other.replace("\n", ";")
        answers_search = re.findall(";s:([0-9]+):\"(.*?)\"", self.answers_other, re.MULTILINE | re.DOTALL)
        array = []

        for found in answers_search:
            result = found[1]
            array.append(result)

        return array

    def __init__(self, id: int, question: str, answer: str, answers_other: str, image: None, question_set: int,
                 time_creation: datetime, time_edited: datetime) -> None:
        self.id = id
        self.question = question
        self.answer = answer
        self.answers_other = answers_other
        self.image = image
        self.question_set = question_set
        self.time_creation = time_creation
        self.time_edited = time_edited

    def __repr__(self):
        return json.dumps(self.__dict__)


class QuestionAnswer:
    id: int
    question: str
    answer: str
    question_set: str
    module: int
    image: str
    time_edited: datetime
    time_creation: datetime

    def __init__(self, id: int, question: str, answer: str, question_set: str, module: int, image: str,
                 time_edited: datetime, time_creation: datetime) -> None:
        self.id = id
        self.question = question
        self.answer = answer
        self.question_set = question_set
        self.module = module
        self.image = image
        self.time_edited = time_edited
        self.time_creation = time_creation

    def __repr__(self):
        return json.dumps(self.__dict__)


class Quiz:
    id: int
    name: str
    description: None
    time_creation: datetime
    time_edited: datetime
    module: int

    def __init__(self, id: int, name: str, description: None, time_creation: datetime, time_edited: datetime,
                 module: int) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.time_creation = time_creation
        self.time_edited = time_edited
        self.module = module

    def __repr__(self):
        return json.dumps(self.__dict__)


class User:
    id: int
    name: str
    email: str
    password: str
    session_token: None
    date_creation: datetime
    secret_key: None
    activated: int
    role: int

    def __init__(self, id: int, name: str, email: str, password: str, session_token: None, date_creation: datetime,
                 secret_key: None, activated: int, role: int) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.session_token = session_token
        self.date_creation = date_creation
        self.secret_key = secret_key
        self.activated = activated
        self.role = role

    def __repr__(self):
        return json.dumps(self.__dict__)


class UsersActivations:
    id: int
    id_licence: int
    id_user: int
    date_activation: datetime
    info: None
    licence: str

    def __init__(self, id: int, id_licence: int, id_user: int, date_activation: datetime, info: None,
                 licence: str) -> None:
        self.id = id
        self.id_licence = id_licence
        self.id_user = id_user
        self.date_activation = date_activation
        self.info = info
        self.licence = licence

    def __repr__(self):
        return json.dumps(self.__dict__)


class UserLicence:
    id: int
    key: str
    module: int
    type: str
    creation_date: datetime

    def __init__(self, id: int, key: str, module: int, type: str, creation_date: datetime) -> None:
        self.id = id
        self.key = key
        self.module = module
        self.type = type
        self.creation_date = creation_date

    def __repr__(self):
        return json.dumps(self.__dict__)
