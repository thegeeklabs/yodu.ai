from typing import Dict, Optional

from pydantic import BaseModel, Field


class Request(BaseModel):
    # Any fields defined in props will be used to overwrite Provider's default properties
    props: Optional[Dict]

    # user_id of the User for whom items are to be recommended
    user_id: Optional[str]

    # limit on how many items are needed
    limit: Optional[int] = Field(default=10)

    # pagination variable to offset starting point
    offset: Optional[int] = Field(default=0)

    # Internal next_token used by some providers
    next_token: Optional[str]
