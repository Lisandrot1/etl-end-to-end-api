from datetime import datetime


def date_parts(executon=None):
    
    fecha = executon or datetime.now()
    year = fecha.year
    month= f'{fecha.month:02d}'
    day= f'{fecha.day:02d}'
    
    return year, month, day