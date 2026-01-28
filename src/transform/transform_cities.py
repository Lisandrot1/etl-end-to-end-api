import pandas as pd
import boto3
from io import BytesIO
from utils.config import config_env
from utils.logging import transform_logger
from utils.save_data_minio import save_to_parquet

log = transform_logger()

def read_cities():
    config = config_env()
    
    bucketname  = config.get('bucket_name')
    access_key = config.get('access_key')
    secret_key = config.get('secret_key')
    endpoint = config.get("minio_endpoint")
    
    try:
        log.info('Iniciando con Lectura de datos.')
        s3 = boto3.client(
            's3',
            endpoint_url=endpoint,  
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='us-east-1'
        )
       
        prefix = 'bronze/cities/ingest_date=2026-01-01'
        
        response = s3.list_objects_v2(
            Bucket=bucketname,
            Prefix = prefix
        )
        dfs = []
        if 'Contents' in response:
            for meta in response.get('Contents', []):
                key = meta["Key"]
                obj = s3.get_object(Bucket=bucketname, Key=key)
                data = obj["Body"].read()

                df = pd.read_json(BytesIO(data))
                dfs.append(df)
        else:
                log.error("No files found in the bucket.")
                
        final_df = pd.concat(dfs, ignore_index=True)
        
        log.info('Finalizacion Lectura de Datos bronze')
        return final_df
        
    except Exception as ex:
        log.error(f'Error al Leer datos de Bronze: {ex}')
        raise ex
        
    
def transform_cities():
    try:
        df_cities = read_cities()
        
        log.info('Inicando Transformacion de datos.')
        
        df = df_cities[['name']]
        
        save_to_parquet(
            df,
            f'silver/cities/current/cities.parquet'
        )
        
    except Exception as ex:
        log.error(f'Error En la Transformacion de Cities: {ex}')
        raise ex

