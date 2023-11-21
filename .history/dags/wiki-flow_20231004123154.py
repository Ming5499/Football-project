from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from dags.test.py import *
    
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 9),
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


extract_data_from_wikipedia = PythonOperator(
    task_id = 'extract_data_from_wikipedia',
    python_callable=get_wikipedia_page(),
    provide_context = True,
    op_kwargs={"url":"https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"},
    dag=dag
)