from influxdb_client import InfluxDBClient

from yodu import settings


class InfluxDb:
    client = None
    bucket = "bridgeml"

    def __init__(self, bucket="bridgeml"):
        self.bucket = bucket

    def get_client(self):
        if not self.client:
            self.client = InfluxDBClient(
                url=settings.INFLUX_DB_HOST,
                port=8086,
                username=settings.INFLUX_DB_USER,
                password=settings.INFLUX_DB_PASSWORD,
                ssl=settings.INFLUX_USE_SSL,
                verify_ssl=settings.INFLUX_USE_VERIFY_SSL,
            )
        return self.client

    def get_query_api(self):
        return self.get_client().query_api()

    def top_items_by_source(
        self, days_ago, action_type, tag_type, source, limit=5
    ):
        """
        Return top items for a source by action_type
        Example: Return top liked items for a given source
        Example: Return top read items for a given source
        Example: Return top read items for a given category
        :param days_ago:
        :param action_type:
        :param source:
        :param limit:
        :return:
        """
        query = (
            'from(bucket: "bridgeml")\
        |> range(start: -'
            + str(days_ago)
            + 'd)\
        |> filter(fn: (r) => r["_measurement"] == "'
            + action_type
            + '")\
        |> filter(fn: (r) => r["'
            + tag_type
            + '"] == "'
            + source
            + '")\
        |> group(columns: ["item_id"])\
        |> aggregateWindow(every: '
            + str(days_ago)
            + 'd, fn: sum, createEmpty: false)\
        |> group()\
        |> sort(columns: ["_value"], desc: true)\
        |> top(n: '
            + str(limit)
            + ")"
        )
        res = self.get_query_api().query(org="influxdata", query=query)
        records = res[0].records
        top = {}
        for record in records:
            values = record.values
            top[values["item_id"]] = values["_value"]
        return top

    def top_by_user_action(self, days_ago, action_type, tag, user_id, limit=5):
        """
        Returns top tag for a user by action_type
        Ex: Top sources liked by the user
        Ex: Top categories liked by the user
        :param days_ago:
        :param action_type:
        :param tag:
        :param user_id:
        :param limit:
        :return:
        """
        query = (
            'from(bucket: "bridgeml")\
            |> range(start: -'
            + str(days_ago)
            + 'd)\
            |> filter(fn: (r) => r["_measurement"] == "'
            + action_type
            + '")\
            |> filter(fn: (r) => r["user_id"] == "'
            + str(user_id)
            + '")\
            |> group(columns: ["'
            + tag
            + '"])\
            |> aggregateWindow(every: '
            + str(days_ago)
            + 'd, fn: sum, createEmpty: false)\
            |> group()\
            |> sort(columns: ["_value"], desc: true) \
            |> top(n: '
            + str(limit)
            + ")"
        )
        res = self.get_query_api().query(org="influxdata", query=query)
        records = res[0].records
        top = {}
        for record in records:
            values = record.values
            top[values[tag]] = values["_value"]
        return top

    def top_by_action(self, days_ago, action_type, tag, limit=5):
        """
        Returns top tag for all items by action_type
        Ex: Top sources by likes
        :param days_ago:
        :param action_type:
        :param tag:
        :param limit:
        :return:
        """
        query = (
            'from(bucket: "bridgeml")\
            |> range(start: -'
            + str(days_ago)
            + 'd)\
            |> filter(fn: (r) => r["_measurement"] == "'
            + action_type
            + '")\
            |> group(columns: ["'
            + tag
            + '"])\
            |> aggregateWindow(every: '
            + str(days_ago)
            + 'd, fn: sum, createEmpty: false)\
            |> group()\
            |> sort(columns: ["_value"], desc: true) \
            |> top(n: '
            + str(limit)
            + ")"
        )
        res = self.get_query_api().query(org="influxdata", query=query)
        records = res[0].records
        top = {}
        for record in records:
            values = record.values
            top[values[tag]] = values["_value"]
        return top
