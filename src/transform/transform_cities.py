from utils.logging import logs_logging
from utils.date_part import date_parts
from utils.storage_handler import (
    read_data,
    save_to_parquet
)


log = logs_logging()

        
    
def transform_cities(execution_date=None):
    try:
        year, month, day = date_parts(execution_date)
        df_cities = read_data(f'bronze/cities/year={year}/month={month}/day={day}')
        
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
            
        year, month, day = date_parts()        
        
        save_to_parquet(
            df,
            f'silver/cities/year={year}/month={month}/day={day}/cities.parquet'
        )
        
    except Exception as ex:
        log.error(f'Error En la Transformacion de Cities: {ex}')
        raise ex

