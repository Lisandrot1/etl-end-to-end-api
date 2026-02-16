from utils.logging import logs_logging
from utils.date_part import date_parts
import pandas as pd
from utils.storage_handler import (
    read_data_to_json,
    save_to_parquet
)

log = logs_logging(__name__)

def transforms_weather():
    year, month, day = date_parts()
    df = read_data_to_json(f'bronze/weather/year={year}/month={month}/day={day}')
    try:
        log.info('Transformando datos de Weather.')
        #ordanizamos el dt y cambiamos el nombre y el tipo de dato
        
        df['dt'] = pd.to_datetime(df['dt'], unit='s')
        df['date'] = df['dt'].dt.floor('D')

        df_normalized = pd.json_normalize(df.to_dict('records'))

        df_weather = pd.DataFrame({
            'date': df_normalized['date'],
            'cityId': df_normalized['id'],
            'temp': df_normalized['main.temp'],
            'feels_like': df_normalized['main.feels_like'],
            'temp_min': df_normalized['main.temp_min'],
            'temp_max': df_normalized['main.temp_max'],
            'humidity': df_normalized['main.humidity'],
            'pressure': df_normalized['main.pressure'],
            'sea_level': df_normalized['main.sea_level'],
            'grnd_level': df_normalized['main.grnd_level'],
            'weather_main': df_normalized['weather'].apply(lambda x: x[0]['main']),
            'weather_desc': df_normalized['weather'].apply(lambda x: x[0]['description']),
            'wind_speed': df_normalized['wind.speed'],
            'wind_deg': df_normalized['wind.deg'],
            'wind_gust': df_normalized.get('wind.gust', pd.NA),  # Puede no estar siempre
            'clouds': df_normalized['clouds.all'],
            'rain_1h': df_normalized.get('rain.1h', 0),  # Asignar 0 si no hay lluvia
            'sunrise': df_normalized['sys.sunrise'],
            'sunset': df_normalized['sys.sunset'],
            'timezone': df_normalized['timezone']
        })

        save_to_parquet(
            df_weather,
            f'silver/weather/year={year}/month={month}/day={day}/weather.parquet'
        )
    except Exception as ex:
        log.error('Error al Transformar Weather', exc_info=True)
        raise ex