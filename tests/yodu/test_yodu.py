from yodu.recommeder.recommender import RecommenderEngine

test_items = [
    {
        "item_id": "1",
        "title": "test title 1",
        "category": "technology",
        "created_at": "some_date",
        "updated_at": "some_date",
        "tags": ["technology", "ai", "ml"],
        "description": "This is a test item"
    }
]

test_action = [{
    "action_id": "1",
    "item_id": "1",
    "user_id": "1",
    "action_type": "LIKE",
    "created_at": "some_date",
    "updated_at": "some_date"
}]

test_users = {
    "user_id": "1",
    "created_at": "some_date",
    "updated_at": "some_date"
}


def test_yodu():
    recommender_id = None
    config = None
    recommender = RecommenderEngine(recommender_id, config)
    recommender.add_items(test_items)
    recommender.add_users(test_users)
    # recommender.add_actions(test_actions)
    # recommender.get_recommendations(user_id, algo_spec, limit, offset)
