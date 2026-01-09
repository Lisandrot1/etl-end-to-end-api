from utils.logging import infra_logger
#from ingestion.extract_weather import get_weather
from ingestion.extract_cities import get_cities


log = infra_logger()


def main_pipeline():
    log.info('='*50)
    log.info('Iniciando Pipeline ETL')
    
    get_cities()
    
    


if __name__ == "__main__":
    main_pipeline()