import datetime
import random

from influxdb_client import Point, WritePrecision
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS

from yodu import settings
from yodu.models.action import Action
from yodu.recommeder.db.influx_db import InfluxDb


class Indexer:
    __es_client = None
    __influxdb_client = None

    def add_items(self, items):
        return self.__es_client.add_records(items)

    def add_users(self, users):
        return self.__es_client.add_records(users)

    def add_actions(self, actions):
        return self.__es_client.add_actions(actions)


def create_sample_actions():
    actions = []
    for i in range(0, 100000):
        rand_user = random.randint(0, 100)
        rand2 = random.randint(-1, 1)
        rand3 = random.randint(0, 10)
        rand4 = random.randint(0, 10)
        rand = random.randint(0, 100)
        action = Action(item_id=rand,
                        user_id=rand_user,
                        type="READ",
                        value=rand2,
                        tags={
                            "source": "test" + str(rand3),
                            "category": "test" + str(rand4)
                        }
                        )
        actions.append(action)
    return actions


def ingest_items(actions):
    client = InfluxDb().get_client()
    points = []
    rand_days = random.randint(0, 48)
    write_time = datetime.datetime.utcnow() - datetime.timedelta(hours=rand_days)
    for action in actions:
        point = Point(action.type) \
            .field(action.type, action.value) \
            .time(write_time, WritePrecision.MS)
        point.tag("user_id", action.user_id)
        point.tag("item_id", action.item_id)
        for key, value in action.tags.items():
            point.tag(key, value)
        points.append(point)
    try:
        client.write_api(write_options=SYNCHRONOUS).write(bucket=settings.INFLUX_DB_BUCKET,
                                                          org=settings.INFLUX_DB_ORG,
                                                          record=points)
    except InfluxDBError as e:
        print(e)
        if e.response.status == 401:
            raise Exception(f"Insufficient write permissions to 'my-bucket'.") from e
        raise
    client.close()


def read_lens_data():
    import ijson
    from datetime import datetime

    with open("/Users/shashank/PycharmProjects/yodu/data/lens-notifications.json", "rb") as f:
        for record in ijson.items(f, "item"):
            print(record)
            message = record["Message"]["data"]
            type = record["Message"]["type"]
            if "profileId" in message and "pubId" in message:
                profile_id = message["profileId"]
                pub_id = message["pubId"]

                tags = {}
                if "timestamp" in message and '$numberLong' in message["timestamp"]:
                    t = int(message["timestamp"]['$numberLong']) / 1000
                    time_stamp = datetime.fromtimestamp(t).isoformat()
                else:
                    t = record["Timestamp"]
                    time_stamp = datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat()
                for key, value in message.items():
                    tags[key] = value
                action = Action(item_id=pub_id, user_id=profile_id, tags=tags, value=1, type=type,
                                created_at=time_stamp)
                print(action)
            else:
                print("Skipping")
                print(record)


read_lens_data()


def ingest_actions():
    pass
