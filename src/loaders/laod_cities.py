from utils.logging import logs_logging
from utils.date_part import date_parts
from utils.storage_handler import (
    read_data_to_parquet,
    save_to_parquet
 )

log = logs_logging()
year, month, day = date_parts()

def dim_cities(df):
    try:
        log.info('creando')
        dim_cities = df[['cityId', 'Name_City', 'population', 'lat', 'lon']] \
                .drop_duplicates(subset=['cityId'])
        save_to_parquet(
            dim_cities,
            'gold/dim_citie/dim_citie.parquet'
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
            'gold/dim_country/dim_country.parquet'
        )
        return df_unique_country
    
    except Exception as ex:
        log.error(f'ERROR em dim_country: {ex}', exc_info=True)
        
        
def dim_date(df):
    try:
        df_date = df[['date_id','date']].drop_duplicates().copy()

        df_date['year'] = df_date['date'].dt.year
        df_date['month'] = df_date['date'].dt.month
        df_date['day'] = df_date['date'].dt.day
        
        dim_date = df_date[['date_id','date','year','month','day']]
        
        save_to_parquet(
            dim_date,
            'gold/dim_date/dim_date.parquet'
        )
        return dim_date
    except Exception as ex:
        log.error(f'ERROR al Crear Dim_Date: {ex}', exc_info=True)


def fact_weather(df_weather, df_cities):
    try:
        df_weather = df_weather[['date_id','lat','lon','temp','feels_like','humidity','weather_main','weather_desc','wind_speed']]
        
        df_weather['lat'] = df_weather['lat'].round(4)
        df_weather['lon'] = df_weather['lon'].round(4)
        
        df_cities['lat'] = df_cities['lat'].round(4)
        df_cities['lon'] = df_cities['lon'].round(4)
        fact = df_weather.merge(
            df_cities[['cityId', 'lat', 'lon']],
            on=['lat','lon'],
            how='left'
        )
        
        fact_weather = fact[[
            'cityId',
            'date_id',
            'temp',
            'feels_like',
            'humidity',
            'weather_main',
            'weather_desc',
            'wind_speed'
        ]]
        if fact['cityId'].isna().sum() > 0:
            raise ValueError("Hay registros sin cityId después del merge")
        
        save_to_parquet(
            fact_weather,
            f'gold/fact_weather/year={year}/month={month}/day={day}/fact_weather.parquet'
        )
    except Exception as ex:
        log.error(f'ERROR al Convertir Fact_Weather: {ex}',  exc_info=True)



def main_gold():
    try:
        cities = read_data_to_parquet(f'silver/cities/year={year}/month={month}/day={day}')
        weather = read_data_to_parquet(f'silver/weather/year={year}/month={month}/day={day}')
        dim_cities(cities)
        dim_country(cities)
        dim_date(weather)
        fact_weather(weather, cities)
    except Exception as ex:
        log.error(f'Error en orquestacion de gold: {ex}', exc_info=True)