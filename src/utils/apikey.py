import json
from pathlib import Path
from .logging import logging_module

log = logging_module()
route = Path('src/credenciales/credentials.json')

def apiKey():
    try:
        log.info('Leyendo Crendenciales.')
        
        with route.open(mode='r', encoding='utf-8') as cred:
            path = json.load(cred)
            
            return path['apiweather']['apikey']
        
    except Exception as ex:
        log.error(f'Error al Leer Credenciales: {ex}')

