# dags/pyspark_notebook_dag.py

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
}

with DAG('pyspark_notebook_dag', default_args=default_args, schedule_interval='@daily') as dag:

    run_notebook = BashOperator(
        task_id='run_notebook',
        bash_command='spark-submit /opt/airflow/notebooks/notebook1.py',
    )

    run_notebook
