from models.action import Action
from models.item import Item


def load_test_items():
    '''
    Create items with IDS: items0, item2...items99
    With categories ranging from category0...category9
    With source ranging from source0,...source9
    :return:
    '''
    items = []
    for i in range(0, 100):
        item = Item(
            id="item" + str(i),
            source="source" + str(i % 10),
            tags={
                "category": "category" + str(i % 10),
                "source": "source" + str(i % 10)
            })
        items.append(item)
    return items


def load_test_actions():
    actions = []
    for i in range(0, 100):
        action = Action(
            id="action" + str(i),
            user_id="user" + str(i % 10),
            item_id="item" + str(i),
            tags={
                "category": "category" + str(i % 10),
                "source": "source" + str(i % 10),
            },
            type="LIKE",
            value=1)
        actions.append(action)
    for i in range(0, 100):
        action = Action(
            id="action" + str(i),
            user_id="user" + str(i % 10),
            item_id="item" + str(i),
            tags={
                "category": "category" + str(i % 10),
                "source": "source" + str(i % 10),
            },
            type="READ",
            value=1)
        actions.append(action)
    return actions
