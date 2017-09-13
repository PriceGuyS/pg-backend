import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

# https://github.com/timotheus/ebaysdk-python
# install guide https://github.com/timotheus/ebaysdk-python/blob/master/INSTALL
#################################################################################################################################
#   Default example with a few additions
#################################################################################################################################
# try:
#     api = Connection(appid="DavisFre-PriceGuy-PRD-d5d74fc8f-5a07a211", config_file=None)
#     response = api.execute('findItemsAdvanced', {'keywords': 'legos'}) # https://wiki.python.org/moin/UsingAssertionsEffectively
#
#     assert(response.reply.ack == 'Success') # if not a 200 aka "success"
#     assert(type(response.reply.timestamp) == datetime.datetime) # assert is used for error checking
#     assert(type(response.reply.searchResult.item) == list) # see if result is a list (replace with string to see assert work)
#
#     item = response.reply.searchResult.item[0]
#     assert(type(item.listingInfo.endTime) == datetime.datetime)
#     assert(type(response.dict()) == dict) # makes sure response is of type dict else error?
#     print len(response.dict()) # this returns a lot (only 6 responses based on len)
#
#
# except ConnectionError as e:
#     print(e)
#     print(e.response.dict())
#################################################################################################################################

try:
    api = Connection(appid="DavisFre-PriceGuy-PRD-d5d74fc8f-5a07a211", config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': 'Nintendo 64', # link below has more arguments for itemfilter
                                                'itemFilter': [{
                                                    'name': 'Condition',
                                                    'value': 'New'},
                                                    {'name': 'FreeShippingOnly',
                                                    'value': True},
                                                ]
                                                }) # https://wiki.python.org/moin/UsingAssertionsEffectively
                                                # https://github.com/timotheus/ebaysdk-python/blob/master/samples/finding.py shows format

    assert(response.reply.ack == 'Success') # if not a 200 aka "success"
    assert(type(response.reply.timestamp) == datetime.datetime) # assert is used for error checking
    assert(type(response.reply.searchResult.item) == list) # see if result is a list (replace with string to see assert work)
    item = response.reply.searchResult.item[0]
    # assert(type(item.listingInfo.endTime) <= datetime.datetime)
    assert(type(response.dict()) == dict) # makes sure response is of type dict else error?
    # print len(response.dict()) # this returns a lot (only 6 responses based on len)
    # auctions = response.dict()
    i = 1 # was gonna be a for loop
    print "item {}: ".format(i)+str(item) # tried iterating through all results but the type is not iterable. Tried a conversion or two and couldnt get
    # item looks like a dict but i cannot get attribs via [0] or ['attrib'] response needs to be converted

except ConnectionError as e:
    print(e)
    print(e.response.dict())
