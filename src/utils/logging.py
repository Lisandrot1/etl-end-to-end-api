import logging


def logging_module(name: str = __name__):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logging.basicConfig(
            
            level= logging.INFO,
            format="%(asctime)s %(name)s %(filename)s %(message)s",
            filename='logs.log',
            filemode='a'
            
            )
    
    return logger