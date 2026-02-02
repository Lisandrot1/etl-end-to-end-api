import io
import json
import os
from minio import Minio
#from pyarrow import parquet
from .logging import logs_logging
from pathlib import Path



log = logs_logging()


bucket_name = os.environ["bucket_name"]


_minio_client = None

def client_create():
    global _minio_client
    # 2. Si ya existe el cliente, lo devolvemos sin crear uno nuevo
    if _minio_client:
        return _minio_client
    
    
    try:
        log.info('Creando Cliente Minio!')
        _minio_client = Minio(os.environ["client"],
               access_key= os.environ["access_key"],
               secret_key= os.environ["secret_key"],
               secure= False)
        
        found = _minio_client.bucket_exists(bucket_name)
        
        if not found:
            _minio_client.make_bucket(bucket_name)
            log.info('Bucket Creado Correctamente.')
        else:
           log.info('Bucket Encontrado Correctamente.')
        return _minio_client
    
    except Exception as ex:
        log.error(f'Error al Crear Cliente Minio: {ex}')
        raise ex

        
        
def save_data_storage(data, route_path):
    path = Path(route_path).as_posix()

    try:
        client = client_create()
        
        json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
        json_bytesid = io.BytesIO(json_bytes)
        
        
        client.put_object(
            bucket_name = bucket_name,
            object_name = path,
            data = json_bytesid,
            length = len(json_bytes),
            content_type = 'application/json'
        )
        
    except Exception as ex:
        log.error(f'Error al guardar a Minio: {ex}')
        
        raise ex

def save_to_parquet(data, route_path):
    path = Path(route_path).as_posix()
    
    try:
        client = client_create()
            
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
        
        log.info('Guardado Correctamente.')

        
    except Exception as ex:
        log.error(f'Error al Guardar parquet: {ex}')
        raise ex


