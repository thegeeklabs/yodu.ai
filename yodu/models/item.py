from datetime import datetime
from typing import Optional, Dict
from uuid import uuid4

from pydantic import BaseModel, Field


class Item(BaseModel):
    # Unique ID for the item. If no ID is provided, a uuid4 is generated.
    id: str = Field(default_factory=uuid4)

    # Id of the source i.e. the publisher or the User who created this Item
    source: str

    # Properties dictionary to hold various metadata such as tags, categories, authors etc.
    props: Optional[Dict]

    # Internal identifier to specify if this item was provided by a Yodu Provider
    source_provider: Optional[str]

    # Time when the item was created
    created_at: datetime = Field(default_factory=datetime.now)

    # Time when the item was updated
    updated_at: datetime = Field(default_factory=datetime.now)
