import requests
from utils.logging import ingestion_logger
from dotenv import dotenv_values

log = ingestion_logger()

api_key = dotenv_values('.env')

def get_weather():
    try:
        log.info('Extraccion Del Clima Weather!')
        
        keyapi = api_key.get('apiweather')

        url = f"https://api.openweathermap.org/data/2.5/weather?q=Vienna&appid={keyapi}"

        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            log.info('Extraccion Completado de Weather.')
            return data
        else:
            log.warning(f'Peticion de Usuario Fallido: {res.status_code}: {res.text}')
            
            return None
            
    except Exception as ex:
        log.error(f'Error al traer informacion del usuario: {ex}')