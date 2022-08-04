Yodu.ai is built using the concept of providers.

## Provider
A provider can take n number or arguments and returns a list of `items` based on various logic.

## Algorithm Specification
Yodu allows the users to specify as multiple Algorithms that the feed must adhere to use, using a configration file 
called as `algo_spec`. 
An Algo Specification lists a number of providers that are called in parallel to get a list of items.
You can provide weights to each Provider to make a provider returns more `items` than other providers, If no weights
are given then all Providers get a uniform weight.

## Algorithms for Recommendation Engine
- Call recommender with a user_id
- Recommender loads the given algo_spec and gets a list of Providers
- Each Provider is asked for items concurrently
- Recommender waits for X seconds, then makes a final list.
- Based on algo_spec, Recommender then filters, sorts & cleans up the list.
- The list is then returned to the user.
- Each request must specif `offset` & `limit`. These values are passed to each provider.

## Auto-balancing Recommder System
To make the items are specific to each user. Yodu calculates a user_meta. This user_meta contains stats on which
providers were more liked by the user than others. The recommender system then use this meta to adjust the weights of
the providers.

## Type of Providers
Yodu comes with a set of default providers, which are described below.

- User Specific
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

## ML
Similar to other Providers, ML providers are treated the same way. The providers are loaded in memory when the 
application starts. Each ML provider must return a list of items when asked for.