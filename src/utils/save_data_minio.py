import io
import json
from minio import Minio
from utils.config import config_env
from .logging import ingestion_logger
from pathlib import Path

config = config_env()

log_ingestion = ingestion_logger()
bucket_name = config.get('bucket_name')


_minio_client = None

def client_create():
    global _minio_client  # Usamos la variable global
    
    # 2. Si ya existe el cliente, lo devolvemos sin crear uno nuevo
    if _minio_client is not None:
        return _minio_client
    
    log_ingestion.info('Creando Cliente Minio!')
    
    try:
        _minio_client = Minio(config.get('client'),
               access_key= config.get('access_key'),
               secret_key= config.get('secret_key'),
               secure= False)
        
        return _minio_client
    except Exception as ex:
        log_ingestion.error('Error al Crear Cliente Minio: {ex}')
        raise ex



def save_data_storage(data, route_path):
    path = Path(route_path).as_posix()

    try:
        client = client_create()
        found = client.bucket_exists(bucket_name)
        
        if not found:
            client.make_bucket(bucket_name)
            log_ingestion.info('Bucket Creado Correctamente.')
            
        else:
            log_ingestion.info('Bucket Encontrado Correctamente.')
        
        json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
        json_bytesid = io.BytesIO(json_bytes)
        
        
        client.put_object(
            
            bucket_name = bucket_name,
            object_name = path,
            data = json_bytesid,
            length = len(json_bytes),
            content_type = 'application/json'
        )
        
        log_ingestion.info(f'{path} Guardado Correctamente.')
        
    except Exception as ex:
        log_ingestion.error(f'Error al guardar a Minio: {ex}')
        
        raise ex



