import requests
import json

apiKey = 'm4erhxjphffkusatd6x85sak'
url = "http://api.walmartlabs.com/v1/search?apiKey=%s&categoryId=2636&query=Super+Mario+64" % apiKey

r = requests.get(url)

print json.dumps(r.json(), indent=4, sort_keys=True)
