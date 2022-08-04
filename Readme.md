# Yodu.ai

A generic purpose Recommender System that can be configured for any UseCase.
ExampleUseCase:
- Social Platforms
- Ecommerce Websites
- Video Portals
- News Aggregator Websites

If you want to contribute just send me an email at shashank[at]thegeeklabs.com. Happy to share DB and other access.

# TODO list
- Add APIs for add_action
- Add APIs for add_item
- Add APIs for add_source
- Add APIs for add_follow
- Add ElasticSearch to Indexer


## TODO:
- Add APIs to add items
- ADD Search by popularity
- Add Follow action

## Modules:

- Recommender
- Providers
- Scheduler
- MLAgent
- Search/Query Engine

### Providers
User Specific
- Top items by top actions by user.
    - Example: Get items based on items from sources liked by user
      - Get top liked categories by user
      - Options:
        - [Latest] Get top articles(based on same action) from these categories
        - [Ranked BY Action] 
- Trending items by a tag
  - Trending is calculated by Linear Regression
  - Example:
    - Trending items in source "X" by likes
- Top items from sources followed by User
- Similar items liked by other users
  - Used Matrix Multiplication to find similar items liked by similar users
