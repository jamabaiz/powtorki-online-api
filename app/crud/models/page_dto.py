from typing import List, Generic

from pydantic import BaseModel


class TaxonomyMapForm(BaseModel):
    id_taxonomy: int


class AnswerMapForm(BaseModel):
    answer: str
    is_correct: bool


class DateForm(BaseModel):
    date_number: int
    date_text: str


class PageForm(BaseModel):
    class Config:
        orm_mode = True

    id_type: int
    id_sub_type: int
    title: str
    document: str | None
    description: str | None
    note: str | None

    taxonomies: List[TaxonomyMapForm] | None
    answers: List[AnswerMapForm] | None
    map_answers: List[AnswerMapForm] | None
    date: DateForm | None


from typing import TypeVar

T = TypeVar('T')


class PagedResult(Generic[T]):
    items: List[T]
    total_number: int

    def __init__(self, items: List[T], total_number: int):
        self.items = items
        self.total_number = total_number
