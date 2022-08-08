import yodu
from examples.steem.helpers import load_test_items, load_test_actions
from models.request import Request

recommender = yodu.create_recommender(name="example")

recommender = yodu.get_recommender(name="example")

# Add Items to Recommender
items = load_test_items()
recommender.item.add(items)

# Add Actions to Recommender
actions = load_test_actions()
recommender.action.add(actions)

# Enable Yodu's built-in Providers
recommender.provider.add(name="top_item_by_user_action")
# Add provider from Source (Coming Soon)

algo_spec = {
    "TOP_BY_PREVIOUS_LIKED_SOURCES": {
        "provider": "top_item_by_user_action",
        "duration": "24h",
        "config": {
            "action_type": "LIKE",
            "tag": "source"
        },
        "weight": 1
    },
    "TOP_BY_PREVIOUS_LIKED_CATEGORIES": {
        "provider": "top_item_by_user_action",
        "duration": "30h",
        "config": {
            "action_type": "LIKE",
            "tag": "category"
        },
        "weight": 1
    },
    "TOP_BY_PREVIOUS_READ_CATEGORIES": {
        "provider": "top_item_by_user_action",
        "duration": "30h",
        "config": {
            "action_type": "READ",
            "tag": "category"
        },
        "weight": 1
    }
}
recommender.algo_spec.set(algo_spec=algo_spec)

args = {
    "days_ago": "7"
}
request = Request(user_id="test_user_1", args=args)

items = recommender.get_items(request=request)
