from minio import Minio
from dotenv import dotenv_values
from .logging import logging_module

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



