from typing import Dict, Optional

from pydantic import BaseModel, Field


class Request(BaseModel):
    args: Optional[Dict]
    user_id: Optional[str]
    limit: Optional[int] = Field(default=10)
    offset: Optional[int] = Field(default=0)
    next_token: Optional[str]
'''
Users create a provider which needs certain arguments.
These args can be provided from "default_values or algo_spec or in the request itself.
Good practise it to provide most values in algo_specification.
providers are added or removed to/from a recommender
But enabled using algo_spec.
 
'''