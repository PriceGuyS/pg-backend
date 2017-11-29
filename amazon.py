import sys
import time
import json
from amazonproduct import API
from listingsCreateTable import createTable
from listingsLoadData import loadData
import boto3
from lxml import etree

dynamodb_client = boto3.client('dynamodb', region_name="us-east-1")

reload(sys)
sys.setdefaultencoding('utf8')

api = API(locale='us')

result_file_name = "amazon_results.json"
table_name = "Amazon_test"
start_time = time.time()

with open("n64list", "r") as infile:
    results = []
    for i, line in enumerate(infile):
        if i > 0:
            print "\n"
        print "About to query entry #{}:\n{}".format(i+1, line.rstrip())
        try:
            search_result = api.item_search('VideoGames', Keywords=line, ItemPage=1)
        except Exception as e:
            continue
        for game in search_result:
            try:
                query_result = api.item_lookup(str(game.ASIN), ResponseGroup='OfferFull,ItemAttributes,Images')
            except Exception as e:
                print e
            new_dict, used_dict, collectable_dict = {}, {}, {}
            try:
                new_dict["id"] = str(query_result.Items.Item.ASIN) + "1"
                new_dict["category"] = str(query_result.Items.Item.ItemAttributes.ProductGroup)
                new_dict["inputQuery"] = line.rstrip()
                new_dict["title"] = str(query_result.Items.Item.ItemAttributes.Title)
                new_dict["country"] = "US"
                new_dict["URL"] = str(query_result.Items.Item.DetailPageURL)
                new_dict["condition"] = "New"
                new_dict["endTime"] = "N/A"
                new_dict["shipsTo"] = "Worldwide"
                new_dict["currency"] = str(query_result.Items.Item.OfferSummary.LowestNewPrice.CurrencyCode)
                new_dict["price"] = "{0:.2f}".format(query_result.Items.Item.OfferSummary.LowestNewPrice.Amount / 100.00)
                new_dict["site"] = "amazon"
                try:
                    if(str(query_result.Items.Item.ImageSets.ImageSet.LargeImage.URL) == "https://images-na.ssl-images-amazon.com/images/I/31BDm2VqflL.jpg"):
                        print "LOL: {}".format(str(query_result.Items.Item.ImageSets.ImageSet.MediumImage.URL))
                    new_dict["imageURL"] = str(query_result.Items.Item.ImageSets.ImageSet.LargeImage.URL)
                except:
                    new_dict["imageURL"] = "N/A"
                print "Adding {} {}".format(new_dict["condition"], new_dict["title"])
                results.append(new_dict)
            except Exception as e:
                print "No new item price"

            try:
                used_dict["id"] = str(query_result.Items.Item.ASIN) + "2"
                used_dict["category"] = str(query_result.Items.Item.ItemAttributes.ProductGroup)
                used_dict["inputQuery"] = line.rstrip()
                used_dict["title"] = str(query_result.Items.Item.ItemAttributes.Title)
                used_dict["country"] = "US"
                used_dict["URL"] = str(query_result.Items.Item.DetailPageURL)
                used_dict["condition"] = "Used"
                used_dict["endTime"] = "N/A"
                used_dict["shipsTo"] = "Worldwide"
                used_dict["currency"] = str(query_result.Items.Item.OfferSummary.LowestUsedPrice.CurrencyCode)
                used_dict["price"] = "{0:.2f}".format(query_result.Items.Item.OfferSummary.LowestUsedPrice.Amount / 100.00)
                used_dict["site"] = "amazon"
                try:
                    used_dict["imageURL"] = str(query_result.Items.Item.ImageSets.ImageSet.LargeImage.URL)
                except:
                    used_dict["imageURL"] = "N/A"
                print "Adding {} {}".format(used_dict["condition"], used_dict["title"])
                results.append(used_dict)
            except Exception as e:
                print "No used item price"

    with open(result_file_name, 'w') as outfile:
        json.dump(results, outfile, indent=4, sort_keys=True)

    existing_tables = dynamodb_client.list_tables()['TableNames']

    if table_name not in existing_tables:
        createTable(table_name)
    else:
        createTable(table_name + "_1")
        table_name = table_name + "_1"

    time.sleep(10)

    try:
        loadData(result_file_name, table_name)
    except Exception as e:
        print e

    print "Elapsed time: {}".format(time.time() - start_time)
