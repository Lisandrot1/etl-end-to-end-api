from dotenv import dotenv_values
from pyspark.sql import SparkSession
from pathlib import Path

path = Path('notebooks/colombia.csv')
config = dotenv_values('.env')

def get_session():
    return SparkSession.builder \
        .appName("etl-end-to-end-api") \
        .getOrCreate()


def get_read_data():
    spSession = get_session()

    df = spSession.read.csv(str(path), header=True, sep=',')

    # Mostrar los datos
    print(df.columns)
    



if __name__ == "__main__":
    print('Inicio Data Read')
    get_read_data()
