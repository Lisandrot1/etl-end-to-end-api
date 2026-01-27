import pandas as pd
import s3fs
from utils.config import config_env
#from utils.logging import transform_logger



def read_cities():
    config = config_env()
    
    bucketname  = config.get('bucket_name')
    access_key = config.get('access_key')
    secret_key = config.get('secret_key')
    endpoint = config.get("minio_endpoint")
    try:
        fs = s3fs.S3FileSystem(
            key=access_key,
            secret=secret_key,
            client_kwargs={
                "endpoint_url": endpoint
            }
        )
        
        path = f'{bucketname}/bronze/cities/insget_date=2026-01-01/*.json'
        
        dfs = []
        for file in fs.glob(path):
            with fs.open(file) as f:
                df = pd.read_json(f)    
                dfs.append(df)
                print('dataframe',df)
        
    except Exception as ex:
        print(f'Error al Leer datos de Bronze: {ex}')
        
    
    
    


