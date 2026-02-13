import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logging import logs_logging
from utils.date_part import date_parts
from utils.storage_handler import (
    read_data_to_parquet,
    save_to_json
)

log = logs_logging()
def get_data_weather(rows,apikey, weather_url):
    params = {
            'id': rows.cityId,
            'appid': apikey,
            'units': 'metric',
            'lang': 'es'
        }

    try:
        res = requests.get(
            weather_url,
            params=params,
            timeout=10
        )
        res.raise_for_status()
        return {
                'status':'success',
                'data': res.json()
            }

    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'error': str(e),
            'id': rows.cityId
        }

'''def get_weather():

    try:

        log.info('Extracción del clima Weather')

        year, month, day = date_parts()

        print(year,month,day)
    except Exception as ex:
        log.error(f'error:{ex}')'''
        
def get_weather():

    try:
        WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
        log.info('Extracción del clima Weather')

        year, month, day = date_parts()
        apikey = os.environ['apiweather']

        # llamamos el parquet 
        read_data = read_data_to_parquet(
            f'silver/cities/year={year}/month={month}/day={day}'
        )

        #creamos los lotes (batch)

        batch_size = 500
        processed_rows = 0
        data = []
        max_workers = 15

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for row in read_data.itertuples():
                future = executor.submit(get_data_weather, row, apikey, WEATHER_API_URL)
                futures.append(future)

            completed = 0
            successful = 0
            failed = 0

            for future in as_completed(futures):
                result = future.result()
                completed+=1

                if result['status'] == 'success':
                    data.append(result['data'])
                    successful+=1
                else:
                    failed += 1

                if len(data) == batch_size:
                    processed_rows += batch_size
                    save_to_json(
                        data,
                        f'bronze/weather/year={year}/month={month}/day={day}/weather_{processed_rows}.json'
                    )
                    data.clear()
                    log.info(f'Datos Guardados: {processed_rows}')

        if data:
            processed_rows += len(data)
            save_to_json(
                data,
                f'bronze/weather/year={year}/month={month}/day={day}/weather_{processed_rows}.json'
            )
            data.clear()
            log.info(f'Datos Guardados: {processed_rows}')
            
    except Exception as ex:
        log.error(f'Error en la Extracion de Weather: {ex}', exc_info=True)
        raise