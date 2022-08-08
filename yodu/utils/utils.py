import datetime
import os
import shutil

import dateparser


def time_ago_to_date(time_ago_str):
    if time_ago_str == "now":
        date = datetime.datetime.now()
    else:
        date = dateparser.parse(time_ago_str)
    date = date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return date


def move_dir(base_dir, source_dir, destination_dir):
    # fetch all files
    source_dir = base_dir + "/" + source_dir
    destination_dir = base_dir + "/" + destination_dir
    os.makedirs(os.path.dirname(destination_dir), exist_ok=True)
    try:
        # Delete provider if exists
        shutil.rmtree(destination_dir)
    except:
        pass
    shutil.copytree(source_dir, destination_dir)
