from models.action import Action
from models.item import Item


def load_test_items():
    items = []
    for i in range(0, 5):
        item = Item(
            id="test_items_" + str(i),
            tags={
                "category": "test_category_" + str(i),
                "source": "test_source_" + str(i)
            },
            type="LIKE",
            value=1)
        items.append(item)
    return items


def load_test_actions():
    actions = []
    for i in range(0, 5):
        action = Action(
            id="test_action_" + str(i),
            user_id="test_user" + str(i),
            item_id="test_items_" + str(i),
            tags={
                "category": "test_category_" + str(i),
                "source": "test_source_" + str(i)
            },
            type="LIKE",
            value=1)
        actions.append(action)
    return actions
