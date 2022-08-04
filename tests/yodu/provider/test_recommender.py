from yodu.provider import ProviderBase
from yodu.recommeder import RecommenderEngine


def test_recommender():
    recommender = RecommenderEngine()
    recommender.providers = [ProviderBase(), ProviderBase()]
    items = recommender.get_recommendations()
    assert items is not None
    assert len(items) == 2
