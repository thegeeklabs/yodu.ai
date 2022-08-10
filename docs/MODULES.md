# Modules:

## Recommender

The core recommender systems that orchestrates calling providers, filtering
and processing of requests.

## Providers

Modules that manages all providers.
Yodu comes with a set of providers in the directory: ``.
Each provider must have a "meta". You can see default meta here:

Provider args can be provided from `default_values` or `algo_spec` or in the `get_items` request itself.
Good practise it to provide most values in algo_specification.
Providers can be added or removed from a given recommender system but to use them you must
specify them in the algorithm specification `algo_spec` file.

When a provider is aded to a recommender, the provider directory is added
to  `yodu/provider/repo/<recommender_name>/<provider_name>`

## Scheduler

Scheduler for running background processes such as ML models, user_mets etc.

## Search/Query Engine

These modules interacts with the ElasticSearch instance based on Provider input and
returns a list of items.