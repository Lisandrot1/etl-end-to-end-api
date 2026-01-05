import io
import json
from minio import Minio
from dotenv import dotenv_values
from .logging import logging_module
from pathlib import Path

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



def save_data_minio(data, route_path):
    path = Path(route_path).as_posix()

    try:
        client = client_create()
        found = client.bucket_exists(bucket_name)
        
        if not found:
            client.make_bucket(bucket_name)
            log.info('Bucket Creado Correctamente.')
            
        else:
            log.info('Bucket Encontrado Correctamente.')
        
        json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
        json_bytesid = io.BytesIO(json_bytes)
        
        
        client.put_object(
            
            bucket_name = bucket_name,
            object_name = path,
            data = json_bytesid,
            length = len(json_bytes),
            content_type = 'application/json'
        )
        
        log.info(f'{path} Guardado Correctamente.')
        
    except Exception as ex:
        log.error(f'Error al guardar a Minio: {ex}')
        raise ex