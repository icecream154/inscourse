import json
import requests


def do_request(request_type: str, url: str, params: dict = None, headers: dict = None, data: dict = None):
    response = requests.request(request_type, url, params=params, headers=headers, data=data)
    # print(response.request.headers)
    response_dict = None
    if response.status_code == 200:
        try:
            response_dict = json.loads(response.text)
        except json.decoder.JSONDecodeError as ex:
            print(ex)
    else:
        response_dict = response.text
    return response.status_code, response_dict
