from typing import Dict

from yodu import ESClient
from yodu.models.request import Request


class ProviderBase:
    __meta = None
    __data = None

    def __init__(self, meta, data):
        self.__meta = meta
        self.__data = data

    def get_items(self, **kwprops):
        pass

    def get_meta(self):
        return self.__meta

    def build_input(self, config: Dict, request: Request):
        input_dict = {}
        """
        Get all values from request
        Then get all values from config
        Rest all values from meta
        """
        if request.limit:
            input_dict["limit"] = request.limit
        if request.offset:
            input_dict["offset"] = request.offset
        if request.user_id:
            input_dict["user_id"] = request.user_id
        if request.props:
            for key, val in request.props.items():
                input_dict[key] = val
        for name, val in config.items():
            if name not in input_dict:
                input_dict[name] = config[name]
        for name, val in self.__meta["props"].items():
            if (
                name not in input_dict
                and name in self.__meta["props"]
                and "default" in self.__meta["props"][name]
            ):
                input_dict[name] = self.__meta["props"][name]["default"]
        return input_dict

    def execute(self, es_client: ESClient, indices, query):
        action_index = indices["actions"]
        hits = es_client.get_client().search(
            index=action_index, size=0, **query
        )
        res = hits.body["aggregations"]["top_tag_by_action"]["buckets"]
        """
        returns a list of top categories.
        We then get items from each of these categories and rank by count
        """
        items_dict = {}
        for hit in res:
            for row in hit["top_action_hits"]["hits"]["hits"]:
                item = row["_source"]
                if "item_id" in item:
                    if item["item_id"] in items_dict:
                        items_dict[item["item_id"]] = (
                            items_dict[item["item_id"]] + 1
                        )
                    else:
                        items_dict[item["item_id"]] = 1
        items_dict = dict(
            sorted(items_dict.items(), key=lambda item: item[1], reverse=True)
        )
        top_items = list(items_dict.keys())
        return top_items
