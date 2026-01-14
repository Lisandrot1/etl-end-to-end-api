from dotenv import dotenv_values
from utils.logging import infra_logger

log = infra_logger()

def config_env():
    return dotenv_values('.env')
