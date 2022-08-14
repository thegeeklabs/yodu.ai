import json
from typing import Dict, Any

import ray

from yodu import ESClient
from yodu.models.request import Request
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
    "props": {
        "action_type": {"type": "str", "source": "request.props.action_type"},
        "days_ago": {
            "type": "int",
            "source": "request.props.days_ago",
            "default": 1,
        },
        "user_id": {"type": "str", "source": "request.props.user_id"},
        "tag": {"type": "str", "source": "request.props.tag"},
        "next_token": {"type": "str", "source": "request.next_token"},
        "limit": {"type": "int", "source": "request.limit", "default": 10},
        "offset": {"type": "int", "source": "request.offset", "default": 0},
    },
}


@ray.remote
class Provider(ProviderBase):
    __es_client = None
    __indices = None
    __name = None
    __meta = None

    def __init__(self, indices=Dict, name=str, **data: Any):
        super().__init__(meta=meta, data=data)
        self.__name = name
        if not self.__es_client:
            self.__es_client = ESClient()
        self.__indices = indices
        self.__meta = meta

    def get_items(self, config: Dict, request: Request):
        """
        :param config:
        :param request:
        :return:
        """
        query = """
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
                "field": "props.TAG_PLACEHOLDER.keyword",
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
                      "includes": [ "item_id", "user_id","type" , "value", "props" ]
                    },
                    "size": ITEMS_PER_ACTION
                  }
                }
              }
            }
          }
        }
        """
        input_dict = self.build_input(config=config, request=request)
        time_now = time_ago_to_date("now")
        time_ago = time_ago_to_date(str(input_dict["days_ago"]) + " days ago")
        query = query.replace("DATE_NOW_PLACEHOLDER", time_now)
        query = query.replace("DATE_AGO_PLACEHOLDER", time_ago)
        query = query.replace(
            "ACTION_TYPE_PLACEHOLDER", input_dict["action_type"]
        )
        query = query.replace("TAG_PLACEHOLDER", input_dict["tag"])
        query = query.replace("LIMIT_PLACEHOLDER", str(input_dict["limit"]))
        query = query.replace("ITEMS_PER_ACTION", str(5))
        res = json.loads(query)
        results = self.execute(
            es_client=self.__es_client, indices=self.__indices, query=res
        )
        return [self.__name, results]
