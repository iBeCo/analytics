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
