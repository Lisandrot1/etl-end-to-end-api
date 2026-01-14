import requests
import time
from utils.config import config_env
from utils.logging import ingestion_logger
from utils.save_data_minio import save_data_storage


log = ingestion_logger()
config = config_env()

username = config.get('username')

def get_cities():
    try:
        log.info('Iniciando Extraccion de Ciudades.')
        
        url = 'http://api.geonames.org/searchJSON'
        
        maxRows = 1000
        startRows = 0
        total_extraido = 0
        
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
                    log.info(f'No hay mas ciudades. Extraccion completada con {total_extraido} ciudades.')
                    break
                
                save_data_storage(
                    geonames,
                    f"bronze/cities/cities_{startRows:08d}.json"
                )
                
                total_extraido += len(geonames)
                log.info(f"Guardadas {len(geonames)} ciudades desde startRow={startRows} (Total: {total_extraido})")
                
                startRows += maxRows
                time.sleep(0.3)

            else:
                log.error(f'Error en la peticion de ciudades: {res.status_code}: {res.text}')
                break
            
    except Exception as ex:
        log.error(f'Error: {ex}')
        raise ex
