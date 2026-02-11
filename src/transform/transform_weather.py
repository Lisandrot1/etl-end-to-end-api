from utils.logging import logs_logging
from utils.date_part import date_parts
import pandas as pd
from utils.storage_handler import (
    read_data,
    save_to_parquet
)

log = logs_logging()

def transforms_weather():
    year, month, day = date_parts()
    df = read_data(f'bronze/weather/year={year}/month={month}/day={day}')
    try:
        log.info('Transformando datos de Weather.')
        #ordanizamos el dt y cambiamos el nombre y el tipo de dato
        
        df['dt'] = pd.to_datetime(df['dt'], unit='s')
        df['date'] = df['dt'].dt.floor('D')
        df_normalized = pd.json_normalize(df.to_dict('records'))

        df_weather = pd.DataFrame({
            'date':df_normalized['date'],
            'lat':df_normalized['coord.lat'],
            'lon':df_normalized['coord.lon'],
            'temp': df_normalized['main.temp'],
            'feels_like': df_normalized['main.feels_like'],
            'humidity': df_normalized['main.humidity'],
            'weather_main': df_normalized['weather'].apply(lambda x: x[0]['main']),
            'weather_desc': df_normalized['weather'].apply(lambda x: x[0]['description']),
            'wind_speed': df_normalized['wind.speed']
            
        })

        save_to_parquet(
            df_weather,
            f'silver/weather/year={year}/month={month}/day={day}/weather.parquet'
        )
    except Exception as ex:
        log.error('Error al Transformar Weather', exc_info=True)
        raise ex