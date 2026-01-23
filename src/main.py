from utils.logging import infra_logger
from ingestion.extract_cities import get_cities
#from transform.read_cities import read_cities
from transform.transform_cities import read_cities


log = infra_logger()


def main_pipeline():
    log.info('='*50)
    log.info('Iniciando Pipeline ETL')
    get_cities()

    
    


if __name__ == "__main__":
    main_pipeline()