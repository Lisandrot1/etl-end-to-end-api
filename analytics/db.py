import duckdb
import os

def conn_duckdb():
    conn = duckdb.connect(':memory:')
    conn.execute("INSTALL httpfs")
    conn.execute("LOAD httpfs")
    conn.execute("SET s3_region = 'us-east-1';")
    conn.execute(f"SET s3_endpoint='{os.environ['client']}'")
    conn.execute(f"SET s3_access_key_id ='{os.environ['access_key']}'")
    conn.execute(f"SET s3_secret_access_key  ='{os.environ['secret_key']}'")
    conn.execute("SET s3_url_style='path'")
    conn.execute(f"SET s3_use_ssl = false;")
    
    return conn

