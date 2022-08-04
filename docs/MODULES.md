# Modules:

## Recommender

The core recommender systems that orchestrates calling providers, filtering
and processing of requests.

## Providers

Modules that manages all providers.

## Scheduler

Scheduler for running background processes such as ML models, user_mets etc.

## Search/Query Engine

These modules interacts with the ElasticSearch instance based on Provider input and
returns a list of items.