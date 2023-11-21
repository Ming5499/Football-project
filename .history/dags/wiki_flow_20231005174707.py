from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from datetime import timedelta
import os
import sys 
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.wiki_etl import *
    
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 10),
    'email': ['npam5499@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    dag_id='wiki_flow',
    default_args=default_args,
    schedule_interval = None,
    catchup=False    
)


extract_data_from_wikipedia_task = PythonOperator(
    task_id = 'extract_data_from_wikipedia_task',
    python_callable=get_wikipedia_page,
    provide_context = True,
    op_kwargs={"url":"https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"},
    dag=dag
)

tranform_wikipedia_data_task = PythonOperator(
    task_id = 'tranform_wikipedia_data_task',
    python_callable=transform_wikipedia_data,
    provide_context = True,
    dag= dag
)

load_wikipedia_data_task = PythonOperator(
    task_id = 'load_wikipedia_data_task',
    python_callable=load_wikipedia_data_to_csv,
    provide_context = True,
    dag = dag
)

extract_data_from_wikipedia_task >> tranform_wikipedia_data_task >> load_wikipedia_data_task