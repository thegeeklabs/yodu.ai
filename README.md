# Yodu.ai

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
from yodu import load_test_items, load_test_actions

import yodu

yodu.init(HOST="", PORT="")

recommender = yodu.create_recommender(name="getting_started")
recommender = yodu.get_recommender(name="getting_started")

# Add Items to Recommender
items = load_test_items()
recommender.add_items(items)

# Add Actions to Recommender
actions = load_test_actions()
recommender.add_actions(items)

# Enable Yodu's built-in Providers
recommender.enable_provider(name="TopItemsByUserAction")

# Add provider from Source (Coming Soon)
recommender.add_provider(name="CUSTOM_PROVIDER",
                         source="https://github.com/thegeeklabs/yodu.ai/tree/dev/src/yodu/provider/some_dir")
recommender.enable_provider(name="CUSTOM_PROVIDER")

algo_spec = {
  "TOP_BY_PREVIOUS_LIKED_SOURCES": {
    "provider": "TopItemsByUserAction",
    "duration": "24h",
    "config": {
      "action_type": "LIKE",
      "tag": "source"
    },
    "weight": 1
  },
  "TOP_BY_PREVIOUS_LIKED_CATEGORIES": {
    "provider": "TopItemsByUserAction",
    "duration": "30h",
    "config": {
      "action_type": "LIKE",
      "tag": "category"
    },
    "weight": 1
  },
  "TOP_BY_PREVIOUS_READ_CATEGORIES": {
    "provider": "TopItemsByUserAction",
    "duration": "30h",
    "config": {
      "action_type": "READ",
      "tag": "category"
    },
    "weight": 1
  },
  "TOP_BY_PREVIOUS_READ_CATEGORIES": {
    "provider": "CUSTOM_PROVIDER",
    "duration": "30h",
    "config": {
      "action_type": "READ",
      "tag": "category"
    },
    "weight": 1
  }
}
recommender.add_algo_spec(name="first_algo_spec", config=algo_spec)

items = recommender.get_items(user_id="1", algo_spec="first_algo_spec")
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