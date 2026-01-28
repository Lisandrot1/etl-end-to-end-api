from utils.logging import infra_logger
#from ingestion.extract_cities import get_cities
from transform.transform_cities import transform_cities


log = infra_logger()


def main_pipeline():
    try:
        log.info('='*50)
        log.info('Iniciando Pipeline ETL')
        transform_cities()
        
        log.info('Termiando Pipeline.')
    except Exception as ex:
        log.error(f'Error al correr Pipeline: {ex}')
        raise ex
    


if __name__ == "__main__":
    main_pipeline()