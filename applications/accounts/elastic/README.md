## Get Suggestions

Use this API to get auto complete suggestion
````
POST device/_search
{
    "suggest": {
        "colour-suggest" : {
            "prefix" : "ic",
            "completion" : {
                "field" : "tag_suggest"
            }
        }
    }
}
````

Use this API for location specific search
````
GET device/_search
{
    "query": {
        "bool" : {
            "must" : {
                "match_all" : {}
            },
            "filter" : {
                "geo_distance" : {
                    "distance" : "200km",
                    "location" : {
                        "lat" : 40,
                        "lon" : -70
                    }
                }
            }
        }
    }
}
````
