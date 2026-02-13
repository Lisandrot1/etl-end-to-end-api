from utils.logging import logs_logging
from utils.date_part import date_parts
from utils.storage_handler import (
    read_data_to_json,
    save_to_parquet
)


log = logs_logging(__name__)

        
    
def transform_cities(execution_date=None):
    try:
        year, month, day = date_parts(execution_date)
        df_cities = read_data_to_json(f'bronze/cities/year={year}/month={month}/day={day}')
        
        log.info('Transformando Datos a Parquet')
        
        df = df_cities[[
            'geonameId',
            'name',
            'countryId',
            'population',
            'countryCode',
            'countryName',
            'lat',
            'lng'
            ]].rename(columns={
                'geonameId':'cityId',
                'name':'Name_City',
                'countryCode':'Country_Code',
                'countryName':'Country_Name',
                'lng':'lon'
            })
            
        year, month, day = date_parts()        
        
        save_to_parquet(
            df,
            f'silver/cities/year={year}/month={month}/day={day}/cities.parquet'
        )
        
    except Exception as ex:
        log.error(f'Error En la Transformacion de Cities: {ex}')
        raise ex

