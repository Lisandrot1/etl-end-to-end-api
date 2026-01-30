import requests
import time
import os
from datetime import datetime
from utils.logging import ingestion_logger
from utils.save_data_minio import save_data_storage


log = ingestion_logger()


username = os.environ["username"]

def get_cities():
    try:
        print('Iniciando Extraccion de Ciudades.')
        
        url = 'http://api.geonames.org/searchJSON'
        
        maxRows = 1000
        startRows = 0
        total_extraido = 0
        
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
                    print(f'No hay mas ciudades. Extraccion completada con {total_extraido} ciudades.')
                    print('='*50)
                    break
                
                
                
                total_extraido += len(geonames)
                print(f"Guardadas {len(geonames)} (Total: {total_extraido})")
                
                startRows += maxRows
                ## Llamamos a la funcin que guarda los datos crudos a minio
                save_data_storage(
                    geonames,
                    f"bronze/cities/execution_date={execution_date}/cities_{startRows:05d}.json"
                )
                
                time.sleep(0.3)

            else:
                print(f'Error en la peticion de ciudades: {res.status_code}: {res.text}')
                break
            
    except Exception as ex:
        print(f'Error: {ex}')
        raise ex
