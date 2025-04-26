#--- 課題 ---#
import json
import urllib.request
import os
import re

# Lambda コンテキストからリージョンを抽出
def extract_region_from_arn(arn):
    match = re.search('arn:aws:lambda:([^:]+):', arn)
    if match:
        return match.group(1)
    return "us-east-1"

# モデルID
MODEL_ID = os.environ.get("MODEL_ID", "us.amazon.nova-micro-v1:0")

def lambda_handler(event, context):
    try:
        # ngrokのURLを設定
        ngrok_url = "https://35eb-34-125-21-239.ngrok-free.app"
        
        print("Received event:", json.dumps(event))
        
        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']
        
        print("Processing message:", message)
        print("Using model:", MODEL_ID)
        
        # APIリクエストペイロードを作成
        payload = {
            "prompt": message,
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
        
        # API呼び出しURLを設定
        api_url = f"{ngrok_url}/generate"
        
        # POSTリクエストを送信
        request = urllib.request.Request(api_url, method="POST", headers={'Content-Type': 'application/json'}, data=json.dumps(payload).encode('utf-8'))
        
        with urllib.request.urlopen(request) as response:
            response_body = json.loads(response.read().decode())
        
        print("API response:", json.dumps(response_body, default=str))
        
        # アシスタントの応答を取得
        assistant_response = response_body.get('generated_text', '')
        
        # レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response
            })
        }
        
    except Exception as error:
        print("Error:", str(error))
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
#--- 課題 ---#