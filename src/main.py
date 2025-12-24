from utils.logging import logging_module
from utils.save_data import save_data_minio

log = logging_module()


def main_pipeline():
    save_data_minio()
    


if __name__ == "__main__":
    main_pipeline()