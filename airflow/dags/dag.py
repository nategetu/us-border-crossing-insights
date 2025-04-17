import datetime 
import os 
import json
import ast 

import boto3


from botocore.exceptions import ClientError
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator

from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from common.data_ingestion import process_file, parquet_to_s3, create_redshift_table, cleanup_files

# get ENV variables
def get_secret(secret_name_txt):

    secret_name = secret_name_txt
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return ast.literal_eval(get_secret_value_response.get('SecretString'))
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

# Fetch secrets
secrets = get_secret("us-border-crossing-project")

# Use secrets in your DAG
AWS_ACCESS_KEY_ID = secrets.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = secrets.get("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = secrets.get("AWS_BUCKET_NAME")
DEV_DB_NAME = 'dev'
DATABASE_NAME = secrets.get("DATABASE_NAME")
DB_USERNAME = secrets.get("DB_USERNAME")
DB_PASSWORD = secrets.get("DB_PASSWORD")
REDSHIFT_CLUSTER_IDENTIFIER = secrets.get("REDSHIFT_CLUSTER_IDENTIFIER")

s3_hook = S3Hook()

with DAG(
    'us_border_crossing_pipeline',
    description = 'An ETL pipeline for data.gov US border crossing data using Airflow, S3, and Redshift',
    start_date=datetime.datetime(2025, 3, 28, tzinfo=datetime.timezone.utc),
    schedule_interval = "0 0 14 * *"
) as dag:
    
  start_pipeline_task = EmptyOperator(
        task_id='start_pipeline',
    )
  
  load_bridge_task = EmptyOperator(
        task_id='load_to_s3_bridge',
    )
  
  redshift_bridge_task = EmptyOperator(
        task_id='redshift_bridge',
    )
  
  # Define the arguments for each function call
  source_data_args = [
      {'task_id': 'file_1', 'args': {'url': "https://data.transportation.gov/api/views/keg4-3bc2/rows.csv?accessType=DOWNLOAD", 'file_name': 'border_crossings'}},
      {'task_id': 'file_2', 'args': {'url': "https://hub.arcgis.com/api/v3/datasets/e3b6065cce144be8a13a59e03c4195fe_0/downloads/data?format=csv&spatialRefId=3857&where=1%3D1", 'file_name': 'principal_ports'}},
      {'task_id': 'file_3', 'args': {'url': "https://hub.arcgis.com/api/v3/datasets/6755534edf0f441894e021912486db31_0/downloads/data?format=csv&spatialRefId=4269&where=1%3D1", 'file_name': 'port_statistical_areas'}}
  ]
  
  local_load_tasks = []
  for arg_iter in source_data_args:
      task = PythonOperator(
          task_id=f"local_load_task_{arg_iter['task_id']}",
          python_callable=process_file,
          op_kwargs=arg_iter['args'],
          dag=dag
      )
      local_load_tasks.append(task)

  load_to_s3_tasks = []
  for arg_iter in source_data_args:
      task = PythonOperator(
          task_id=f"load_to_s3_task_{arg_iter['task_id']}",
          python_callable=parquet_to_s3,
          op_kwargs={'file_name': arg_iter['args'].get('file_name'), 'bucket': AWS_BUCKET_NAME , 'hook': s3_hook},  
          dag=dag
      )
      load_to_s3_tasks.append(task)

  create_redshift_table_tasks = []
  for arg_iter in source_data_args:
    file_name = arg_iter['args'].get('file_name')
    sql_ddl = create_redshift_table(file_name=file_name)

    create_table_task = RedshiftDataOperator(
        task_id=f'create_redshift_table_{file_name}',
        database=DATABASE_NAME,
        cluster_identifier=REDSHIFT_CLUSTER_IDENTIFIER,
        db_user=DB_USERNAME,
        sql=sql_ddl,
        aws_conn_id='aws_default',
        task_concurrency=1,
        wait_for_completion=True
    )
    create_redshift_table_tasks.append(create_table_task)

  cleanup_tasks = []
  for arg_iter in source_data_args:
    file_name = arg_iter['args'].get('file_name')
    sql_ddl = create_redshift_table(file_name=file_name)

    cleanup_task = PythonOperator(
        task_id=f'cleanup_{file_name}',
          python_callable=cleanup_task,
          op_kwargs={'file_name': arg_iter['args'].get('file_name')},  
          dag=dag
      )
    cleanup_tasks.append(cleanup_task)   

  s3_file_paths = [f for f in s3_hook.list_keys(bucket_name=AWS_BUCKET_NAME) if f.endswith('.parquet')]

  transfer_s3_to_redshift_tasks = []
  for s3_file in s3_file_paths:
    transfer_s3_to_redshift = S3ToRedshiftOperator(
        task_id=f"transfer_{s3_file}_to_redshift",
        redshift_data_api_kwargs={
            "database": DATABASE_NAME,
            "cluster_identifier": REDSHIFT_CLUSTER_IDENTIFIER,
            "db_user": DB_USERNAME,
            "wait_for_completion": True,
        },
        s3_bucket=AWS_BUCKET_NAME,
        s3_key=s3_file,
        schema="PUBLIC",
        table=s3_file.split('.')[0],
        copy_options=["parquet"],
    )
    transfer_s3_to_redshift_tasks.append(transfer_s3_to_redshift)

  transform_table_task = RedshiftDataOperator(
    task_id='transform_redshift_table',
    database=DATABASE_NAME,
    cluster_identifier=REDSHIFT_CLUSTER_IDENTIFIER,
    db_user=DB_USERNAME,
    sql='sql/transform_tables.sql',
    aws_conn_id='aws_default',
    task_concurrency=1,
    wait_for_completion=True
  )

  end_pipeline_task = EmptyOperator(
      task_id='end_pipeline',
  )

  for local_task in local_load_tasks:
      start_pipeline_task >> local_task

  for local_task, s3_task, redshift_tbl_ddl_task, cleanup_task, transfer_s3_to_redshift_task in zip(local_load_tasks, load_to_s3_tasks, create_redshift_table_tasks, cleanup_tasks, transfer_s3_to_redshift_tasks):
      local_task >> load_bridge_task >> s3_task >> redshift_tbl_ddl_task >> cleanup_task >> transfer_s3_to_redshift_task

  redshift_bridge_task >> transform_table_task >> end_pipeline_task