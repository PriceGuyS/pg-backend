from amazonproduct import API
from lxml import etree

api = API(locale='us')

for game in api.item_search('VideoGames', Keywords='n64', ItemPage=1):
    print game.ItemAttributes.Title
    result = api.item_lookup(str(game.ASIN), ResponseGroup='Offers')
    print etree.tostring(result.Items.Item.Offers, pretty_print=True)
