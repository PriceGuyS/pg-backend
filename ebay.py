import datetime
import json
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

def main():
    try:
        with open("n64list",'rU') as f: #n64 list contains list of queries that are iterated through
            results = []
            for query in f:
                api = Connection(appid="DavisFre-PriceGuy-PRD-d5d74fc8f-5a07a211", config_file=None)
                response = api.execute('findItemsAdvanced', {'keywords': '{}'.format(query), # link below has more arguments for itemfilter
                                                            "PaginationInput": { # does not work for w/e reason
                                                            # "EntriesPerPage": 50,
                                                                "PageNumber": 1 # page works but results doesnt
                                                            },
                                                            "itemFilter": [ # https://developer.ebay.com/devzone/finding/callref/types/ListingInfo.html
                                                            # https://developer.ebay.com/devzone/finding/callref/types/ItemFilterType.html
                                                            # theres listinginfo and listing, not sure which is right and I can't get either to filter properly

                                                                    # {'name': 'ListingType', 'value': 'AuctionWithBIN'}, # not sure how to get both
                                                                    {'name': 'ListingType', 'value': 'FixedPrice'} # allegedly you can just give one name two values but it didnt seem to work

                                                            ],
                                                            "categoryId": [
                                                                '139973' # this is for videogames
                                                            ]
                                                            }) # https://wiki.python.org/moin/UsingAssertionsEffectively
                                                            # https://github.com/timotheus/ebaysdk-python/blob/master/samples/finding.py shows format

                assert(response.reply.ack == 'Success') # if not a 200 aka "success"
                assert(type(response.reply.timestamp) == datetime.datetime) # assert is used for error checking
                assert(type(response.dict()) == dict) # makes sure response is of type dict else error?
                item = response.dict()

                if item['paginationOutput']['totalPages'] == '0': # detects if 0 results returned, 0 also a string
                    print "Search has no results"
                else:
                    for listing in item['searchResult']['item']:
                        print listing['listingInfo']['buyItNowAvailable']
                        listingDict = {}
                        listingDict['id'] = listing['itemId']; listingDict['query'] = query.rstrip(); listingDict['title'] = listing['title']; listingDict['URL'] = listing['viewItemURL']
                        listingDict['price'] = listing['sellingStatus']['convertedCurrentPrice']['value']; listingDict['currency'] = listing['sellingStatus']['convertedCurrentPrice']['_currencyId']
                        listingDict['condition'] = listing['condition']['conditionDisplayName']; listingDict['endTime'] = listing['listingInfo']['endTime']
                        listingDict['category'] = listing['primaryCategory']['categoryName']; listingDict['country'] = listing['country']; listingDict['shipsTo'] = listing['shippingInfo']['shipToLocations']
                        results.append(listingDict)

        with open('jsonResults1.json', 'w') as w: # might wannna do a for loop and do appends?
            json.dump(results, w, indent=4, sort_keys=True)


    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == "__main__":
    main()
