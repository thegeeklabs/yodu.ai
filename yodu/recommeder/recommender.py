import time
import uuid
from queue import Queue
from threading import Thread

from yodu.db.es.es_client import ESClient
from yodu.provider.provider_base import ProviderBase
from yodu.recommeder.db.influx_db import InfluxDb

NUM_THREADS = 5
que = Queue()
threads_list = list()


class RecommenderEngine:
    __recommender_id = None
    __providers = None
    __es_client = None
    __influxdb_client = None
    __algo_spec = None

    def __init__(self, recommender_id, algo_spec):
        if not recommender_id:
            self.recommender_id = recommender_id
        else:
            self.recommender_id = uuid.uuid4()
        self.__es_client = ESClient()
        self.__influxdb_client = InfluxDb().get_client()
        self.__algo_spec = algo_spec
        self.set_algo_specifications(algo_spec)

    def set_algo_specifications(self, algo_spec):
        for name, config in algo_spec.items():
            self.add_provider(name, config["provider"])

    def add_provider(self, name: str, provider: ProviderBase):
        if not self.__providers:
            self.__providers = {}
        self.__providers[name] = provider

    def remove_provider(self, name):
        if name in self.__providers:
            self.__providers.pop(name)

    def init_provider(self, provider, config, user_id):
        pass

    def get_recommendations(self, user_id):
        """
        Algo:
        Add all providers to threads.
        Wait for x seconds
        return results
        """
        for name, provider in self.__providers.items():
            args = self.__algo_spec[name]["config"]
            args["user_id"] = user_id
            worker = Thread(
                target=lambda q, config: q.put(provider.get_items(config=config)),
                args=(que, args),
            )
            worker.start()
            threads_list.append(worker)

        # Join all the threads
        time.sleep(1)
        for t in threads_list:
            t.join()

        # Check thread's return value
        results = []
        while not que.empty():
            result = que.get()
            results.append(result)

        return results
