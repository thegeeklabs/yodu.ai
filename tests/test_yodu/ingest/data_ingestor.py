import datetime
import logging
import random
import threading
import time
from datetime import datetime

import ijson
from elasticsearch import helpers
from influxdb_client import Point, WritePrecision
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import ASYNCHRONOUS

from yodu import settings
from yodu.db.es.es_client import ESClient
from yodu.models.action import Action
from yodu.recommeder.db.influx_db import InfluxDb

logger = logging.getLogger(__name__)

steemit_blockchain_path = (
    "/Users/shashank/PycharmProjects/test_yodu/data/steem.blockchain.json"
)


class Indexer:
    __es_client = None
    __influxdb_client = None

    def add_items(self, items: list):
        return self.__es_client.add_records(items)

    def add_users(self, users):
        return self.__es_client.add_records(users)

    def add_actions(self, actions: list):
        return self.__es_client.add_actions(actions)


def create_sample_actions():
    actions = []
    for i in range(0, 100000):
        rand_user = random.randint(0, 100)
        rand2 = random.randint(-1, 1)
        rand3 = random.randint(0, 10)
        rand4 = random.randint(0, 10)
        rand = random.randint(0, 100)
        action = Action(
            item_id=rand,
            user_id=rand_user,
            type="READ",
            value=rand2,
            tags={
                "source": "test" + str(rand3),
                "category": "test" + str(rand4),
            },
        )
        actions.append(action)
    return actions


def action_to_point(action: Action):
    point = (
        Point(action.type)
        .field(action.type, action.value)
        .time(action.created_at, WritePrecision.MS)
    )
    point.tag("user_id", action.user_id)
    point.tag("item_id", action.item_id)
    for key, value in action.props.items():
        point.tag(key, value)
    return point


def write_points(points):
    client = InfluxDb(bucket="lens").get_client()
    try:
        client.write_api(write_options=ASYNCHRONOUS).write(
            bucket="lens", org=settings.INFLUX_DB_ORG, record=points
        )
    except InfluxDBError as e:
        print(e)
        if e.response.status == 401:
            raise Exception(
                f"Insufficient write permissions to 'my-bucket'."
            ) from e
        raise
    client.close()


es_client = ESClient().get_client()


def add_items_to_es(docs):
    def doc_generator(df):
        for document in df:
            yield {
                "_index": "lens",
                "_source": document,
            }

    helpers.bulk(es_client, doc_generator(docs))
    # response = client.bulk(index='lens', body=docs)


def ingest_items(actions):
    rand_days = random.randint(0, 48)
    write_time = datetime.datetime.utcnow() - datetime.timedelta(
        hours=rand_days
    )
    for action in actions:
        point = (
            Point(action.type)
            .field(action.type, action.value)
            .time(write_time, WritePrecision.MS)
        )
        point.tag("user_id", action.user_id)
        point.tag("item_id", action.item_id)
        for key, value in action.props.items():
            point.tag(key, value)


thread_count = 10
max_batch_size = 1000
batch_size = max_batch_size * thread_count


def read_lens_data_es():
    i = 0
    real_count = 0
    count = 0
    points = []
    skipped = 0
    batches = {}
    total_time = 0
    with open(
        "/Users/shashank/PycharmProjects/yodu/data/lens-notifications.json",
        "rb",
    ) as f:
        for record in ijson.items(f, "item"):
            message = record["Message"]["data"]
            type = record["Message"]["type"]
            if "profileId" in message and "pubId" in message:
                profile_id = message["profileId"]
                pub_id = message["pubId"]

                tags = {}
                if (
                    "timestamp" in message
                    and "$numberLong" in message["timestamp"]
                ):
                    t = int(message["timestamp"]["$numberLong"]) / 1000
                    time_stamp = datetime.fromtimestamp(t).isoformat()
                else:
                    t = record["Timestamp"]
                    time_stamp = datetime.strptime(
                        t, "%Y-%m-%dT%H:%M:%S.%fZ"
                    ).isoformat()
                for key, value in message.items():
                    if key != "timestamp":
                        tags[key] = value
                id = record["_id"]["$oid"]
                action = Action(
                    id=id,
                    item_id=pub_id,
                    user_id=profile_id,
                    tags=tags,
                    value=1,
                    type=type,
                    created_at=time_stamp,
                )
                action_dict = action.dict()
                action_dict["_id"] = action.id
                current_index = i % thread_count
                if current_index not in batches:
                    batches[current_index] = []
                batches[current_index].append(action_dict)
                i = i + 1
                count = count + 1
            else:
                skipped = skipped + 1
            if i >= batch_size:
                start = time.time()
                process_batches(batches)
                end = time.time()
                total_time = total_time + (end - start)
                total_average = count / total_time
                speed = (max_batch_size * thread_count) / (end - start)
                print("Docs:" + str(max_batch_size * thread_count))
                print("Total time:" + str(end - start))
                print("Speed: " + str(speed) + "/second")
                print("Total Average: " + str(total_average))
                i = 0
                batches = {}
                print("Processed: " + str(count) + "\n")
            real_count = real_count + 1
        write_points(points)


def read_lens_data():
    i = 0
    real_count = 0
    count = 0
    points = []
    skipped = 0
    batches = {}
    total_time = 0
    with open(
        "/Users/shashank/PycharmProjects/yodu/data/lens-notifications.json",
        "rb",
    ) as f:
        for record in ijson.items(f, "item"):
            message = record["Message"]["data"]
            type = record["Message"]["type"]
            if "profileId" in message and "pubId" in message:
                profile_id = message["profileId"]
                pub_id = message["pubId"]

                tags = {}
                if (
                    "timestamp" in message
                    and "$numberLong" in message["timestamp"]
                ):
                    t = int(message["timestamp"]["$numberLong"]) / 1000
                    time_stamp = datetime.fromtimestamp(t).isoformat()
                else:
                    t = record["Timestamp"]
                    time_stamp = datetime.strptime(
                        t, "%Y-%m-%dT%H:%M:%S.%fZ"
                    ).isoformat()
                for key, value in message.items():
                    if key != "timestamp":
                        tags[key] = value
                id = record["_id"]["$oid"]
                action = Action(
                    id_=id,
                    item_id=pub_id,
                    user_id=profile_id,
                    tags=tags,
                    value=1,
                    type=type,
                    created_at=time_stamp,
                )
                point = action_to_point(action)
                current_index = i % thread_count
                if current_index not in batches:
                    batches[current_index] = []
                batches[current_index].append(point)
                i = i + 1
                count = count + 1
            else:
                skipped = skipped + 1
            if i >= batch_size:
                start = time.time()
                process_batches(batches)
                end = time.time()
                total_time = total_time + (end - start)
                total_average = count / total_time
                speed = (max_batch_size * thread_count) / (end - start)
                print("Docs:" + str(max_batch_size * thread_count))
                print("Total time:" + str(end - start))
                print("Speed: " + str(speed) + "/second")
                print("Total Average: " + str(total_average))
                i = 0
                batches = {}
                print("Processed: " + str(count) + "\n")
            real_count = real_count + 1
        write_points(points)


def process_batches(batches):
    threads_list = list()
    for key, b in batches.items():
        x = threading.Thread(target=add_items_to_es, args=(b,))
        x.start()
        threads_list.append(x)
    for t in threads_list:
        t.join()
        print("Waiting for thread")


read_lens_data_es()


def ingest_actions():
    pass
