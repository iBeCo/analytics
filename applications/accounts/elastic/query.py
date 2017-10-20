

def store_search(store_id,id):
    query = {
              "query": {
                "bool": {
                  "must": [
                    {
                      "match": {
                        "stores.store_id": store_id
                      }
                    },
                    {
                      "match": {
                        "_id": id
                      }
                    }
                  ]
                }
              }
            }
    return query
