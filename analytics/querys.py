from db import conn_duckdb


def get_fact():
    conn = conn_duckdb()
    return conn.execute("""
                    SELECT
                        * 
                    FROM read_parquet('s3://etl-end-to-end/gold/fact_weather/year=2026/**/*.parquet') as f
                    """).df()


