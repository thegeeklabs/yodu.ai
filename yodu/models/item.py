from datetime import datetime
from typing import Optional, Dict
from uuid import uuid4

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: str = Field(default_factory=uuid4)
    tags: Optional[Dict]
    type: str
    value: float
    tags: Optional[Dict]
    created_at: datetime = Field(default_factory=datetime.now)
