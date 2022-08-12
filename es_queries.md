# ElasticSearch Queries

## Top Publications by comment count
This query returns top Publication ID based on comments, with X number of comments as well.
Query is filtered by range as well
Problems: ES only searches 10K documents
```
POST /lens/_search?size=0
{
  "query": {
		"bool": {
			"must": {
				"term": {
					"type.keyword": "INDEXER_COMMENT_CREATED"
				}
			},
			"filter": {
				"range": {
					"created_at": {
						"gt": "2022-06-07T22:44:12",
						"lt": "2022-07-07T22:44:12"
					}
				}
			}
		}
	},
  "aggs": {
    "top_publication_by_comments": {
      "terms": {
        "field": "tags.pubId.keyword",
        "size": 10
      },
      "aggs": {
        "top_comment_hits": {
          "top_hits": {
            "sort": [
              {
                "created_at": {
                  "order": "desc"
                }
              }
            ],
            "_source": {
              "includes": [ "value","type","tags" ]
            },
            "size": 2
          }
        }
      }
    }
  }
}

```

## Top Commenter
```
POST /lens/_search?size=0
{
  "query": {
    "constant_score": {
      "filter": {
        "match": { "type": "INDEXER_COMMENT_CREATED" }
      }
    }
  },
  "aggs": {
    "top_publication_by_comments": {
      "terms": {
        "field": "tags.profileId.keyword",
        "size": 10
      },
      "aggs": {
        "top_comment_hits": {
          "top_hits": {
            "sort": [
              {
                "created_at": {
                  "order": "desc"
                }
              }
            ],
            "_source": {
              "includes": [ "value","type","tags" ]
            },
            "size": 2
          }
        }
      }
    }
  }
}
```

## Top Posts created by UserIds in last 30 days
```
{
  "query": {
        "bool": {
            "must": [
              {
                "term": {
                    "type.keyword": "INDEXER_POST_CREATED"
                }
              }
            ],
            "filter": {
                "range": {
                    "created_at": {
                        "gt": "2022-07-01T12:13:36.510696Z",
                        "lt": "2022-07-31T12:13:34.243718Z"
                    }
                }
            }
        }
    },
  "aggs": {
    "top_publication_by_comments": {
      "terms": {
        "field": "user_id.keyword",
        "size": 10
      },
      "aggs": {
        "top_comment_hits": {
          "top_hits": {
            "sort": [
              {
                "created_at": {
                  "order": "desc"
                }
              }
            ],
            "_source": {
              "includes": [ "value","type","tags" ]
            }
          }
        }
      }
    }
  }
}
```
