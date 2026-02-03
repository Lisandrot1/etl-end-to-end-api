import io
import json
import os
import boto3
import botocore
from .logging import logs_logging


  
bucket_name = os.environ["bucket_name"]
access_key = os.environ["access_key"]
secret_key = os.environ["secret_key"]
endpoint = os.environ["minio_endpoint"]

log = logs_logging()


_s3_client = None

def client_create():
    global _s3_client
    # 2. Si ya existe el cliente, lo devolvemos sin crear uno nuevo
    if _s3_client:
        return _s3_client

    try:
        log.info('Creando Cliente Minio!')
        _s3_client = boto3.client(
                's3',
                endpoint_url=endpoint,  
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name='us-east-1'
            )
        
        try:
            _s3_client.head_bucket(Bucket= bucket_name)
            
            log.info('Bucket Encontrado Correctamente')
        except botocore.exceptions.ClientError as ex:
            
            error_code = ex.responsep['Error']['Code']
            if error_code == '404':
                log.info('Bucket no existe. Creando...')
                # El método correcto es create_bucket
                
                _s3_client.create_bucket(Bucket=bucket_name)
                log.info('Bucket Creado Correctamente.')
            else:
                # Si es un error de permisos u otro, lanzarlo
                raise ex
            
        return _s3_client
    except Exception as ex:
        log.error(f'Error al Crear Cliente Minio: {ex}')
        raise ex

        
        
def save_to_json(data, route_path):
    path = route_path.replace(os.sep, '/')

    try:
        client = client_create()
        
        buffer = io.BytesIO()
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        buffer.write(json_data.encode('utf-8'))
        buffer.seek(0)
        
        
        client.put_object(
            Bucket = bucket_name,
            Key = path,
            Body = buffer,
            ContentType = 'application/json'
        )
        
    except Exception as ex:
        log.error(f'Error al guardar a Minio: {ex}')        
        raise ex


def save_to_parquet(data, route_path):
    path = route_path.replace(os.sep, '/')
    
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
            Bucket = bucket_name,
            Key = path,
            Body = buffer,
            ContentType = 'application/octet-stream'
        )
        log.info('Parquet Guardado Correctamente.')

    except Exception as ex:
        log.error(f'Error al Guardar parquet: {ex}')
        raise ex


