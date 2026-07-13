from pydantic import BaseModel, ConfigDict


class DbCharacter(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str | None
    description: str | None
    note: str | None


class UpdateCharacter(BaseModel):
    name: str | None
    description: str | None
    note: str | None


class CreateCharacter(BaseModel):
    name: str | None
    description: str | None
    note: str | None
