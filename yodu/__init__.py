__title__ = "Yodu.ai Recommendation Engine"
__version__ = "0.0.4"
__author__ = "Shashank Agarwal"
__license__ = "Apache"
__copyright__ = "Copyright 2022-present The Geek Labs"

from yodu.db.es.es_client import ESClient
from yodu.recommeder.recommender import Recommender

TITLE = __title__
VERSION = __version__
AUTHOR = __author__
LICENSE = __license__
COPYRIGHT = __copyright__

DEFAULT_INDICES = ["items", "actions"]


def init():
    pass


def create_recommender(name: str):
    es = ESClient().get_client()
    indices = {}
    for index in DEFAULT_INDICES:
        indices[index] = name + "_" + index
    try:
        for key, val in indices.items():
            es.indices.create(index=val)
    except Exception as e:
        raise e
    return Recommender(name=name, indices=indices, es_client=es)


def get_recommender(name: str):
    es = ESClient().get_client()
    indices_res = es.indices.get(index=name + "_*")
    indices = {}

    if indices_res and indices_res.body:
        indices_dict = {}
        for index in indices_res.body:
            indices_dict[index] = 1
        for index in DEFAULT_INDICES:
            if name + "_" + index in indices_dict:
                indices[index] = name + "_" + index
    return Recommender(name=name, indices=indices, es_client=es)


def delete_recommender(name: str):
    recommeder = get_recommender(name)
    es = ESClient().get_client()
    indices = recommeder.get_indices()
    for index, index_name in indices.items():
        es.indices.delete(index=index_name)
