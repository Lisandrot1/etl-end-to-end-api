from ingestion.extract_cities import get_cities
from transform.transform_cities import transform_cities





def main_pipeline():
    print('EJECUTANDO EN DOCKER.')
    try:
        print('='*50)
        print('Iniciando Pipeline ETL')
        get_cities()
        transform_cities()
        
        print('Termiando Pipeline.')
    except Exception as ex:
        print(f'Error al correr Pipeline: {ex}')
        raise ex
    


if __name__ == "__main__":
    main_pipeline()