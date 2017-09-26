from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html tutorial!
dynamodb = boto3.resource('dynamodb', aws_access_key_id='##YourKeyHere##', aws_secret_access_key='##YourKeyHere##', region_name='us-west-2')

table = dynamodb.Table('Listings')

with open("jsonResults.json") as json_file:
    listings = json.load(json_file, parse_float = decimal.Decimal)
    for listing in listings:
        URL = listing['URL']
        category = listing['category']
        condition = listing['condition']
        country = listing['country']
        currency = listing['currency']
        endTime = listing['endTime']
        price = listing['price']
        query = listing['query']
        shipsTo = listing['shipsTo']
        title = listing['title']


        print("Adding listing: ", title)

        table.put_item(
           Item={
               'URL': URL,
               'category': category,
               'condition': condition,
               'country': country,
               'currency': currency,
               'endTime': endTime,
               'price': price,
               'query': query,
               'shipsTo': shipsTo,
               'title': title
            }
        )
