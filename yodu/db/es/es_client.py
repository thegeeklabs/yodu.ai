from elasticsearch import Elasticsearch

from yodu import settings


class ESClient:
    client = None

    def __int__(self):
        pass

    def get_client(self):
        if not self.client:
            es_uri = "https://" + settings.ES_USER + ":" + settings.ES_PASSWORD + "@" + settings.ES_HOST + ":" + str(
                settings.ES_PORT)
            self.client = Elasticsearch(hosts=es_uri, verify_certs=False)
        return self.client

    def get_docs(self, item_index, item_ids: list):
        hits = self.get_client().mget(index=item_index,
                                      body={
                                          'ids': item_ids
                                      })
        return hits
