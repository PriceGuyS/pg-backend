from amazonproduct import API
import json
from listingsCreateTable import createTable
from listingsLoadData import loadData
import time

api = API(locale='us')

result_file_name = "amazon_results.json"
table_name = "testTable"

with open("n64List", "r") as infile:
    results = []
    for line in infile:
        print "About to query: {}".format(line)
        for game in api.item_search('VideoGames', Keywords=line, ItemPage=1):
            query_result = api.item_lookup(str(game.ASIN), ResponseGroup='OfferFull,ItemAttributes')
            new_dict, used_dict, collectable_dict = {}, {}, {}
            try:
                new_dict["category"] = query_result.Items.Item.ItemAttributes.ProductGroup
                new_dict["query"] = line.rstrip()
                new_dict["title"] = query_result.Items.Item.ItemAttributes.Title
                new_dict["country"] = "US"
                new_dict["URL"] = query_result.Items.Item.DetailPageURL
                new_dict["condition"] = "New"
                new_dict["endTime"] = "N/A"
                new_dict["shipsTo"] = "Worldwide"
                new_dict["currency"] = query_result.Items.Item.OfferSummary.LowestNewPrice.CurrencyCode
                new_dict["price"] = "{0:.2f}".format(query_result.Items.Item.OfferSummary.LowestNewPrice.Amount / 100.00)
                print "Adding {} {}".format(new_dict["condition"], new_dict["title"])
                results.append(new_dict)
            except Exception as e:
                print e

            try:
                used_dict["category"] = query_result.Items.Item.ItemAttributes.ProductGroup
                used_dict["query"] = line.rstrip()
                used_dict["title"] = query_result.Items.Item.ItemAttributes.Title
                used_dict["country"] = "US"
                used_dict["URL"] = query_result.Items.Item.DetailPageURL
                used_dict["condition"] = "Used"
                used_dict["endTime"] = "N/A"
                used_dict["shipsTo"] = "Worldwide"
                used_dict["currency"] = query_result.Items.Item.OfferSummary.LowestUsedPrice.CurrencyCode
                used_dict["price"] = "{0:.2f}".format(query_result.Items.Item.OfferSummary.LowestUsedPrice.Amount / 100.00)
                print "Adding {} {}".format(used_dict["condition"], used_dict["title"])
                results.append(used_dict)
            except Exception as e:
                print e

    with open(result_file_name, 'w') as outfile:
        json.dump(results, outfile, indent=4, sort_keys=True)

    try:
        createTable(table_name)
        time.sleep(10)
        loadData(result_file_name, table_name)
    except Exception as e:
        print e
