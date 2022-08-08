import importlib
import os

from utils.utils import move_dir


class ProviderHelper:
    __recommender_name = None
    __provider_dir = None

    def __init__(self, recommender_name):
        self.__recommender_name = recommender_name
        self.__provider_dir = os.path.dirname(os.path.realpath(__file__))

    def add(self, name: str):
        '''
        Move from repo to recommender provider repo
        repo/recommender_name/enabled
        '''
        plugin_dir = "providers/" + name + "/"
        destination_dir = "repo/" + self.__recommender_name + "/" + name
        move_dir(self.__provider_dir, plugin_dir, destination_dir)

    def load_provider(self, name: str):
        print(self.__provider_dir)
        # import yodu.provider.repo.getting_started.top_item_by_user_action.provider
        provider_path = "yodu.provider.repo.getting_started." + name + ".provider"

        mod = importlib.import_module(provider_path)
        mod = getattr(mod, "Provider")
        return mod

    def remove(self, recommender_name: str, provider_name: str):
        '''
        Move from enabled to repo
        :return:
        '''
        pass

    def delete_provider(self):
        '''
        Check if provider_no_enabled
        Delete from repo
        :return:
        '''
        pass
