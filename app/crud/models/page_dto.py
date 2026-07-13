from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict


class TaxonomyMapForm(BaseModel):
    id_taxonomy: int


class AnswerMapForm(BaseModel):
    answer: str
    is_correct: bool


class DateForm(BaseModel):
    date_number: int
    date_text: str


class PageForm(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_type: int
    id_sub_type: int
    title: str
    document: str | None
    description: str | None
    note: str | None

    taxonomies: list[TaxonomyMapForm] | None
    answers: list[AnswerMapForm] | None
    map_answers: list[AnswerMapForm] | None
    date: DateForm | None


T = TypeVar('T')


class PagedResult(BaseModel, Generic[T]):
    items: list[T]
    total_number: int
