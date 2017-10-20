

def store_search(store_id, device_id):
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
                        "device_id": device_id
                      }
                    }
                  ]
                }
              }
            }
    return query


def get_device(device_id):
    query = {
              "query": {
                "bool": {
                  "must": [
                    {
                      "match": {
                        "device_id": device_id
                      }
                    }
                  ]
                }
              }
            }
    return query
