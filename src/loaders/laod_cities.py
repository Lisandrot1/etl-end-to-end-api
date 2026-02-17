from utils.logging import logs_logging
from utils.date_part import date_parts
from utils.storage_handler import (
    read_data_to_parquet,
    save_to_parquet
 )

log = logs_logging(__name__)
year, month, day = date_parts()

def dim_cities(df):
    try:
        dim_cities = df[['cityId', 'countryId', 'Name_City', 'population', 'lat', 'lon']] \
                .drop_duplicates(subset=['cityId'])
                
       
        save_to_parquet(
            dim_cities,
            'gold/dim_citie/dim_citie.parquet',
            show_log=False
        )
        return dim_cities
    
    except Exception as ex:
        log.error(f'ERROR en dim_cities: {ex}', exc_info=True)

def dim_country(df):
    try:
        
        df_country = df[['countryId', 'Country_Code', 'Country_Name']]
        df_unique_country = df_country.drop_duplicates(subset=['countryId']).copy()
        
        save_to_parquet(
            df_unique_country,
            'gold/dim_country/dim_country.parquet',
            show_log=False
        )
        return df_unique_country
    
    except Exception as ex:
        log.error(f'ERROR em dim_country: {ex}', exc_info=True)
        

def fact_weather(df_weather, df_cities):
    try:
        df_weather = df_weather[[
            'date',
            'cityId',
            'timezone',
            'temp',
            'feels_like',
            'temp_min',
            'temp_max',
            'weather_main',
            'weather_desc',
            'clouds',
            'humidity',
            'pressure',
            'sea_level',
            'grnd_level',
            'wind_speed',
            'wind_deg',
            'wind_gust',
            'rain_1h',
            'sunrise',
            'sunset']]

        fact_weather = df_weather.merge(
            df_cities[['cityId']],
            on=['cityId'],
            how='left'
        )

        save_to_parquet(
            fact_weather,
            f'gold/fact_weather/year={year}/month={month}/day={day}/fact_weather.parquet',
            show_log=False
        )
    except Exception as ex:
        log.error(f'ERROR al Convertir Fact_Weather: {ex}',  exc_info=True)



def main_gold():
    try:
        cities = read_data_to_parquet(f'silver/cities/year={year}/month={month}/day={day}')
        weather = read_data_to_parquet(f'silver/weather/year={year}/month={month}/day={day}')
        dim_cities(cities)
        dim_country(cities)
        fact_weather(weather, cities)
        log.info('Capa Gold finalizada con exito.')
    except Exception as ex:
        log.error(f'Error en orquestacion de gold: {ex}', exc_info=True)