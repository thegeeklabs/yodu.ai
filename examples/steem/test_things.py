from typing import Dict, Optional

from pydantic import BaseModel, Field

# provider.enable(recommender_name="test_recommender", name="top_item_by_user_action")

meta = {
    "name": "TopItemsByUserAction",
    "author": "Shashank Agarwal",
    "description": "Return top items for a source by action_type \
        Example: Return top liked items for a given source \
        Example: Return top read items for a given source \
        Example: Return top read items for a given category",
    "args": {
        "action_type": {
            "type": "str",
            "source": "request.args.action_type"
        },
        "days_ago": {
            "type": "int",
            "source": "request.args.days_ago",
            "default": 1
        },
        "user_id": {
            "type": "str",
            "source": "request.args.user_id"
        },
        "tag": {
            "type": "str",
            "source": "request.args.tag"
        },
        "next_token": {
            "type": "str",
            "source": "request.next_token"
        },
        "limit": {
            "type": "int",
            "source": "request.limit",
            "default": 10
        },
        "offset": {
            "type": "int",
            "source": "request.offset",
            "default": 0
        },
    }
}





build_input_args(request)
