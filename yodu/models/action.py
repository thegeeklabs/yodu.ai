from datetime import datetime
from typing import Optional, Dict
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class Action(BaseModel):
    id: str = Field(default_factory=uuid4)
    item_id: str
    user_id: str
    type: str
    value: float
    tags: Optional[Dict]
    created_at: datetime = Field(default_factory=datetime.now)
