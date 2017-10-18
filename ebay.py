import datetime
import json
import time
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from listingsCreateTable import createTable
from listingsLoadData import loadData

def main():
    try: # insert a cron job?
        with open("n64list",'rU') as f: #n64 list contains list of queries that are iterated through
            results = []
            for query in f:
                api = Connection(appid="DavisFre-PriceGuy-PRD-d5d74fc8f-5a07a211", config_file=None)
                response = api.execute('findItemsAdvanced', {'keywords': '{}'.format(query), # link below has more arguments for itemfilter
                                                            "PaginationInput": { # does not work for w/e reason
                                                                "PageNumber": 1 # page works but results doesnt
                                                            },
                                                            "itemFilter": [
                                                                    # {'name': 'ListingType', 'value': 'AuctionWithBIN'}, # not sure how to get both
                                                                    {'name': 'ListingType', 'value': 'FixedPrice'} # allegedly you can just give one name two values but it didnt seem to work
                                                                    # https://developer.ebay.com/devzone/finding/callref/types/ItemFilterType.html
                                                            ],
                                                            "categoryId": [
                                                                '139973' # this is for videogames
                                                            ]
                                                            })

                assert(response.reply.ack == 'Success') # if not a 200 aka "success"
                assert(type(response.reply.timestamp) == datetime.datetime) # assert is used for error checking
                assert(type(response.dict()) == dict) # makes sure response is of type dict else error?
                item = response.dict()

                if item['paginationOutput']['totalPages'] == '0': # detects if 0 results returned, 0 also a string
                    print "Search has no results"
                else:
                    for listing in item['searchResult']['item']:
                        print query
                        listingDict = {}
                        listingDict['id'] = listing['itemId']; listingDict['query'] = query.rstrip(); listingDict['title'] = listing['title']; listingDict['URL'] = listing['viewItemURL']
                        listingDict['price'] = listing['sellingStatus']['convertedCurrentPrice']['value']; listingDict['currency'] = listing['sellingStatus']['convertedCurrentPrice']['_currencyId']
                        listingDict['condition'] = listing['condition']['conditionDisplayName']; listingDict['endTime'] = listing['listingInfo']['endTime']
                        listingDict['category'] = listing['primaryCategory']['categoryName']; listingDict['country'] = listing['country']; listingDict['shipsTo'] = listing['shippingInfo']['shipToLocations']
                        results.append(listingDict)

        jsonFile = 'jsonResults3.json'
        tableName = 'testTable'
        with open(jsonFile, 'w') as w: # might wannna do a for loop and do appends?
            json.dump(results, w, indent=4, sort_keys=True)

        createTable(tableName)
        time.sleep(10)
        loadData(jsonFile, tableName)


    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == "__main__":
    main()
