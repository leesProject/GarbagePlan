import urllib.request
import json
import os
import database
import calc
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def notification_charge(event, context):
    room_members = database.items_read('borderless-house-members')
    logger.info(room_members)

    this_week_charger = database.items_read(
        'borderles-this-week-garbage-charge')
    logger.info(this_week_charger)

    type_of_garbage = database.items_read('borderless-type-of-garbage')
    logger.info(type_of_garbage)

    # 今週のゴミ当番がいるか確認
    database_charge_room_array, correc_room, correc_name, next_room, next_name = calc.confirm_charge(
        room_members, this_week_charger)

    # ゴミの種類を取得
    todays_garbage_name = calc.confirm_garbage_type(type_of_garbage)

    # ゴミの種類の配列が空ではない場合
    if todays_garbage_name:
        # メッセージを整形
        send_message = calc.make_garbage_massege(
            correc_name, correc_room, todays_garbage_name)
        # メッセージをLINEに送信
        post_to_line(send_message)

        # 一旦今週のごみ捨て当番のレコードを削除する
        database.items_delete(
            'borderles-this-week-garbage-charge', database_charge_room_array)

        # 来週のごみ捨て当番のレコードを登録する
        database.items_add('borderles-this-week-garbage-charge',
                           'C5ac0fe9390c99fe1e7aa307168695d04', next_room, next_name)


def post_to_line(send_message):
    access_token = os.environ['ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']

    url = "https://api.line.me/v2/bot/message/push"
    method = "POST"
    headers = {"Content-Type": "application/json",
               "Authorization": 'Bearer ' + access_token}

    # PythonオブジェクトをJSONに変換する
    obj = {
        'to': group_id,
        'messages': [{
            'type': 'text',
            'text': send_message,
        }],
    }
    json_data = json.dumps(obj).encode("utf-8")

    # httpリクエストを準備してPOST
    request = urllib.request.Request(
        url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
