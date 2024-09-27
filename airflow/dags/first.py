from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def print_first_dag():
    print("Hello, I'm the first DAG")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag1 = DAG(
    'firstdag',
    default_args=default_args,
    schedule_interval='@daily',
)

first_task = PythonOperator(
    task_id='print_first',
    python_callable=print_first_dag,
    dag=dag1,
)
