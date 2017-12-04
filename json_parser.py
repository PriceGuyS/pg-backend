import json
import sys
import decimal
import boto3
from listingsCreateTable import createTable
import time

def importData(jsonFile, name):
    maxRetries = 5
    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html tutorial!
    mysession = boto3.session.Session(aws_access_key_id='ACCESS_KEY', aws_secret_access_key='SECRET_KEY') # this accesses the keys in the 'credentials' file in ~/.aws/
    #mysession = boto3.session.Session(profile_name="davis2") # for specifying user
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table(name)

    with open(jsonFile) as json_file:

        listings = json.load(json_file, parse_float = decimal.Decimal)
        for listing in listings:
            counter = 0
            amazon = listing["amazon"]
            category = listing["category"]
            ebay = listing["ebay"]
            ID = listing["id"] # case not matching because I didn't realize id is a keyword
            inputQuery = listing["inputQuery"]
            title = listing["title"]

            print "Adding listing: {}".format(title)

            while(counter != maxRetries):
                try:
                    table.put_item(
                       Item={
                           'amazon': amazon,
                           'category': category,
                           'ebay': ebay,
                           'id': ID,
                           'inputQuery': inputQuery,
                           'title': title,
                        }
                    )
                    counter = 0
                    break
                except Exception as e:
                    print e
                    counter = counter + 1

def parse_json():
    results = []
    count = 0
    with open('n64ListAll', 'r') as n64_list:
        n64_games = [game.decode('utf-8') for game in n64_list.read().split('\n')]

        with open('amazon_results.json') as amazon_file, open('ebay.json') as ebay_file:
            amazon_listings = json.load(amazon_file, parse_float = decimal.Decimal)
            ebay_listings = json.load(ebay_file, parse_float = decimal.Decimal)
            for game in n64_games:
                combined_obj = { "amazon":{}, "ebay":{}}
                a_list = [i for i in amazon_listings if game in i["title"]]
                e_list = [j for j in ebay_listings if game in j["title"]]
                if a_list and e_list:
                    print game
                    print "Amazon"
                    print a_list[0]["title"]
                    print "Ebay"
                    print e_list[0]["title"]
                    combined_obj["category"] = a_list[0]["category"]
                    combined_obj["inputQuery"] = game
                    combined_obj["id"] = e_list[0]["id"]
                    combined_obj["title"] = game
                    combined_obj["amazon"]["URL"] = a_list[0]["URL"]
                    combined_obj["amazon"]["condition"] = a_list[0]["condition"]
                    combined_obj["amazon"]["country"] = a_list[0]["country"]
                    combined_obj["amazon"]["currency"] = a_list[0]["currency"]
                    combined_obj["amazon"]["endTime"] = a_list[0]["endTime"]
                    combined_obj["amazon"]["id"] = a_list[0]["id"]
                    if a_list[0]["imageURL"] == "https://images-na.ssl-images-amazon.com/images/I/31BDm2VqflL.jpg":
                        combined_obj["amazon"]["imageURL"] = "N/A"
                    else:
                        combined_obj["amazon"]["imageURL"] = a_list[0]["imageURL"]
                    combined_obj["amazon"]["price"] = a_list[0]["price"]
                    combined_obj["amazon"]["shipsTo"] = a_list[0]["shipsTo"]
                    combined_obj["amazon"]["title"] = a_list[0]["title"]

                    combined_obj["ebay"]["URL"] = e_list[0]["URL"]
                    combined_obj["ebay"]["condition"] = e_list[0]["condition"]
                    combined_obj["ebay"]["country"] = e_list[0]["country"]
                    combined_obj["ebay"]["currency"] = e_list[0]["currency"]
                    combined_obj["ebay"]["endTime"] = e_list[0]["endTime"]
                    combined_obj["ebay"]["id"] = e_list[0]["id"]
                    combined_obj["ebay"]["imageURL"] = e_list[0]["imageURL"]
                    combined_obj["ebay"]["price"] = e_list[0]["price"]
                    combined_obj["ebay"]["shipsTo"] = e_list[0]["shipsTo"]
                    combined_obj["ebay"]["title"] = e_list[0]["title"]
                    print combined_obj
                    results.append(combined_obj)

            with open('ebay_and_amazon.json', 'w') as w: # might wannna do a for loop and do appends?
                json.dump(results, w, indent=4, sort_keys=True)

            import_name = "EbayAndAmazon"

            dynamodb_client = boto3.client('dynamodb', region_name="us-east-1")

            existing_tables = dynamodb_client.list_tables()['TableNames']

            if import_name not in existing_tables:
                print "Creating Table {}.".format("EbayAndAmazon")
                createTable(import_name)
            else:
                import_name = "EbayAndAmazon" + "_1"
                print "{} already exists. Creating {}.".format("EbayAndAmazon", import_name)
                createTable(import_name)

            time.sleep(10)

            try:
                print "Loading {} into {}:".format("ebay_and_amazon.json", import_name)
                importData("ebay_and_amazon.json", "EbayAndAmazon")
            except Exception as e:
                print e

if __name__ == "__main__":
    parse_json()
