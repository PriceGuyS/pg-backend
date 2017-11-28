from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

def removeItems(tableName):
    # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html tutorial!
    mysession = boto3.session.Session(aws_access_key_id='ACCESS_KEY', aws_secret_access_key='SECRET_KEY') # this accesses the keys in the 'credentials' file in ~/.aws/
    #mysession = boto3.session.Session(profile_name="davis2") # for specifying user
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table(tableName)

    table.delete_item(      #this needs to be chenged to check every item in table
        Key={
            'id': ID,
            'endTime': endTime
        },
        ConditionExpression="",
    )
