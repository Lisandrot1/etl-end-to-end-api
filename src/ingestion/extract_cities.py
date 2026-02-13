import requests
import time
import os
from datetime import datetime
from utils.logging import logs_logging
from utils.storage_handler import save_to_json
from utils.date_part import date_parts

log = logs_logging(__name__)

def get_cities():
    try:
        log.info('Iniciando Extraccion de Ciudades.')        
        maxRows = 1000
        startRows = 0
        
        year, month, day = date_parts()
        
        while True:
            
            params = {
                "featureClass": "P",
                "fcode": "PPL",
                "maxRows": maxRows,
                "startRow": startRows,
                "username": os.environ["username"]
            }
            
            res = requests.get(
                'http://api.geonames.org/searchJSON',
                params=params,
                timeout=30)
            
            if res.status_code == 200:
                
                data = res.json()
                geonames = data.get('geonames', [])
                
                if not geonames:
                    log.info('No hay mas ciudades. Extraccion completada')
                    break
                
                startRows += maxRows
                ## Llamamos a la funcion que guarda los datos crudos a minio
                save_to_json(
                    geonames,
                    f"bronze/cities/year={year}/month={month}/day={day}/cities_{startRows:05d}.json"
                )
                time.sleep(0.3)

            else:
                log.error('Error en la peticion de ciudades:',{res.status_code}, {res.text})
                break
            
    except Exception as ex:
        log.error(f'Error: {ex}', exc_info=True)
        raise ex
