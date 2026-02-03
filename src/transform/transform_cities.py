import pandas as pd
import boto3
import os
from io import BytesIO
from utils.logging import logs_logging
from utils.save_data_minio import save_to_parquet

log = logs_logging()

def read_cities():
    
    
    bucketname  = os.environ["bucket_name"]
    access_key = os.environ["access_key"]
    secret_key = os.environ["secret_key"]
    endpoint = os.environ["minio_endpoint"]
    
    try:
        log.info('Leyendo Datos de Bronze.')
        s3 = boto3.client(
            's3',
            endpoint_url=endpoint,  
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='us-east-1'
        )
       
        prefix = 'bronze/cities/execution_date=2026-02-02'
        
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
        
        return final_df
        
    except Exception as ex:
        log.error(f'Error al Leer datos de Bronze: {ex}')
        raise ex
        
    
def transform_cities():
    try:
        df_cities = read_cities()
        
        log.info('Transformando Datos a Parquet')
        
        df = df_cities[['name']]
        
        save_to_parquet(
            df,
            f'silver/cities/current/cities.parquet'
        )
        
    except Exception as ex:
        log.error(f'Error En la Transformacion de Cities: {ex}')
        raise ex

