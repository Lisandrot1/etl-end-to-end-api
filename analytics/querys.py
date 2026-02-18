from utils import date_parts
from db import conn_duckdb

year, month, day = date_parts()

def execute_query(query):
    """Ejecuta query y retorna resultado usando la conexión configurada"""
    conn = conn_duckdb()
    result = conn.execute(query).fetchdf()
    conn.close()
    return result

# ==========================================
# MÉTRICAS GLOBALES DEL DÍA
# ==========================================

def temperatura_global_promedio():
    """Temperatura promedio global del día"""
    query = f"""
        SELECT 
            ROUND(AVG(temp), 2) as temp_promedio,
            ROUND(AVG(feels_like), 2) as sensacion_termica,
            COUNT(*) as total_ciudades
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet')
    """
    return execute_query(query)

def ciudad_mas_caliente():
    """Ciudad con temperatura más alta del día"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            f.temp,
            f.feels_like,
            f.humidity
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        ORDER BY f.temp DESC
        LIMIT 1
    """
    return execute_query(query)

def ciudad_mas_fria():
    """Ciudad con temperatura más baja del día"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            f.temp,
            f.feels_like,
            f.humidity
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        ORDER BY f.temp ASC
        LIMIT 1
    """
    return execute_query(query)

def ciudad_mas_humeda():
    """Ciudad con mayor humedad del día"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            f.humidity,
            f.temp,
            f.weather_main as condicion
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        ORDER BY f.humidity DESC
        LIMIT 1
    """
    return execute_query(query)

def ciudad_mas_seca():
    """Ciudad con menor humedad del día"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            f.humidity,
            f.temp,
            f.weather_main as condicion
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        ORDER BY f.humidity ASC
        LIMIT 1
    """
    return execute_query(query)

def ciudad_vientos_mas_fuertes():
    """Ciudad con vientos más fuertes del día"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            ROUND(f.wind_speed, 2) as velocidad_viento,
            ROUND(f.wind_gust, 2) as rafaga_viento,
            f.temp
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        ORDER BY f.wind_speed DESC
        LIMIT 1
    """
    return execute_query(query)

def ciudad_mayor_lluvia():
    """Ciudad con mayor precipitación del día"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            f.rain_1h,
            f.temp,
            f.humidity,
            f.weather_desc
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        WHERE f.rain_1h > 0
        ORDER BY f.rain_1h DESC
        LIMIT 1
    """
    return execute_query(query)

def rango_termico_global():
    """Diferencia entre temperatura máxima y mínima del día"""
    query = f"""
        SELECT 
            ROUND(MAX(temp), 2) as temp_maxima,
            ROUND(MIN(temp), 2) as temp_minima,
            ROUND(MAX(temp) - MIN(temp), 2) as rango_termico
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet')
    """
    return execute_query(query)

# ==========================================
# TOP RANKINGS
# ==========================================

def top_ciudades_calientes(limit=10):
    """Top N ciudades más calientes del día"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            ROUND(f.temp, 1) as temperatura,
            ROUND(f.feels_like, 1) as sensacion_termica,
            f.humidity as humedad
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        ORDER BY f.temp DESC
        LIMIT {limit}
    """
    return execute_query(query)

def top_ciudades_frias(limit=10):
    """Top N ciudades más frías del día"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            ROUND(f.temp, 1) as temperatura,
            ROUND(f.feels_like, 1) as sensacion_termica,
            f.humidity as humedad
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        ORDER BY f.temp ASC
        LIMIT {limit}
    """
    return execute_query(query)

def top_paises_por_temperatura(limit=10):
    """Top N países por temperatura promedio del día"""
    query = f"""
        SELECT 
            p.Country_Name,
            ROUND(AVG(f.temp), 2) as temp_promedio,
            COUNT(*) as num_ciudades
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        GROUP BY p.Country_Name
        ORDER BY temp_promedio DESC
        LIMIT {limit}
    """
    return execute_query(query)

# ==========================================
# CONDICIONES CLIMÁTICAS
# ==========================================

def distribucion_condiciones_climaticas():
    """Distribución de condiciones climáticas del día"""
    query = f"""
        SELECT 
            weather_main as condicion,
            COUNT(*) as num_ciudades,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as porcentaje
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet')
        GROUP BY weather_main
        ORDER BY num_ciudades DESC
    """
    return execute_query(query)

