import boto3
from boto3 import dynamodb
from boto3.session import Session
from boto3.dynamodb.conditions import Key, Attr

dynamodb_session = Session(profile_name="mayama-cli",
                           region_name="ap-northeast-1")
dynamodb = dynamodb_session.resource('dynamodb')
type_garbage_table = dynamodb.Table("borderless-type-of-garbage")


def main():
    update()
    scan()


def update():
    file = open("../conf/type-of-garbage.csv", "r")

    # ハウス名を入力
    house_name = "Oimachi"

    garbage_type_day = {}
    for line in file:
        line = line.rstrip()
        items = line.split(",")
        garbage_type = items[0]

        days = items
        del days[0:1]

        garbage_type_day[garbage_type] = days

    file.close()

    for key, value in garbage_type_day.items():
        with type_garbage_table.batch_writer() as batch:
            batch.put_item(
                Item={
                    'House': house_name,
                    'GarbageType': key,
                    'Day': value
                }
            )


def scan():
    res = type_garbage_table.scan()
    print(res)


if __name__ == '__main__':
    main()
