import requests
import pandas as pd
from dotenv import dotenv_values

config = dotenv_values('.env')

username = config.get('username')

url = f'http://api.geonames.org/searchJSON?featureClass=P&fcode=PPL&maxRows=10&username={username}'

def cities():
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # convertimos el resultado de la api en un dataframe, para sacar las ciudades
            df = pd.json_normalize(data['geonames'])
            df_name_citys = df['name']
            print(df_name_citys)
            
        else:
            print(f'Error falla en la peticion: {res.status_code}: {res.text}')
    except Exception as ex:
        print(f'error :{ex}')
        raise ex
        

        
cities()

