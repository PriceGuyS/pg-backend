import datetime
import sys
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

def main(query, page):
    try:
        pages = {}
        for i in range(int(page)):
            api = Connection(appid="DavisFre-PriceGuy-PRD-d5d74fc8f-5a07a211", config_file=None)
            response = api.execute('findItemsAdvanced', {'keywords': '{}'.format(query), # link below has more arguments for itemfilter
                                                        "PaginationInput": { # does not work for w/e reason
                                                        # "EntriesPerPage": 50,
                                                        "PageNumber": (i+1)
                                                        }
                                                        }) # https://wiki.python.org/moin/UsingAssertionsEffectively
                                                        # https://github.com/timotheus/ebaysdk-python/blob/master/samples/finding.py shows format

            assert(response.reply.ack == 'Success') # if not a 200 aka "success"
            assert(type(response.reply.timestamp) == datetime.datetime) # assert is used for error checking
            assert(type(response.reply.searchResult.item) == list) # see if result is a list (replace with string to see assert work)
            assert(type(response.dict()) == dict) # makes sure response is of type dict else error?
            # item = response.dict()
            pages[i+1]=response.dict()

        for i,listing in enumerate(pages[1]['searchResult']['item']):
            print "listing {}: ".format(i)+str(listing)+"\n"
        for i,listing in enumerate(pages[3]['searchResult']['item']):
            print "listing {}: ".format(i)+str(listing)+"\n"

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
