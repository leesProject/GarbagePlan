import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import logging
import datetime
from datetime import timedelta

dynamodb = boto3.resource('dynamodb')
today = (datetime.datetime.now()+timedelta(hours=9)) 
today = today.strftime('%Y-%m-%d')
official_table = dynamodb_table = dynamodb.Table('borderless-house-members')

def tenant_info_update(event, context):
    records = read_move_table('move-out',today)
    update_move_out_info(records)
    delete_move_table('move-out',records)
    records = read_move_table('move-in',today)
    update_move_in_info(records)
    delete_move_table('move-in',records)

def read_move_table(move_status,date):
    move_table = dynamodb.Table('borderless-house-'+move_status)
    response = move_table.query(
        KeyConditionExpression=Key('House').eq("Oimachi"),
        FilterExpression=Attr('Date').lte(date)
    )
    return response['Items']

def delete_move_table(move_status,records):
    move_table = dynamodb.Table('borderless-house-'+move_status)
    for record in records:
        move_table.delete_item(
            Key={
                    "House": "Oimachi",
                    "Room": record['Room']
                }
        )

def update_move_out_info(records):
    for record in records:
        official_table.put_item(
            Item={
                "House": "Oimachi",
                "Room": record['Room'].split('-')[0],
                "Name": 'None',
                "GroupId": 'C5ac0fe9390c99fe1e7aa307168695d04'
            }
        )

def update_move_in_info(records):
    for record in records:
        official_table.put_item(
            Item={
                "House": "Oimachi",
                "Room": record['Room'].split('-')[0],
                "Name": record['Name'],
                "GroupId": 'C5ac0fe9390c99fe1e7aa307168695d04'
            }
        )
