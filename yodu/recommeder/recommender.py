from queue import Queue

import ray

from yodu import ESClient
from yodu.algo_spec.helper import AlgoSpecHelper
from yodu.helpers.action_helper import ActionHelper
from yodu.helpers.item_helper import ItemHelper
from yodu.models.request import Request
from yodu.provider.helper import ProviderHelper

NUM_THREADS = 5
que = Queue()
threads_list = list()


class Recommender:
    __recommender_name = None
    __providers = None
    __indices = None
    __es_client = None

    item = None
    action = None
    provider = None
    algo_spec = None

    def __init__(self, name, indices, algo_spec=None, es_client=None):
        self.recommender_name = name
        self.__indices = indices
        self.__es_client = es_client
        if self.__es_client is None:
            self.__es_client = ESClient().get_client()
        self.provider = ProviderHelper(recommender_name=self.recommender_name)
        self.item = ItemHelper(
            index_name=self.__indices["items"], es_client=self.__es_client
        )
        self.action = ActionHelper(
            index_name=self.__indices["actions"], es_client=self.__es_client
        )
        self.algo_spec = AlgoSpecHelper(recommender_name=self.recommender_name)

    def get_docs(self, item_index, item_ids: list):
        hits = self.__es_client.mget(index=item_index, body={"ids": item_ids})
        items = []
        for doc in hits.body["docs"]:
            items.append(doc["_source"])
        return items

    def get_indices(self):
        return self.__indices

    def get_items(self, request: Request):
        """
        Algo:
        Add all providers to threads.
        Wait for x seconds
        return results
        """
        algo_spec = self.algo_spec.load()

        result_ids = []
        for provider_name, provider_dict in algo_spec["providers"].items():
            args = provider_dict["config"]
            provider_obj = self.provider.load_provider(
                name=provider_dict["provider"]
            ).remote(indices=self.__indices, name=provider_name)
            args["user_id"] = request.user_id
            result_ids.append(
                provider_obj.get_items.remote(config=args, request=request)
            )

        results = ray.get(result_ids)
        top_items_ids = {}
        top_items_providers = {}
        for provider_results in results:
            provider_name = provider_results[0]
            for item_id in provider_results[1]:
                if item_id in top_items_ids:
                    top_items_ids[item_id] = top_items_ids[item_id] + 1
                    top_items_providers[item_id].append(provider_name)
                else:
                    top_items_ids[item_id] = 1
                    top_items_providers[item_id] = [provider_name]
        top_items_ids = dict(
            sorted(
                top_items_ids.items(), key=lambda item: item[1], reverse=True
            )
        )
        if len(top_items_ids) > 0:
            top_items_ids = list(top_items_ids.keys())[: request.limit]
            items = self.get_docs(
                item_index=self.__indices["items"],
                item_ids=top_items_ids,
            )
            for item in items:
                item["source_provider"] = top_items_providers[item["id"]][0]
            return items
        return None
