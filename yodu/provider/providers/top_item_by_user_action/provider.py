import json
from typing import Optional

from yodu.provider.provider_base import ProviderBase
from yodu.recommeder.db.influx_db import InfluxDb
from yodu.utils.utils import time_ago_to_date


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

    def get_items(self, config):
        """
        - Get action sorted by "tag" type
        - Get items wich same "tag" type
        :param action_type:
        :param user_id:
        :return:
        """
        self.init(config)

        print(self.action_type)
        print(self.tag)
        print(self.user_id)
        print(self.next_token)
        return {}

    def top_items_by_source(self, days_ago, action_type, tag_type, source, limit=5):
        '''
        Return top items for a source by action_type
        Example: Return top liked items for a given source
        Example: Return top read items for a given source
        Example: Return top read items for a given category
        :param days_ago:
        :param action_type:
        :param source:
        :param limit:
        :return:
        '''
        pass

    def top_by_action(self, days_ago, action_type, tag, limit=5):
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
