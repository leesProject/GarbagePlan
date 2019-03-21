import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import logging

dynamodb = boto3.resource('dynamodb')


def items_read(table_name):
    dynamodb_table = dynamodb.Table(table_name)
    response = dynamodb_table.query(
        KeyConditionExpression=Key('House').eq("Oimachi")
    )
    return response["Items"]


def items_delete(table_name, database_charge_room_array):
    dynamodb_table = dynamodb.Table(table_name)
    print(database_charge_room_array)
    for database_charge in database_charge_room_array:
        dynamodb_table.delete_item(
            Key={
                "House": "Oimachi",
                "Room": database_charge
            }
        )


def items_add(table_name, group_id, next_room, next_name):
    dynamodb_table = dynamodb.Table(table_name)
    for room_num, room_name in zip(next_room, next_name):
        dynamodb_table.put_item(
            Item={
                "House": "Oimachi",
                "Room": room_num,
                "GroupId": group_id,
                "Name": room_name
            }
        )
