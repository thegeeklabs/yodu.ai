import json
from datetime import datetime

from yodu.models.action import Action

steemit_blockchain_path = (
    "/Users/shashank/PycharmProjects/test_yodu/data/steem.blockchain.json"
)

"""
['vote', {'author': 'playhighcard', 'permlink': 'shb-1658613843533-e278a173-2b5d-49eb-915f-ac239435e526', 'voter': 'wking-chili', 'weight': 10000}]
"""


def vote_to_action(vote_dict):
    pass


def read_lens_data_es(data_file):
    i = 0
    real_count = 0
    count = 0
    points = []
    skipped = 0
    batches = {}
    total_time = 0
    with open(data_file, "r") as f:
        for line in f:
            data = json.loads(line)
            if "op" in data and len(data["op"]) > 0:
                operation = data["op"]
                action_type = operation[0]
                "2022-07-31T03:34:48"
                t = data["timestamp"]
                time_stamp = datetime.strptime(
                    t, "%Y-%m-%dT%H:%M:%S"
                ).isoformat()
                if action_type in ["comment", "vote"]:
                    """if there is no parent_author then it is a post/Item othwerise it is a comment"""
                    if operation[1]["parent_author"] != "":
                        props = operation[1]
                        item_id = props["permlink"]
                        user_id = props["author"]
                        id = user_id + "_" + item_id
                        """
                            id: str = Field(default_factory=uuid4)
                            item_id: str
                            user_id: str
                            type: str
                            value: float
                            tags: Optional[Dict]
                            created_at: datetime = Field(default_factory=datetime.now)
                        """
                        action = Action(
                            id=id,
                            user_id=user_id,
                            item_id=item_id,
                            value=1,
                            tags=props,
                            type=action_type,
                            created_at=time_stamp,
                        )
                        action_dict = action.dict()
                        print(action_dict)
                    else:
                        print("Not a comment")
                else:
                    print(operation)

            else:
                print(data)


read_lens_data_es(steemit_blockchain_path)
