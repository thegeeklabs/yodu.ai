import time
from queue import Queue
from threading import Thread

import yodu.provider as provider
from yodu import ESClient
from yodu.helpers.action_helper import ActionHelper
from yodu.helpers.item_helper import ItemHelper
from yodu.provider.provider_base import ProviderBase

NUM_THREADS = 5
que = Queue()
threads_list = list()


class Recommender:
    __recommender_name = None
    __providers = None
    __algo_spec = None
    __indices = None
    __es_client = None

    item = None
    action = None
    provider = None

    def __init__(self, name, indices, algo_spec=None, es_client=None):
        self.recommender_name = name
        self.__indices = indices
        if algo_spec:
            self.__algo_spec = algo_spec
        self.__es_client = es_client
        if self.__es_client == None:
            self.__es_client = ESClient().get_client()
        self.provider = provider

        self.item = ItemHelper(index_name=self.__indices["items"], es_client=self.__es_client)
        self.action = ActionHelper(index_name=self.__indices["actions"], es_client=self.__es_client)

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
