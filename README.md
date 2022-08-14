# Yodu.ai

[![PyPI version](https://badge.fury.io/py/yodu.svg)](https://badge.fury.io/py/yodu)

A generic purpose Recommender System that can be configured for any UseCase.
ExampleUseCase:

- Social Platforms
- Ecommerce Websites
- Video Portals
- News Aggregator Websitesx

If you want to contribute just email me at shashank[at]yodu.ai . Happy to share DB and other access.

## Learn more:

- [Documentation](https://github.com/thegeeklabs/yodu.ai/tree/dev/docs)
    - [About Yodu.ai](https://github.com/thegeeklabs/yodu.ai/blob/dev/docs/ABOUT.md)
    - [Algorithm](https://github.com/thegeeklabs/yodu.ai/blob/dev/docs/ALGORITHM.md)
    - [Modules](https://github.com/thegeeklabs/yodu.ai/blob/dev/docs/MODULES.md)
- [TODO_list](https://github.com/thegeeklabs/yodu.ai/blob/dev/docs/TO_DO.md)
- [Contribution Guidelines](https://github.com/thegeeklabs/yodu.ai/blob/dev/CONTRIBUTING.md)
    - [CODE_OF_CONDUCT](https://github.com/thegeeklabs/yodu.ai/blob/dev/CODE_OF_CONDUCT.md)
    - [Issues](https://github.com/thegeeklabs/yodu.ai/blob/dev/docs/contributing/issues.md)
- [LICENSE](https://github.com/thegeeklabs/yodu.ai/blob/dev/LICENSE)

# Getting Started:

## Install Yodu Library

    pip install yodu

## Configure Yodu

Yodu uses ElasticSearch as the default backend.
You must define these environment variables.

```shell
ES_HOST=<ELASTICSEARCH_HOST>
ES_USER=<ELASTICSEARCH_USER>
ES_PASSWORD=<ELASTICSEARCH_PASSWORD>
```

### Interacting with Yodu Recommendation Engine

## Create a Recommender

This will create various indexes required by the recommender.

    recommender = yodu.create_recommender(name="example")

## Load a recommender by Name

This will load the various indexes related to the recommender and also the algo_spec
if it was previously created for this recommender.

    recommender = yodu.get_recommender(name="example")

## Add Items to recommender

Represent the item that is recommended.
Example: Youtube video, ecommerce product, Article, Post etc.

Each Item must have a "source" which can be a User or a type Source

```python
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


items = load_test_items()
recommender.item.add(items)
```

## Add Actions to recommender

Action represent interactions between Users & Items. Actions are the primary indicator on how to rank, score items.
Example: LIKE, COMMENT, READ etc.

```python
def load_test_actions():
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


actions = load_test_actions()
recommender.action.add(actions)
```

## Enable a Provider

You use one of the built-in providers or add your own providers.
`top_item_by_user_action` is a built-in provider that returns top items by a user action.

For example: We can configure this provider to `get top items from top liked categories`
The Provider will first calculate top categories for the given user based on past likes by that user,
then it gets top items based on global likes by all users for each of those categories.
Finally, the provider will aggregate all items returned from all categories and return
the top most recommended items.

```python
# Enable Yodu's built-in Providers
recommender.provider.add(name="top_item_by_user_action")
```

## Add Algorithm Specification

The algorithm specification defines what providers the recommender must use
to generate recommendations.

In this example, the recommender will call each provider in parallel with the given configuration.
Finally, it de-duplicates and aggregates all items and orders them based on how many times an item was recommended by
the
given list of providers in the algo_spec.

Lastly, it will filter items based on past user interaction with the item (i.e if a user has performed some action to a
given item). So if a user has already performed a "READ" action for an item, the recommender can filter out these items.

```python

algo_spec = {
    "providers": {
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
    },
    "filters": {
        "PAST_ACTION": {
            "provider": "get_past_user_item_action",
            "description": "Filter items if a user has performed any action on the item",
            "duration": "24h",
            "config": {"action_type": "ALL"},
        },
    }
}
recommender.algo_spec.set(algo_spec=algo_spec)
```

## Get recommendations based on the Algorithm Specification

```python
args = {
    "days_ago": "7"
}
request = Request(user_id="test_user_1", args=args)

items = recommender.get_items(request=request)
```

# Full Example

```python
import yodu
from examples.steem.helpers import load_test_items, load_test_actions
from models.request import Request

recommender = yodu.create_recommender(name="example")
recommender = yodu.get_recommender(name="example")

# Add Items to Recommender
items = load_test_items()
recommender.item.add(items)

# Add Actions to Recommender
actions = load_test_actions()
recommender.action.add(actions)

# Enable Yodu's built-in Providers
recommender.provider.add(name="top_item_by_user_action")
# Add provider from Source (Coming Soon)

algo_spec = {
    "providers": {
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
    },
    "filters": {
        "PAST_ACTION": {
            "provider": "get_past_user_item_action",
            "description": "Filter items if a user has performed any action on the item",
            "duration": "24h",
            "config": {"action_type": "ALL"},
        },
    }
}
recommender.algo_spec.set(algo_spec=algo_spec)

args = {
    "days_ago": "7"
}
request = Request(user_id="test_user_1", args=args)

items = recommender.get_items(request=request)
```

# Coming Soon

## Deploying the Server

### Deploying a Yodu Recommendation Server(With ElasticSearch)

```
git clone <repo>
cd yodu
kubectl deploy <coming_soon>
```

### Deploying a Yodu Recommendation Server(Using your own ElasticSearch)

```
git clone <repo>
cd yodu
kubectl deploy <coming_soon>
```
