from utils.save_data_minio import client_create
from pyspark.sql import SparkSession


def get_bucket():
    client = client_create()
        
    objects = client.list_objects(
        "etl-end-to-end",
        prefix='bronze/cities',
        recursive=True
        )

    for obj in objects:
        print(obj.object_name)

