from typing import Dict, Optional

from pydantic import BaseModel, Field


class Request(BaseModel):
    args: Optional[Dict]
    user_id: Optional[str]
    limit: Optional[int] = Field(default=10)
    offset: Optional[int] = Field(default=0)
    next_token: Optional[str]
