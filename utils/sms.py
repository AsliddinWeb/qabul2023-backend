import json

import requests

from .eskiz_auth import eskiz_auth

def send_sms(phone_number, text, code, bearer_token):
    url = "https://notify.eskiz.uz/api/message/sms/send"

    payload = {'mobile_phone': phone_number[1:],
               'message': str(text).format(code),
               'from': '4546',
               'callback_url': 'http://qabul.xiuedu.uz/'}
    files = [

    ]
    headers = {
        'Authorization': f"Bearer {bearer_token}"
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return {
        'status_code': response.status_code,
        'data': json.loads(response.text)
    }
