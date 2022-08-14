import unittest

import yodu
from test_utils.test_utils import load_test_items, load_test_actions
from yodu.models.request import Request


class TestYodu(unittest.TestCase):
    def test_recommender(self):
        recommender_name = "example"
        yodu.delete_recommender(name=recommender_name)
        recommender = yodu.create_recommender(name=recommender_name)

        recommender = yodu.get_recommender(name=recommender_name)

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
            "providers": {
                "TOP_BY_PREVIOUS_LIKED_SOURCES": {
                    "provider": "top_item_by_user_action",
                    "description": "Get top items from past top liked sources",
                    "duration": "24h",
                    "config": {"action_type": "LIKE", "tag": "source"},
                    "weight": 1,
                },
                "TOP_BY_PREVIOUS_LIKED_CATEGORIES": {
                    "provider": "top_item_by_user_action",
                    "description": "Get top items from past top liked categories",
                    "duration": "30h",
                    "config": {"action_type": "LIKE", "tag": "category"},
                    "weight": 1,
                },
                "TOP_BY_PREVIOUS_READ_CATEGORIES": {
                    "provider": "top_item_by_user_action",
                    "description": "Get top items from past top READ categories",
                    "duration": "30h",
                    "config": {"action_type": "READ", "tag": "category"},
                    "weight": 1,
                },
            },
            "filters": {
                "PAST_ACTION": {
                    "provider": "get_past_user_item_action",
                    "description": "Filter items if a user has performed any action on the item",
                    "duration": "24h",
                    "config": {"action_type": "ALL"},
                },
            },
        }
        recommender.algo_spec.set(algo_spec=algo_spec)

        props = {"days_ago": "7"}
        request = Request(user_id="test_user_1", props=props)

        items = recommender.get_items(request=request)
        assert items is not None
        assert len(items) == 10
