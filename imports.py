import sys
import time
from listingsCreateTable import createTable
from listingsLoadData import loadData
import boto3

def importData(table_name, result_file_name):
    start_time = time.time()

    dynamodb_client = boto3.client('dynamodb', region_name="us-east-1")

    existing_tables = dynamodb_client.list_tables()['TableNames']

    if table_name not in existing_tables:
        createTable(table_name)

    time.sleep(10)

    try:
        loadData(result_file_name, table_name)
    except Exception as e:
        print e

    print "Elapsed time: {}".format(time.time() - start_time)
