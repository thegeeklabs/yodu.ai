from typing import Optional

from pydantic import BaseModel

from yodu.models.category import Category


class Item(BaseModel):
    id: str
    name = str
    category = Optional[Category]
