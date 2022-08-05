import uuid

from elasticsearch import helpers


class ItemHelper:
    es_client = None
    index_name = None

    def __init__(self, index_name, es_client):
        assert es_client is not None
        assert index_name is not None
        self.es_client = es_client
        self.index_name = index_name

    def add(self, items: list):

        def convert_items(items_list):
            for action in items_list:
                if not action.id:
                    action.id = uuid.uuid4()
                doc = {
                    "_index": self.index_name,
                    "_id": str(action.id),
                    "_source": action.dict()
                }
                yield doc

        helpers.bulk(self.es_client, convert_items(items))
