import json
from typing import Dict, Any

import ray

from models.request import Request
from yodu import ESClient
from yodu.provider.provider_base import ProviderBase
from yodu.utils.utils import time_ago_to_date

meta = {
    "name": "TopItemsByUserAction",
    "version": "0.0.1",
    "author": "Shashank Agarwal",
    "description": "Return top items for a source by action_type \
        Example: Return top liked items for a given source \
        Example: Return top read items for a given source \
        Example: Return top read items for a given category",
    "args": {
        "action_type": {
            "type": "str",
            "source": "request.args.action_type"
        },
        "days_ago": {
            "type": "int",
            "source": "request.args.days_ago",
            "default": 1
        },
        "user_id": {
            "type": "str",
            "source": "request.args.user_id"
        },
        "tag": {
            "type": "str",
            "source": "request.args.tag"
        },
        "next_token": {
            "type": "str",
            "source": "request.next_token"
        },
        "limit": {
            "type": "int",
            "source": "request.limit",
            "default": 10
        },
        "offset": {
            "type": "int",
            "source": "request.offset",
            "default": 0
        },
    }
}


@ray.remote
class Provider(ProviderBase):
    __es_client = None
    __indices = None
    __name = None

    def __init__(self, indices=Dict, name=str, **data: Any):
        super().__init__(**data)
        self.__name = name
        if not self.__es_client:
            self.__es_client = ESClient().get_client()
        self.__indices = indices

    def get_meta(self):
        return meta

    def build_input(self, config: Dict, request: Request):
        input_dict = {}
        '''
        Get all values from request
        Then get all values from config
        Rest all values from meta
        '''
        if request.limit:
            input_dict["limit"] = request.limit
        if request.offset:
            input_dict["offset"] = request.offset
        if request.user_id:
            input_dict["user_id"] = request.user_id
        if request.args:
            for key, val in request.args.items():
                input_dict[key] = val
        for name, val in config.items():
            if name not in input_dict:
                input_dict[name] = config[name]
        for name, val in meta["args"].items():
            if name not in input_dict and name in meta["args"] and "default" in meta["args"][name]:
                input_dict[name] = meta["args"][name]["default"]
        return input_dict

    def execute(self, query):
        action_index = self.__indices["actions"]
        hits = self.__es_client.search(index=action_index, size=0, **query)
        res = hits.body["aggregations"]['top_tag_by_action']['buckets']
        '''
        returns a list of top categories.
        We then get items from each of these categories and rank by count
        '''
        items_dict = {}
        for hit in res:
            print(hit)
            for row in hit['top_action_hits']['hits']['hits']:
                item = row["_source"]
                if "item_id" in item:
                    if item["item_id"] in items_dict:
                        items_dict[item["item_id"]] = items_dict[item["item_id"]] + 1
                    else:
                        items_dict[item["item_id"]] = 1
        items_dict = dict(sorted(items_dict.items(), key=lambda item: item[1], reverse=True))
        top_items = list(items_dict.keys())
        return top_items

    def get_items(self, config: Dict, request: Request):
        '''

        :param config:
        :param request:
        :return:
        '''
        query = '''
        {
          "query": {
                "bool": {
                    "must": {
                        "term": {
                            "type.keyword": "ACTION_TYPE_PLACEHOLDER"
                        }
                    },
                    "filter": {
                        "range": {
                            "created_at": {
                                "gt": "DATE_AGO_PLACEHOLDER",
                                "lt": "DATE_NOW_PLACEHOLDER"
                            }
                        }
                    }
                }
            },
          "aggs": {
            "top_tag_by_action": {
              "terms": {
                "field": "tags.TAG_PLACEHOLDER.keyword",
                "size": LIMIT_PLACEHOLDER
              },
              "aggs": {
                "top_action_hits": {
                  "top_hits": {
                    "sort": [
                      {
                        "created_at": {
                          "order": "desc"
                        }
                      }
                    ],
                    "_source": {
                      "includes": [ "item_id", "user_id","type" , "value", "tags" ]
                    },
                    "size": ITEMS_PER_ACTION
                  }
                }
              }
            }
          }
        }
        '''
        input_dict = self.build_input(config=config, request=request)
        time_now = time_ago_to_date("now")
        time_ago = time_ago_to_date(str(input_dict["days_ago"]) + " days ago")
        query = query.replace("DATE_NOW_PLACEHOLDER", time_now)
        query = query.replace("DATE_AGO_PLACEHOLDER", time_ago)
        query = query.replace("ACTION_TYPE_PLACEHOLDER", input_dict["action_type"])
        query = query.replace("TAG_PLACEHOLDER", input_dict["tag"])
        query = query.replace("LIMIT_PLACEHOLDER", str(input_dict["limit"]))
        query = query.replace("ITEMS_PER_ACTION", str(5))
        res = json.loads(query)
        results = self.execute(res)
        return [self.__name, results]
