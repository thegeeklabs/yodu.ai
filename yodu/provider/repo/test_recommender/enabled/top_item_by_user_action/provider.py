import json
from typing import Optional

from yodu.provider.provider_base import ProviderBase
from yodu.recommeder.db.influx_db import InfluxDb
from yodu.utils.utils import time_ago_to_date

meta = {
    "name": "TopItemsByUserAction",
    "author": "Shashank Agarwal",
    "description": "Return top items for a source by action_type \
        Example: Return top liked items for a given source \
        Example: Return top read items for a given source \
        Example: Return top read items for a given category",
    "args": {
        "action_type": {
            "type": "str",
            "source": "request.action_type"
        },
        "days_ago": {
            "type": "int",
            "source": "request.days_ago",
            "default": 1
        },
        "user_id": {
            "type": "str",
            "source": "request.user_id"
        },
        "tag": {
            "type": "str",
            "source": "request.tag"
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


class TopItemsByUserAction(ProviderBase):
    action_type: Optional[str]
    tag: Optional[str]
    user_id: Optional[str]
    next_token: Optional[str]
    __influx_db_client = InfluxDb().get_client()

    def init(self, kwargs):
        if "action_type" in kwargs:
            self.action_type = kwargs["action_type"]
        if "tag" in kwargs:
            self.tag = kwargs["tag"]
        if "User_id" in kwargs:
            self.user_id = kwargs["user_id"]
        if "next_token" in kwargs:
            self.next_token = kwargs["next_token"]

    # def build_input_args(self, request):
    #     args = {}
    #     args_meta = meta["args"]
    #     for arg in args_meta:


    def get_items(self, request):
        '''
        Returns top tag for all items by action_type
        Ex: Top sources by likes
        :param days_ago:
        :param action_type:
        :param tag:
        :param limit:
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
                      "includes": [ "value","type","tags" ]
                    },
                    "size": ITEMS_PER_ACTION
                  }
                }
              }
            }
          }
        }
        '''
        time_now = time_ago_to_date("now")
        time_ago = time_ago_to_date(str(days_ago) + " days ago")
        query = query.replace("DATE_NOW_PLACEHOLDER", time_now)
        query = query.replace("DATE_AGO_PLACEHOLDER", time_ago)
        query = query.replace("ACTION_TYPE_PLACEHOLDER", action_type)
        query = query.replace("TAG_PLACEHOLDER", tag)
        query = query.replace("LIMIT_PLACEHOLDER", str(limit))
        query = query.replace("ITEMS_PER_ACTION", str(2))
        res = json.loads(query)
        return res
