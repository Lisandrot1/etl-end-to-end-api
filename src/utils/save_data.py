from minio import Minio
from dotenv import dotenv_values
from .logging import logging_module
#from pathlib import Path

config = dotenv_values('.env')
log = logging_module()
bucket_name = config.get('bucket_name')


def client_create():
    log.info('Creando Cliente Minio!')
    try:
        client = Minio(config.get('client'),
               access_key=config.get('access_key'),
               secret_key=config.get('secret_key'),
               secure=False)
        
        return client
    except Exception as ex:
        log.error('Error al Crear Cliente Minio: {ex}')
        raise ex



def save_data_minio():
    object_name = 'bronze/text.txt'
    file_path = 'text.txt'
    
    
    
    try:
        client = client_create()
        found = client.bucket_exists(bucket_name)
        
        if not found:
            client.make_bucket(bucket_name)
            log.info('Bucket Creado Correctamente.')
        else:
            log.info('Bucket Encontrado Correctamente.')
            
        client.fput_object(
            bucket_name,
            object_name,
            file_path
        )
    except Exception as ex:
        log.error(f'Error al guardar a Minio: {ex}')