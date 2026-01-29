import requests
from utils.logging import ingestion_logger
from utils.config import config_env
log = ingestion_logger()

config = config_env()

def get_weather():
    try:
        print('Extraccion Del Clima Weather!')
        
        keyapi = config.get('apiweather')

        url = f"https://api.openweathermap.org/data/2.5/weather?q=Vienna&appid={keyapi}"

        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            print('Extraccion Completado de Weather.')
            return data
        else:
            log.warning(f'Peticion de Usuario Fallido: {res.status_code}: {res.text}')
            
            return None
            
    except Exception as ex:
        log.error(f'Error al traer informacion del usuario: {ex}')