import yodu
from examples.steem.helpers import load_test_items, load_test_actions

# yodu.init(HOST="", PORT="")

# recommender = yodu.create_recommender(name="getting_started")
recommender = yodu.get_recommender(name="getting_started")

# Add Items to Recommender
items = load_test_items()
recommender.item.add(items)

# Add Actions to Recommender
actions = load_test_actions()
recommender.action.add(items)

# Enable Yodu's built-in Providers
recommender.enable_provider(name="TopItemsByUserAction")

# Add provider from Source (Coming Soon)
recommender.add_provider(name="CUSTOM_PROVIDER",
                         source="https://github.com/thegeeklabs/yodu.ai/tree/dev/src/yodu/provider/some_dir")
recommender.enable_provider(name="CUSTOM_PROVIDER")

algo_spec = {
    "TOP_BY_PREVIOUS_LIKED_SOURCES": {
        "provider": "TopItemsByUserAction",
        "duration": "24h",
        "config": {
            "action_type": "LIKE",
            "tag": "source"
        },
        "weight": 1
    },
    "TOP_BY_PREVIOUS_LIKED_CATEGORIES": {
        "provider": "TopItemsByUserAction",
        "duration": "30h",
        "config": {
            "action_type": "LIKE",
            "tag": "category"
        },
        "weight": 1
    },
    "TOP_BY_PREVIOUS_READ_CATEGORIES": {
        "provider": "TopItemsByUserAction",
        "duration": "30h",
        "config": {
            "action_type": "READ",
            "tag": "category"
        },
        "weight": 1
    },
    "TOP_BY_PREVIOUS_READ_CATEGORIES": {
        "provider": "CUSTOM_PROVIDER",
        "duration": "30h",
        "config": {
            "action_type": "READ",
            "tag": "category"
        },
        "weight": 1
    }
}
recommender.add_algo_spec(name="first_algo_spec", config=algo_spec)

items = recommender.get_items(user_id="1", algo_spec="first_algo_spec")
