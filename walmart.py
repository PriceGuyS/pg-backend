import requests
import json

apiKey = 'm4erhxjphffkusatd6x85sak'
url = "http://api.walmartlabs.com/v1/search"
with open("n64list", "r") as f:
    results = []
    for query in f:
        param = {'apiKey':'%s'%apiKey, 'categoryId':'2636', 'query':'%s'%f}

        r = requests.get(url, params=param)

        i = 0
        for listing in r.json()['items']:
            print listing['itemId']
            print listing['name']

# print json.dumps(r.json(), indent=4, sort_keys=True)
