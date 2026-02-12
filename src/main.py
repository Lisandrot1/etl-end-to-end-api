from ingestion.extract_cities import get_cities
from ingestion.extract_weather import get_weather
from transform.transform_cities import transform_cities
from transform.transform_weather import transforms_weather
from loaders.laod_cities import main_gold
from utils.logging import logs_logging


log = logs_logging()

def main_pipeline():
    log.info('EJECUTANDO EN DOCKER.')
    try:
        log.info('='*50)
        log.info('Iniciando Pipeline ETL')
        get_cities()
        transform_cities()
        get_weather()
        transforms_weather()
        log.info('Termiando Pipeline.')
        log.info('='*50)

    except Exception as ex:
        log.error(f'Error al correr Pipeline: {ex}')
        raise ex
    


if __name__ == "__main__":
    main_pipeline()