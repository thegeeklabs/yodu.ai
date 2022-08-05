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

    def add_records(self, index_name, items):
        try:
            for item in items:
                print(item)
        except Exception as e:
            raise e
        return True

    def get_records(self):
        pass

    def add_users(self, users):
        return users

    def add_actions(self, actions):
        return actions

    def query(self, **kwargs):
        pass
