import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import logging

dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def tenant_move_info(event, context):
    logger.info(event)
    data=json.dumps(event)
    data = json.loads(data)
    
    move_status = data["Records"][0]["Sns"]["Subject"]
    tenant_info = data["Records"][0]["Sns"]["Message"]
    name = tenant_info.split(',')[0]
    date = tenant_info.split(',')[1]
    room = tenant_info.split(',')[2]
    
    if(len(date.split('　→　')) == 2):
        date = date.split('　→　')[1]    
    items_add(move_status,name,date,room)

def items_add(move_status,name,date,room):
    dynamodb_table = dynamodb.Table('borderless-house-'+move_status)
    dynamodb_table.put_item(
        Item={
                "House": "Oimachi",
                "Room": room,
                "Name": name,
                "Date": date
            }
    )
