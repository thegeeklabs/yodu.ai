from typing import Optional

from yodu.provider.provider_base import ProviderBase
from yodu.recommeder.db.influx_db import InfluxDb


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
