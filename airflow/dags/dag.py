import datetime 
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator, AthenaSensor

with DAG(
    'us_border_crossing_pipeline',
    description = 'An ETL pipeline for data.gov US border crossing data using Airflow, S3, and Athena',
    start_date = datetime.date(2025,3,28),
    schedule_interval = datetime.timedelta(days=1)
) as dag:
    
  start_pipeline_task = EmptyOperator(
        task_id='start_pipeline',
    )
  
  extract_data_task = BashOperator(
    task_id = 'download_data'
    bash_command = 'bash command fr fr'
  )
  
  load_to_s3_task = PythonOperator(
    task_id = 'load_to_s3',
    python_callable = 'python/load_to_s3.py'
  )

  create_table_Task = AthenaOperator(
    task_id='create_athena_table',
    database=athena_database,
    sql='sql/create_table.sql'
  )

  end_pipeline_task = EmptyOperator(
      task_id='end_pipeline',
  )