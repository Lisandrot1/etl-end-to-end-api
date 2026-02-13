from datetime import datetime, timedelta


def date_parts(executon=None):
    
    fecha = executon or (datetime.utcnow() - timedelta(hours=5))
    year = fecha.year
    month= f'{fecha.month:02d}'
    day= f'{fecha.day:02d}'
    
    return year, month, day