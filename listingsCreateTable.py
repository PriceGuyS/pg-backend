from __future__ import print_function # Python 2/3 compatibility
import boto3

def createTable(name):
    mysession = boto3.session.Session(aws_access_key_id='ACCESS_KEY', aws_secret_access_key='SECRET_KEY') # this accesses the keys in the 'credentials' file in ~/.aws/
    #mysession = boto3.session.Session(profile_name="davis2") # for specifying user
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # PRICING! https://aws.amazon.com/dynamodb/pricing/
    # Tutorial: http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html

    table = dynamodb.create_table(
        TableName=name,
        KeySchema=[ # http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table
        # https://aws.amazon.com/blogs/database/choosing-the-right-dynamodb-partition-key/
        # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GuidelinesForTables.html
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'inputQuery',
                'KeyType': 'RANGE'  #Sort key
            },
        ], # http://boto3.readthedocs.io/en/latest/reference/customizations/dynamodb.html not a lot of data types, one for date in Java but not python. Not even a floa
        AttributeDefinitions=[ #number of attribs has to match between key schema and attrib defs. kept these just in case schema needs adjusting
            # {
            #     'AttributeName': 'site',
            #     'AttributeType': 'S'
            # },
            # {
            #     'AttributeName': 'category',
            #     'AttributeType': 'S'
            # },
            # {
            #     'AttributeName': 'condition',
            #     'AttributeType': 'S'
            # },
            # {
            #     'AttributeName': 'country',
            #     'AttributeType': 'S'
            # },
            # {
            #     'AttributeName': 'currency',
            #     'AttributeType': 'S'
            # },

            # {
            #     'AttributeName': 'price',
            #     'AttributeType': 'N' #might work for decimals
            # },
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'inputQuery',
                'AttributeType': 'S'
            }
            # {
            #     'AttributeName': 'shipsTo',
            #     'AttributeType': 'S'
            # },
            # {
            #     'AttributeName': 'title',
            #     'AttributeType': 'S'
            # },


        ], # http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ProvisionedThroughput.html I doubt we need 10
        # 1 read per sec for a 4kb item 1 write per sec for 1kb
        # about 25 for both for free package
        # GlobalSecondaryIndexes=[
        #     {
        #         'IndexName': "videogames",
        #         'KeySchema': [
        #             {
        #                 'AttributeName': 'site',
        #                 'KeyType': 'HASH'
        #             },
        #             {
        #                 'AttributeName': 'inputQuery',
        #                 'KeyType': 'RANGE'
        #             }
        #         ],
        #         'Projection': {
        #             'ProjectionType': 'INCLUDE',
        #             'NonKeyAttributes': [
        #                 'title',
        #             ]
        #         },
        #         'ProvisionedThroughput': {
        #             'ReadCapacityUnits': 10,
        #             'WriteCapacityUnits': 10
        #         }
        #     }
        # ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 15,
            'WriteCapacityUnits': 15
        }
    )

    print("Table status:", table.table_status)
