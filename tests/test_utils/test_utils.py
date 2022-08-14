from models.action import Action
from models.item import Item


def load_test_items():
    """
    Create items with IDS: items0, item2...items99
    With categories ranging from category0...category9
    With source ranging from source0,...source9
    :return:
    """
    items = []
    for i in range(0, 100):
        item = Item(
            id="item" + str(i),
            source="source" + str(i % 10),
            props={
                "category": "category" + str(i % 10),
                "source": "source" + str(i % 10),
            },
        )
        items.append(item)
    return items

'''
"TOP_BY_PREVIOUS_LIKED_SOURCES": {
            "provider": "top_item_by_user_action",
            "description": "Get top items from past top liked sources",
            "duration": "24h",
            "config": {"action_type": "LIKE", "tag": "source"},
            "weight": 1,
        },
        "TOP_BY_PREVIOUS_LIKED_CATEGORIES": {
            "provider": "top_item_by_user_action",
            "description": "Get top items from past top liked categories",
            "duration": "30h",
            "config": {"action_type": "LIKE", "tag": "category"},
            "weight": 1,
        },
        "TOP_BY_PREVIOUS_READ_CATEGORIES": {
            "provider": "top_item_by_user_action",
            "description": "Get top items from past top READ categories",
            "duration": "30h",
            "config": {"action_type": "READ", "tag": "category"},
            "weight": 1,
        },
        
'''
def load_test_actions():
    '''
    Actions to create:
    Top previous liked source
    source9
    source8

    top previous liked category
    category7
    category6

    top previous read category
    category1
    category2


    :return:
    '''

    # Create random actions
    actions = []
    for i in range(0, 100):
        action = Action(
            id="action" + str(i),
            user_id="user" + str(i % 10),
            item_id="item" + str(i),
            props={
                "category": "category" + str(i % 10),
                "source": "source" + str(i % 10),
            },
            type="LIKE",
            value=1,
        )
        actions.append(action)
    # Like source9 20 times
    # Like source8 15 times
    for i in range(0, 20):
        action = Action(
            id="like_source_9_action" + str(i),
            user_id="user" + str(i % 10),
            item_id="item" + str(i),
            props={
                "source": "source9",
            },
            type="LIKE",
            value=1,
        )
        actions.append(action)

    for i in range(0, 15):
        action = Action(
            id="like_source_8_action" + str(i),
            user_id="user" + str(i % 10),
            item_id="item" + str(i),
            props={
                "source": "source8",
            },
            type="LIKE",
            value=1,
        )
        actions.append(action)


    for i in range(0, 100):
        action = Action(
            id="action" + str(i),
            user_id="user" + str(i % 10),
            item_id="item" + str(i),
            props={
                "category": "category" + str(i % 10),
                "source": "source" + str(i % 10),
            },
            type="READ",
            value=1,
        )
        actions.append(action)
    return actions
