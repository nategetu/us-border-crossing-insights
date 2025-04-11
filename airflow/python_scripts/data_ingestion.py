import os
import urllib.request

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

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
        pq.write_table(pa_table, f'{file_name}_s3.parquet')

def parquet_to_s3(file_name, bucket, hook):
    response = hook.upload_file(file_name, bucket, file_name)
    if response is None and os.path.exists(file_name):
        os.remove(file_name)
