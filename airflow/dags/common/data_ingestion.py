import os
import urllib.request

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine



def process_file(url, file_name):
    with urllib.request.urlopen(url) as data:
        pd_data = pd.read_csv(data)
        if file_name == 'border_crossings':
            pd_data = pd_data.drop(columns=['Point'])
        elif file_name == 'principal_ports':
            pd_data = pd_data.drop(columns = ['X', 'Y'])
        elif file_name == 'port_statistical_areas':
            pd_data = pd_data[['PORTIDPK', 'FEATUREDESCRIPTION']]
        pa_table = pa.Table.from_pandas(pd_data)
        pq.write_table(pa_table, f'{file_name}.parquet')

def parquet_to_s3(file_name, bucket, hook):
    response = hook.load_file(filename=f'{file_name}.parquet', key=f'{file_name}.parquet', bucket_name=bucket, replace=True)


def create_redshift_table(filename):
    try:
        file_name = filename
        engine = create_engine(f'postgresql+psycopg2://airflow:airflow@postgres/airflow')
        engine.connect()
        pd_table = pq.read_table(f'{file_name}.parquet').to_pandas()
        pd_table.columns = [col.replace(" ", "_") for col in pd_table.columns]
        drop_table_query = f"DROP TABLE IF EXISTS {file_name};"
        schema = pd.io.sql.get_schema(pd_table, name=file_name, con=engine)
        schema = schema.replace(" TEXT", " VARCHAR(4096)")
        return drop_table_query+schema
    except FileNotFoundError as e:
        print(f"Error: {e}. {file_name}.parquet not found.")

def cleanup_files(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
