import json
import os
from os.path import exists

from typing import Dict

ALGO_FILE_NAME = "algo_spec.json"


class AlgoSpecHelper:
    __algo_spec = None
    __algo_spec_dir = None

    __recommender_name = None

    def __init__(self, recommender_name):
        self.__recommender_name = recommender_name
        self.__algo_spec_dir = (
            os.path.dirname(os.path.realpath(__file__))
            + "/repo/"
            + self.__recommender_name
            + "/"
        )
        if exists(self.__algo_spec_dir + ALGO_FILE_NAME):
            self.load()

    def load(self):
        if not self.__algo_spec:
            with open(self.__algo_spec_dir + ALGO_FILE_NAME, "r") as openfile:
                self.__algo_spec = json.load(openfile)
        return self.__algo_spec

    def set(self, algo_spec=Dict):
        if algo_spec:
            os.makedirs(os.path.dirname(self.__algo_spec_dir), exist_ok=True)
            with open(self.__algo_spec_dir + ALGO_FILE_NAME, "w") as outfile:
                json.dump(algo_spec, outfile, indent=4)
                # json_data = json.dumps(algo_spec, indent=4)
                # outfile.write(json_data)
                self.__algo_spec = algo_spec
        else:
            raise FileNotFoundError("Algo spec can not be None")
