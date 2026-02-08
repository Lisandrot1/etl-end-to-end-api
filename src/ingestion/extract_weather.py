import requests
import os
import time
from utils.logging import logs_logging
from utils.date_part import date_parts
from utils.storage_handler import (
    read_data_to_parquet,
    save_to_json
)

log = logs_logging()

# Configuración de la API
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
def get_weather():
    log.info('Extracción del clima Weather')

    year, month, day = date_parts()
    apikey = os.environ['apiweather']
    
    # llamamos el parquet 
    read_data = read_data_to_parquet(
        f'silver/cities/year={year}/month={month}/day={day}'
    )
    # creamos una lista vacia para insertar ahi los json
    data = []
    #creamos los lotes (batch)
    batch_size = 500
    processed_rows = 0
    for i,columns in enumerate(read_data.itertuples(), start=1):
        params = {
            'lat': columns.lat,
            'lon': columns.lon,
            'appid': apikey,
            'units': 'metric',
            'lang': 'es'
        }
        try:
            res = requests.get(
                WEATHER_API_URL,
                params=params,
                timeout=10
            )
            res.raise_for_status()
            data.append(res.json())

            if len(data) == batch_size:
                processed_rows += batch_size
                save_to_json(
                    data,
                    f'bronze/weather/year={year}/month={month}/day={day}/weather_{processed_rows}.json'
                )
                data.clear()
                log.info(f'Datos Guardados: {processed_rows}')
        except requests.exceptions.RequestException as e:
            log.warning(
                f'Error al Traer Clima de  ciudades: {e}'
            )
            continue
    # Si quedaron registros sin alcanzar el tamaño de lote, los guardamos
    if data:
        processed_rows += len(data)
        save_to_json(
            data,
            f'bronze/weather/year={year}/month={month}/day={day}/weather_{processed_rows}.json'
        )
        data.clear()

    # Log final indicando que la extracción terminó
    log.info(f'Extracción del clima finalizada. Registros procesados: {processed_rows}')


