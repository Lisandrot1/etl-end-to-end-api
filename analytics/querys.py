from db import conn_duckdb


def get_temp_actual():
    conn = conn_duckdb()
    return conn.execute("""
                    SELECT
                        ROUND(AVG(f.temp), 2) as avg_temperatura
                    FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year=2026/**/*.parquet') as f
                    """).df()


def get_count_cities():
    conn = conn_duckdb()
    return conn.execute("""
                    SELECT
                        COUNT(*) AS  Cant_ciudades
                    FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year=2026/**/*.parquet') as f
                    """).df()
# TOP 5 PAISES MAS CALIENTES    
def get_top5_countrys_calientes():
    conn = conn_duckdb()
    return conn.execute("""
                    SELECT
                        p.Country_Name,
                        ROUND(AVG(f.temp), 2) AS temp_promedio
                    FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year=2026/**/*.parquet') as f
                    INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c ON f.cityId = c.cityId
                    INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_country/dim_country.parquet') as p ON c.countryId = p.countryId
                    GROUP BY p.Country_Name
                    ORDER BY temp_promedio DESC
                    LIMIT 5
                    """).df()
#CIUDAD MAS FRIA DEL DIA
def get_city_mas_frio():
    conn = conn_duckdb()
    return conn.execute("""
                    SELECT
                        C.Name_City,
                        f.temp_min
                    FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year=2026/**/*.parquet') as f
                    INNER JOIN read_parquet('s3://etl-end-to-end/gold/dim_citie/dim_citie.parquet') as c ON f.cityId = c.cityId
                    ORDER BY f.temp_min ASC
                    LIMIT 1
                    """).df()