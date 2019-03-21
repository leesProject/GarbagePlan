・概要

居住中シェアハウスに居住者の入れ替えが頻繁なため、居住者の入れ替え管理自動化ツール開発。

・担当部分

GarbagePlan/src/send_tenant_move_info/

GarbagePlan/src/tenant_info_update/tenant_info_update/

GarbagePlan/src/tenant_move_info/

・前提条件

‐居住者の入居、退居の予告は数日前にメールにて通知される。

‐通知メールのContent-Transfer-Encodingはquoted-printableである。

・開発環境

‐AWS

    Lambda(Python3.6)
    
    DynamoDB
    
    SES
    
    SNS

・開発人数

2人
