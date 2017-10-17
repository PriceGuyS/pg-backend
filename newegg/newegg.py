import requests

# https://github.com/bemasher/NeweggMobileAPI
# CHECK THIS OUT: https://github.com/econpy/newegg
URL = "http://www.ows.newegg.com/Search.egg/Advanced/application/x-www-form-urlencoded"
PARAMS = {
        	"PageNumber": 1,
        	"BrandId": -1,
        	"NValue": "",
        	"StoreDepaId": -1,
        	"NodeId": -1,
        	"Keyword": "Super Mario 64",
        	"IsSubCategorySearch": False,
        	"SubCategoryId": -1,
        	"Sort": "FEATURED",
        	"CategoryId": -1,
        	"IsUPCCodeSearch": False
        }

r = requests.post(url=URL, data=PARAMS)

print(r.json)
print(r.text)
