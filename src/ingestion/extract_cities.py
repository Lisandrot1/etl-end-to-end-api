import requests
import time
import os
from datetime import datetime
from utils.logging import logs_logging
from utils.storage_handler import save_to_json

log = logs_logging()


username = os.environ["username"]

def get_cities():
    try:
        log.info('Iniciando Extraccion de Ciudades.')
        
        url = 'http://api.geonames.org/searchJSON'
        
        maxRows = 1000
        startRows = 0
        
        execution_date = datetime.now().strftime("%Y-%m-%d")

        
        while True:
            
            params = {
                "featureClass": "P",
                "fcode": "PPL",
                "maxRows": maxRows,
                "startRow": startRows,
                "username": username
            }
            
            res = requests.get(url, params=params, timeout=30)
            
            if res.status_code == 200:
                
                data = res.json()
                geonames = data.get('geonames', [])
                
                if not geonames:
                    log.info('No hay mas ciudades. Extraccion completada')
                    break
                
                startRows += maxRows
                ## Llamamos a la funcin que guarda los datos crudos a minio
                save_to_json(
                    geonames,
                    f"bronze/cities/execution_date={execution_date}/cities_{startRows:05d}.json"
                )
                time.sleep(0.3)

            else:
                log.error('Error en la peticion de ciudades:',{res.status_code}, {res.text})
                break
            
    except Exception as ex:
        log.error('Error:', exc_info=True)
        raise ex
