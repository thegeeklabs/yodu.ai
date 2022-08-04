from yodu.provider.top_item_by_action_by_user import TopItemsByUserAction
from yodu.recommeder.db.influx_db import InfluxDb
from yodu.recommeder import RecommenderEngine

org = "influxdata"
algo_spec = {
    "TOP_BY_PREVIOUS_LIKED_SOURCES": {
        "provider": TopItemsByUserAction(),
        "duration": "24h",
        "config": {
            "action_type": "LIKE",
            "tag": "source"
        },
        "weight": 1
    },
    "TOP_BY_PREVIOUS_LIKED_CATEGORIES": {
        "provider": TopItemsByUserAction(),
        "duration": "30h",
        "config": {
            "action_type": "LIKE",
            "tag": "category"
        },
        "weight": 1
    },
    "TOP_BY_PREVIOUS_READ_CATEGORIES": {
        "provider": TopItemsByUserAction(),
        "duration": "30h",
        "config": {
            "action_type": "READ",
            "tag": "category"
        },
        "weight": 1
    }
}


def test_influx_db_client():
    days_ago = 1
    action_type = "LIKE"
    tag = "source"
    limit = 5
    res = InfluxDb().top_by_action(days_ago, action_type, tag, limit)
    # This returns top categories liked by user
    # return top items in these categories by LIKE that are not already liked by user
    print(res)


def test_top_item_by_action_by_user():
    engine = RecommenderEngine(recommender_id=None, algo_spec=algo_spec)
    '''
    action_type: str
    tag: Dict
    user_id: str
    next_token: str
    '''
    # engine.add_provider("TOP_BY_PREVIOUS_LIKED_SOURCES", TopItemsByUserAction())
    action_type = "LIKE"
    tag = {"source": "test"}
    user_id = "1"
    items = engine.get_recommendations(user_id=user_id)
    assert items is not None

