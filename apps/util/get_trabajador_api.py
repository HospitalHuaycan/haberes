import json
from json import JSONDecodeError

import requests


def get_trabajador_api_by_plaza(plaza):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token c87bb8f86be0e5058718352485e6a5b791dd1286'
    }
    r = requests.get('http://api.dirislimasur.gob.pe:8080/api/trabajador/trabajador/?plaza=' + plaza, headers=headers)
    try:
        response_dict = json.loads(r.text)
        return response_dict
    except JSONDecodeError:
        return {"url": "xxxxx", "id": "xxxxx", "tipo": "xxxxx", "apellidos_nombre": "xxxxx", "plaza": "xxxxx"}


# response = get_trabajador_api_by_plaza('113643')
# trabajador = response['results'][0]
# print(trabajador['url'])
# print(trabajador['tipo'])
# print(trabajador['dni'])
# print(trabajador['apellidos_nombres'])
# print(trabajador['fecha_nacimiento'])
# print(trabajador['plaza'])
# print(trabajador['cargo'])
# print(trabajador['depedencia']['id'])
