import json
from json import JSONDecodeError

import requests


def get_person_api(dni):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token fc062659199a099fade617ceaebfa803308472bb'
    }
    r = requests.get('https://dni.optimizeperu.com/api/prod/persons/' + dni, headers=headers)
    try:
        response_dict = json.loads(r.text)
        return response_dict
    except JSONDecodeError:
        return {"dni": "xxxxx", "name": "xxxxx", "first_name": "xxxxx", "last_name": "xxxxx", "cui": "xxxxx"}
