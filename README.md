・概要

居住中のシェアハウスに居住者の変動が頻繁なため、居住者の入れ替え管理自動化ツール開発。

・担当部分

GarbagePlan/src/send_tenant_move_info/

GarbagePlan/src/tenant_info_update/tenant_info_update/

GarbagePlan/src/tenant_move_info/

・前提条件

‐居住者の入居、退去の予告は数日前にメールにて通知される。

‐通知メールのContent-Transfer-Encodingはquoted-printableである。

・作動プロセス

1.事前にシェアハウス会社からの入居・退去の通知メール

2.SES（オレゴン）にて通知メールをS3 bucketに保持

3.Lambda（オレゴン）にてS3 bucket内通知メールを整形し新入居者又は退去者の情報抽出、

　SNSにてLambda（東京）に送信
 
4.Lambda（東京）にて臨時入居者テーブル（DynamoDB）に入居・退去予定保持

5.入居・退去当日の午前1時正式入居者テーブル（DynamoDB）に入居者の最新情報更新


・開発環境

‐AWS

    Lambda(Python3.6)
    
    DynamoDB
    
    SES
    
    SNS

・開発人数

2人
