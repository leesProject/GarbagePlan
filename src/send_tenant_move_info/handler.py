import boto3
import logging
import json
import base64
import re
import csv

code = {}
line_splitter = ''
logger = logging.getLogger()

def send_tenant_move_info(event, context):
    global line_splitter
    global logger
    logger.setLevel(logging.INFO)
    logger.info('logger starts')
    
    logger.info('===============================EVENT===============================================')
    data=json.dumps(event)
    data = json.loads(data)
    bucket_name = data["Records"][0]["s3"]["bucket"]["name"]
    object_key = data["Records"][0]["s3"]["object"]["key"]
    logger.info('=====================================================================================')
    
    s3 = boto3.resource('s3')
    content_object = s3.Object(bucket_name, object_key)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    
    file_content = file_content.split('Subject: =?UTF-8?Q?')[1]
    
    logger.info('===============================file_content============================================')
    if(re.search(r'\r\n',file_content)):
        line_splitter = '\r\n'
        logger.info('rn')
    else:
        line_splitter = '\n'
        logger.info('n')

    logger.info(file_content)
    logger.info('=====================================================================================')
    
    subject = file_content.split('?=')[0]
    subject = convert_utf8mb3(subject)

    if re.search(r'New_resident',subject) or re.search(r'Move_out_notice',subject) or re.search(r'入居日変更',subject):
        content = file_content.split("Content-Type: text/plain;")[1]
        content = content.split("Content-Transfer-Encoding: quoted-printable")[1]
        content = convert_utf8mb3(content)
        logger.info('===============================content============================================')
        logger.info(content)
        logger.info('====================================================================================')
        message = make_massage(content)

        if re.search(r'New_resident',subject) or re.search(r'入居日変更',subject):
            publish_sns(message,'move-in')
        elif re.search(r'Move_out_notice',subject):
            publish_sns(message,'move-out')
    #権限なし。。。くそ！！！
    #s3_client = boto3.client('s3')
    #s3_client.delete_object(Bucket=bucket_name, Key=object_key)
    
def publish_sns(message, subject):
    client = boto3.client('sns')
    request = {
        'TopicArn': 'arn:aws:sns:us-west-2:778289792916:tenant_move_info',
        'Message': message,
        'Subject': subject
    }
    response = client.publish(**request)

def make_massage(content):
    global line_splitter
    name = ''
    gender = ''
    nationality = ''
    date = ''
    room = ''

    name = content.split('【Name】：')[1]
    gender = content.split('【Gender】：')[1]
    nationality = content.split('【Nationality】：')[1]
    date = content.split('【Date】：')[1]
    room = content.split('【Room】：')[1]

    name = convert_unicode2utf8(name.split(line_splitter)[0])
    gender = gender.split(line_splitter)[0]
    nationality = nationality.split(line_splitter)[0]
    date = date.split(line_splitter)[0]
    room = room.split(line_splitter)[0]

    message = name+','+date+','+room
    return message

def convert_utf8mb3(content):
    global line_splitter
    content = convert2utf8mb4(content)
    return content

def readCSV_file(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            code[row[0]] = row[1:]

def convert2utf8mb4(utf8mb3):
    global line_splitter
    readCSV_file('./utf8mb3.csv')
    if len(utf8mb3.split(line_splitter)) > 1:
        content_lines = utf8mb3.split(line_splitter)
    else:
        content_lines = [utf8mb3]
    converted_content = ''

    #メールの各行ごと処理
    for content_line in content_lines:
        #返還後の文字列
        converted_line = ''
        
        #各行にutf8mb3の文字コードがあるか検索
        content_word_index = 0
        while content_word_index < len(content_line)-8:
            #もしくそutf8mb3の文字コードを探したら
            if(content_line[content_word_index] == '='and content_line[content_word_index+1].lower() == 'e' and content_line[content_word_index+3] == '=' and content_line[content_word_index+6] == '='):
                #一番最初の=は無視する
                string_code = "".join(content_line[content_word_index+1:content_word_index+8].lower())+'0'
                #=をスペースに書き換える
                string_code = string_code.replace('=',' ')
                converted_line = converted_line+code[string_code][int(content_line[content_word_index+8], 16)]
                #変換済みの残り部分は飛ばす
                content_word_index = content_word_index+9
            else:
                converted_line = converted_line + content_line[content_word_index]
                content_word_index = content_word_index+1

        while content_word_index < len(content_line):
            converted_line = converted_line + content_line[content_word_index]
            content_word_index = content_word_index+1
        converted_line = converted_line.replace(' ='+line_splitter,'')
        converted_content = converted_content+converted_line+line_splitter
    return converted_content

def convert_unicode2utf8(what_you_wanna_convert):
    readCSV_file('./unicode.csv')
    converted_result = ''

    word_index = 0
    while word_index < len(what_you_wanna_convert)-5:
    #もしくそ文字コードを探したら
        if(what_you_wanna_convert[word_index] == '='):
            #一番最初の=は無視する
            string_code = "".join(what_you_wanna_convert[word_index+1:word_index+6].lower())
            #=をスペースに書き換える
            string_code = string_code.replace('=',' ')
            converted_result = converted_result+code[string_code][0]
            #変換済みの残り部分は飛ばす
            word_index = word_index+6
        else:
            converted_result = converted_result + what_you_wanna_convert[word_index]
            word_index = word_index+1

    while word_index < len(what_you_wanna_convert):
        converted_result = converted_result + what_you_wanna_convert[word_index]
        word_index = word_index+1

    return converted_result