def ciudades_con_lluvia():
    """Total de ciudades con lluvia del día"""
    query = f"""
        SELECT 
            COUNT(*) as total_ciudades_lluvia,
            ROUND(AVG(rain_1h), 2) as precipitacion_promedio
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet')
        WHERE rain_1h > 0 OR weather_main = 'Rain'
    """
    return execute_query(query)

def metricas_atmosfericas():
    """Métricas atmosféricas promedio del día"""
    query = f"""
        SELECT 
            ROUND(AVG(humidity), 2) as humedad_promedio,
            ROUND(AVG(pressure), 2) as presion_promedio,
            ROUND(AVG(wind_speed), 2) as velocidad_viento_promedio,
            ROUND(AVG(clouds), 2) as nubosidad_promedio
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet')
    """
    return execute_query(query)

# ==========================================
# RESUMEN DEL DÍA
# ==========================================

def resumen_completo_dia():
    """Resumen completo de métricas del día"""
    query = f"""
        SELECT 
            COUNT(*) as total_ciudades,
            COUNT(DISTINCT c.countryId) as total_paises,
            ROUND(AVG(f.temp), 2) as temp_promedio,
            ROUND(MIN(f.temp), 2) as temp_minima,
            ROUND(MAX(f.temp), 2) as temp_maxima,
            ROUND(AVG(f.humidity), 2) as humedad_promedio,
            ROUND(AVG(f.pressure), 2) as presion_promedio,
            ROUND(AVG(f.wind_speed), 2) as viento_promedio,
            SUM(CASE WHEN f.rain_1h > 0 THEN 1 ELSE 0 END) as ciudades_con_lluvia,
            SUM(CASE WHEN f.temp > 40 THEN 1 ELSE 0 END) as ciudades_calor_extremo,
            SUM(CASE WHEN f.temp < 0 THEN 1 ELSE 0 END) as ciudades_frio_extremo,
            SUM(CASE WHEN f.wind_speed > 15 THEN 1 ELSE 0 END) as ciudades_viento_fuerte
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
    """
    return execute_query(query)

def ciudades_por_rango_temperatura():
    """Distribución de ciudades por rangos de temperatura"""
    query = f"""
        SELECT 
            CASE 
                WHEN temp < 0 THEN 'Bajo Cero'
                WHEN temp >= 0 AND temp < 10 THEN 'Frío (0-10°C)'
                WHEN temp >= 10 AND temp < 20 THEN 'Templado (10-20°C)'
                WHEN temp >= 20 AND temp < 30 THEN 'Cálido (20-30°C)'
                WHEN temp >= 30 AND temp < 40 THEN 'Caluroso (30-40°C)'
                ELSE 'Extremo (>40°C)'
            END as rango_temperatura,
            COUNT(*) as num_ciudades,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as porcentaje
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet')
        GROUP BY rango_temperatura
        ORDER BY 
            CASE 
                WHEN rango_temperatura = 'Bajo Cero' THEN 1
                WHEN rango_temperatura = 'Frío (0-10°C)' THEN 2
                WHEN rango_temperatura = 'Templado (10-20°C)' THEN 3
                WHEN rango_temperatura = 'Cálido (20-30°C)' THEN 4
                WHEN rango_temperatura = 'Caluroso (30-40°C)' THEN 5
                ELSE 6
            END
    """
    return execute_query(query)

def ciudades_mayor_variacion_termica():
    """Ciudades con mayor diferencia entre temp_max y temp_min"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            f.temp_max,
            f.temp_min,
            ROUND(f.temp_max - f.temp_min, 2) as variacion_termica,
            f.temp as temp_actual
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        ORDER BY variacion_termica DESC
        LIMIT 10
    """
    return execute_query(query)

def comparacion_sensacion_vs_temperatura():
    """Ciudades con mayor diferencia entre sensación térmica y temperatura real"""
    query = f"""
        SELECT 
            c.Name_City,
            p.Country_Name,
            f.temp,
            f.feels_like,
            ROUND(ABS(f.feels_like - f.temp), 2) as diferencia,
            f.humidity,
            f.wind_speed
        FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year={year}/month={month}/day={day}/*.parquet') as f
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c 
            ON f.cityId = c.cityId
        INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p 
            ON c.countryId = p.countryId
        ORDER BY diferencia DESC
        LIMIT 10
    """
    return execute_query(query)