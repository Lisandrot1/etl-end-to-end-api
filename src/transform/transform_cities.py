import pandas as pd
from utils.save_data_minio import client_create
from utils.config import config_env
from utils.logging import transform_logger
#from s3fs import S3FileSystem
log = transform_logger()

def read_cities():
    config = config_env()
    
    
    try:
        log.info('Iniciando a Leer datos de Bronze')
        
        df = pd.read_json(
            's3://etl-end-to-end/bronze/cities/cities_00000000.json',
            storage_options={
                'endpoint_url': config.get('minio_endpoint'),
                'key': config.get('access_key'),
                'secret': config.get('secret_key')
            }
        )
        
        print(df.head(10))
        return df
        
    except Exception as ex:
        log.error(f'Error al Leer datos de Bronze: {ex}')
        
    
    
    


