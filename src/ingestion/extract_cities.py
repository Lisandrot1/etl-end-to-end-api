import requests
from dotenv import dotenv_values
from utils.logging import logging_module
from utils.save_data_minio import save_data_minio


log = logging_module()
config = dotenv_values('.env')

username = config.get('username')

def get_cities():
    try:
        log.info('Iniciando Extraccion de Ciudades.')
        
        url = f'http://api.geonames.org/searchJSON'
        
        maxRows = 1000
        startRows = 0
        
        params = {
            "featureClass": "P",
            "fcode": "PPL",
            "maxRows": maxRows,
            "startRow": startRows,
            "username": f"{username}"
        }
        
        res = requests.get(url, params=params)
        
        
        if res.status_code == 200:
            
            data = res.json()
            startRows += maxRows
            
            log.info('Extraccion Completado de Ciudades.')
            
            save_data_minio(
                data,
                "bronze/cities/cities.json"
            )
        else:
            log.error(f'Error falla en la peticion: {res.status_code}: {res.text}')
            
    except Exception as ex:
        log.error(f'error :{ex}')
        raise ex
        

