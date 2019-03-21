import json
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def confirm_charge(room_members, this_week_charger):
    room_number_array = []
    room_name_array = []
    for member in room_members:
        room_number_array.append(member["Room"])
        room_name_array.append(member["Name"])

    charge_room_array = []
    charge_name_array = []
    for charger in this_week_charger:
        charge_room_array.append(charger["Room"])
        charge_name_array.append(charger["Name"])

    # 今週のごみ捨て当番のインデックスと名前
    confirm_index = []
    confirm_flag = []

    # ゴミ捨ての当番の名前が入居者の配列に入っているか確認する
    for (name, room) in zip(charge_name_array, charge_room_array):
        name = name.rstrip()
        room = room.rstrip()
        print(name + " " + room)

        if name != "None":
            # 名前のインデックスを入れる
            index = room_name_array.index(name)
            confirm_index.append(index)
            confirm_flag.append(True)
        else:
            # 部屋番号のインデックスを入れる
            index = room_number_array.index(room)
            confirm_index.append(index)
            confirm_flag.append(False)

    logger.info("今週の未確定のゴミ当番: " + str(confirm_index))

    # 当番の名前がいるか比較する
    room_count = len(room_name_array)
    if confirm_flag == [True, False]:
        current_num = confirm_index[1]
        margin_num = 1
        chnage_num = 1
        confirm_index = reconfirm_charge(
            confirm_index, room_name_array, room_count, current_num, chnage_num, margin_num)

    elif confirm_flag == [False, True]:
        current_num = confirm_index[0]
        margin_num = 2
        chnage_num = 0
        confirm_index = reconfirm_charge(
            confirm_index, room_name_array, room_count, current_num, chnage_num, margin_num)
    elif confirm_flag == [False, False]:
        # 1番目
        current_num = confirm_index[1]
        margin_num = 3
        chnage_num = 1
        confirm_index = reconfirm_charge(
            confirm_index, room_name_array, room_count, current_num, chnage_num, margin_num)
        # 2番目
        current_num = confirm_index[0]
        margin_num = 2
        chnage_num = 0
        confirm_index = reconfirm_charge(
            confirm_index, room_name_array, room_count, current_num, chnage_num, margin_num)

    correc_room = []
    correc_name = []
    # 今週のゴミ当番（部屋番号，名前を入れる）
    for index in confirm_index:
        correc_room.append(room_number_array[index])
        correc_name.append(room_name_array[index])

    logger.info("今週の確定したゴミ当番: " + str(confirm_index))
    logger.info("フラグ: " + str(confirm_flag))

    # 次の担当者の配列を入れる
    next_room = []
    next_name = []

    for charge_room_num in charge_room_array:
        current_index = room_number_array.index(charge_room_num)

        if current_index == len(room_number_array) - 2:
            next_index = 0
        elif current_index == len(room_number_array) - 1:
            next_index = 1
        else:
            next_index = current_index + 2

        next_room.append(room_number_array[next_index])
        next_name.append(room_name_array[next_index])

    logger.info("来週のゴミ当番の部屋番号: " + str(next_room))
    logger.info("来週のゴミ当番の名前: " + str(next_name))

    return charge_room_array, correc_room, correc_name, next_room, next_name


# ゴミ捨て当番がいなかった場合には再度選出する
def reconfirm_charge(confirm_index, room_name_array, room_count, current_num, chnage_num, margin_num):
    current_num = current_num + margin_num
    for count in range(room_count):
        if current_num > room_count:
            current_num = 0
        if room_name_array[current_num] != "None":
            confirm_index[chnage_num] = current_num
            break
        count += 1
        current_num += 1

    return confirm_index


def confirm_garbage_type(type_of_garbage):
    week_day_array = ["Monday", "Tuesday", "Wednesday",
                      "Thursday", "Friday", "Saturday", "Sunday"]
    today_time = datetime.datetime.now()
    weekday_num = today_time.weekday() + 1
    # 曜日が漏れたら初期化
    if weekday_num >= 7:
        weekday_num = 0

    todays_day = week_day_array[weekday_num]

    todays_garbage_name = []
    for garbage_day in type_of_garbage:
        for day in garbage_day["Day"]:
            if todays_day == day:
                todays_garbage_name.append(garbage_day["GarbageType"])
    logger.info(todays_day)
    logger.info(todays_garbage_name)

    return todays_garbage_name


# ゴミ捨て当番の送るメッセージを整形
def make_garbage_massege(names, rooms, todays_garbage_name):
    send_message = ""
    for (name, room) in zip(names, rooms):
        send_message += room + " " + name + "\n"

    send_message += "\nWould you please throw out the following garbage\n"

    for garbage_name in todays_garbage_name:
        send_message += "* " + garbage_name + "\n"

    return send_message
