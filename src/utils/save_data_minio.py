import io
import json
import os
from minio import Minio
from pyarrow import parquet
from .logging import ingestion_logger, transform_logger
from pathlib import Path



log_ingestion = ingestion_logger()
log_transform = transform_logger()

bucket_name = os.environ["bucket_name"]


_minio_client = None

def client_create():
    global _minio_client  # Usamos la variable global
    
    # 2. Si ya existe el cliente, lo devolvemos sin crear uno nuevo
    if _minio_client is not None:
        return _minio_client
    
    log_ingestion.info('Creando Cliente Minio!')
    
    try:
        _minio_client = Minio(os.environ["client"],
               access_key= os.environ["access_key"],
               secret_key= os.environ["secret_key"],
               secure= False)
        
        return _minio_client
    except Exception as ex:
        log_ingestion.error('Error al Crear Cliente Minio: {ex}')
        raise ex

def client_bucket_exist():
    try:
        # llamamos al cliente de minio
        client = client_create()
        found = client.bucket_exists(bucket_name)
        # miramos si el bucket si exista

        if not found:
            client.make_bucket(bucket_name)
            log_ingestion.info('Bucket Creado Correctamente.')
        else:
            log_ingestion.info('Bucket Encontrado Correctamente.')
        
        return client
    except Exception as ex:
        log_transform.error(f'Error en el cliente y en la busqueda de bucket.')
        
        
def save_data_storage(data, route_path):
    path = Path(route_path).as_posix()

    try:
        client = client_bucket_exist()
        
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

def save_to_parquet(data, route_path):
    path = Path(route_path).as_posix()
    
    try:
        client = client_bucket_exist()
            
        # esto crea un contenedor en memoria
        buffer = io.BytesIO()
        # con esto escribimos los bytes dentro de buffer que es el contenedor de bytes
        data.to_parquet(buffer, engine='pyarrow')
        #vuelve al inicio del archivo
        buffer.seek(0)

        # Lee y escribe los archivos y los sube a minio s3.
        client.put_object(
            bucket_name = bucket_name,
            object_name = path,
            data = buffer,
            length =buffer.getbuffer().nbytes ,
            content_type = 'application/octet-stream'
        )
        
        log_transform.info('Guardado Correctamente.')
        log_transform.info('='*50)

        
    except Exception as ex:
        log_transform.error(f'Error al Guardar parquet: {ex}')
        raise ex


