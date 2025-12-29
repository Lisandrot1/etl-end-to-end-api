import requests
from utils.logging import logging_module
from utils.apikey import apiKey

log = logging_module()



def get_users():
    try:
        log.info('trayendo informacion del usuario!')
        keyapi = apiKey()

        url = f"https://api.openweathermap.org/data/2.5/weather?q=Madrid&appid={keyapi}"

        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            print(data)
            return data
        else:
            log.warning(f'Peticion de Usuario Fallido: {res.status_code}: {res.text}')
            
            return None
            
    except Exception as ex:
        log.error(f'Error al traer informacion del usuario: {ex}')