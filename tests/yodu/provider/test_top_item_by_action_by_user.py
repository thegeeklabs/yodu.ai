from yodu.db.es.es_client import ESClient
from provider.providers.top_item_by_user_action.provider import TopItemsByUserAction
from yodu.recommeder import RecommenderEngine

org = "influxdata"
algo_spec = {
    "TOP_BY_PREVIOUS_LIKED_SOURCES": {
        "provider": TopItemsByUserAction(),
        "duration": "24h",
        "config": {"action_type": "LIKE", "tag": "source"},
        "weight": 1,
    },
    "TOP_BY_PREVIOUS_LIKED_CATEGORIES": {
        "provider": TopItemsByUserAction(),
        "duration": "30h",
        "config": {"action_type": "LIKE", "tag": "category"},
        "weight": 1,
    },
    "TOP_BY_PREVIOUS_READ_CATEGORIES": {
        "provider": TopItemsByUserAction(),
        "duration": "30h",
        "config": {"action_type": "READ", "tag": "category"},
        "weight": 1,
    },
}


def test_top_item_by_action_by_user():
    engine = RecommenderEngine(recommender_id=None, algo_spec=algo_spec)
    """
    action_type: str
    tag: Dict
    user_id: str
    next_token: str
    """
    # engine.add_provider("TOP_BY_PREVIOUS_LIKED_SOURCES", TopItemsByUserAction())
    action_type = "LIKE"
    tag = {"source": "test"}
    user_id = "1"
    items = engine.get_recommendations(user_id=user_id)
    assert items is not None


def test_top_items_by():
    provider = TopItemsByUserAction()
    query = provider.top_by_action(days_ago=7, action_type="INDEXER_COMMENT_CREATED", tag="pubId", limit=10)
    es_client = ESClient().get_client()
    hits = es_client.search(index="lens", size=0, **query)
    res = hits.body["aggregations"]['top_tag_by_action']['buckets']
    print(res)
