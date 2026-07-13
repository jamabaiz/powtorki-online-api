from typing import List

from pydantic import BaseModel


class TaxonomyOut(BaseModel):
    class Config:
        from_attributes = True

    id: int
    id_parent: int | None
    id_taxonomy_type: int
    name: str
    description: str | None
    path: List[str] = []


class TaxonomyForm(BaseModel):
    class Config:
        from_attributes = True

    id_parent: int | None
    id_taxonomy_type: int
    name: str
    description: str | None
