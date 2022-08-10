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

## Creating your first recommendation engine.

    pip install yodu

### Interacting with Yodu Recommendation Engine

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
    "TOP_BY_PREVIOUS_LIKED_SOURCES": {
        "provider": "top_item_by_user_action",
        "duration": "24h",
        "config": {
            "action_type": "LIKE",
            "tag": "source"
        },
        "weight": 1
    },
    "TOP_BY_PREVIOUS_LIKED_CATEGORIES": {
        "provider": "top_item_by_user_action",
        "duration": "30h",
        "config": {
            "action_type": "LIKE",
            "tag": "category"
        },
        "weight": 1
    },
    "TOP_BY_PREVIOUS_READ_CATEGORIES": {
        "provider": "top_item_by_user_action",
        "duration": "30h",
        "config": {
            "action_type": "READ",
            "tag": "category"
        },
        "weight": 1
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