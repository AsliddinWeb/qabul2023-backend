import json

import requests

def eskiz_auth(email, password):
    url = "https://notify.eskiz.uz/api/auth/login"

    if email and password:
        payload = {'email': email,
                   'password': password}
    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return json.loads(response.text).get('data').get('token')
