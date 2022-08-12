import uuid

from elasticsearch import helpers

from yodu import ESClient


class ItemHelper:
    es_client = None
    index_name = None

    def __init__(self, index_name, es_client: ESClient):
        assert es_client is not None
        assert index_name is not None
        self.es_client = es_client
        self.index_name = index_name

    def add(self, items: list):
        def convert_items(items_list):
            for item in items_list:
                if not item.id:
                    item.id = uuid.uuid4()
                doc = {
                    "_index": self.index_name,
                    "_id": str(item.id),
                    "_source": item.dict(),
                }
                yield doc

        helpers.bulk(self.es_client, convert_items(items))
