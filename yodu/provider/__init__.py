import os
import shutil

current_dir = os.path.dirname(os.path.realpath(__file__))


def move_dir(source_dir, destination_dir):
    # fetch all files
    source_dir = current_dir + "/" + source_dir
    destination_dir = current_dir + "/" + destination_dir
    os.makedirs(os.path.dirname(destination_dir), exist_ok=True)
    try:
        # Delete provider if exists
        shutil.rmtree(destination_dir)
    except:
        pass
    shutil.copytree(source_dir, destination_dir)


def add(recommender_name: str, name: str):
    '''
    Move from repo to recommender provider repo
    repo/recommender_name/enabled
    '''
    plugin_dir = "providers/" + name + "/"
    destination_dir = "repo/" + recommender_name + name
    move_dir(plugin_dir, destination_dir)


def get_providers(recommender_name: str):
    '''
    Get list of all providers in the enabled repo
    :return:
    '''
    pass


def remove(recommender_name: str, provider_name: str):
    '''
    Move from enabled to repo
    :return:
    '''
    pass


def delete_provider():
    '''
    Check if provider_no_enabled
    Delete from repo
    :return:
    '''
    pass
