import logging
from pathlib import Path

LOG_PATH = Path("logs")

def _base_logger(name, file_name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        LOG_PATH.mkdir(exist_ok=True)

        handler = logging.FileHandler(LOG_PATH / file_name, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(filename)s | %(message)s"
        )
        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False

    return logger


def infra_logger():
    return _base_logger("INFRA", "infra.log")


def ingestion_logger():
    return _base_logger("INGESTION", "ingestion.log")


def transform_logger():
    return _base_logger("TRANSFORM", "transform.log")


