from pydantic import BaseModel


class UnitModel(BaseModel):
    code: str
    name: str
    name_en: str
    level: int
    parent_id: str | None
    category: str
    children_count: int | None


class CatalogOfUnits(BaseModel):
    has_next: bool
    has_previous: bool
    page: int
    result: list[UnitModel | None]
