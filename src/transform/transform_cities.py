import os
from utils.logging import logs_logging
from utils.storage_handler import save_to_parquet
from utils.storage_handler import read_data

log = logs_logging()


        
    
def transform_cities():
    try:
        df_cities = read_data('bronze/cities/execution_date=2026-02-02')
        
        log.info('Transformando Datos a Parquet')
        
        df = df_cities[[
            'geonameId',
            'name',
            'countryCode',
            'lat',
            'lng'
            ]].rename(columns={
                'geonameId': 'city_id',
                'name': 'name_city',
                'countryCode': 'country_code',
                'lng': 'lon'
            })
        
        save_to_parquet(
            df,
            f'silver/cities/current/cities.parquet'
        )
        
    except Exception as ex:
        log.error(f'Error En la Transformacion de Cities: {ex}')
        raise ex

