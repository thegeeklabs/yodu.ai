from datetime import datetime
from typing import Optional, Dict
from uuid import uuid4

from pydantic import BaseModel, Field


class Action(BaseModel):
    # Unique ID for the item. If no ID is provided, a uuid4 is generated.
    id: str = Field(default_factory=uuid4)

    # Item ID on which this action was performed
    item_id: str

    # User ID who performed this action
    user_id: str

    # the type of action, ex: LIKE, READ, COMMENT etc.
    type: str

    # A numerical value, used by scoring algorithms
    value: float

    # Properties dictionary to hold various metadata such as tags, categories, authors etc.
    props: Optional[Dict]

    # Time when the item was created
    created_at: datetime = Field(default_factory=datetime.now)
