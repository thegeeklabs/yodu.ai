from datetime import datetime
from typing import Optional, Dict
from uuid import uuid4

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: str = Field(default_factory=uuid4)
    source: str
    tags: Optional[Dict]
    source_provider: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
