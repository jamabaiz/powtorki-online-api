from pydantic import BaseModel, ConfigDict


class TaxonomyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_parent: int | None
    id_taxonomy_type: int
    name: str
    description: str | None
    path: list[str] = []


class TaxonomyForm(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_parent: int | None
    id_taxonomy_type: int
    name: str
    description: str | None
