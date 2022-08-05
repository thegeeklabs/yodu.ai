import datetime

import dateparser


def time_ago_to_date(time_ago_str):
    if time_ago_str == "now":
        date = datetime.datetime.now()
    else:
        date = dateparser.parse(time_ago_str)
    date = date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return date
