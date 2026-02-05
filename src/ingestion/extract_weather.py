import requests
import os
from datetime import datetime
from utils.logging import logs_logging
from utils.storage_handler import read_data

log = logs_logging()



def get_weather():
    
    try:
        log.info('Extraccion Del Clima Weather!')
        
        fecha = datetime.now()
        year = fecha.year
        month= f'{fecha.month:02d}'
        day= f'{fecha.day:02d}'
    
        
        apikey = os.environ['apiweather']
        lon = 40.71427
        lat = -74.00597
        maxRows = 1000
        
        url = f"https://api.openweathermap.org/data/2.5/weather"
        while True:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': apikey,
                'units': 'metric',
                'lang': 'es'
            }
            res = requests.get(url, params= params)

            if res.status_code == 200:
                data = res.json()
                log.info('Extraccion Completado de Weather.')
                print(data)
                return data
            else:
                log.warning(f'Peticion de Usuario Fallido: {res.status_code}: {res.text}')
                
                return None
            
    except Exception as ex:
        log.error(f'Error al traer informacion del usuario: {ex}')