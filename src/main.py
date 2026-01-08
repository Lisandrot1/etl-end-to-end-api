from utils.logging import logging_module
from ingestion.extract_weather import get_weather
from ingestion.extract_cities import get_cities
from transform.transform_cities import get_bucket


log = logging_module()


def main_pipeline():
    log.info('='*50)
    log.info('Iniciando Pipeline ETL')
    
    get_bucket()


if __name__ == "__main__":
    main_pipeline()