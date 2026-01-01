from utils.logging import logging_module
from ingestion.ingesta import get_users
from ingestion.ingesta_citys import get_cities


log = logging_module()


def main_pipeline():
    log.info('='*50)
    log.info('Iniciando Pipeline ETL')
    get_users()
    get_cities()


if __name__ == "__main__":
    main_pipeline()