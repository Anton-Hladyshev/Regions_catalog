from pydantic import BaseModel
from typing import Union, List


class Unit_Model(BaseModel):
    code: str
    name: str
    name_en: str
    level: int
    parent_id: Union[str, None]
    category: str
    children_count: Union[int, None]

class Catalog_of_units(BaseModel):
    has_next: bool
    has_previous: bool
    page: int
    result: List[Union[Unit_Model, None]]
