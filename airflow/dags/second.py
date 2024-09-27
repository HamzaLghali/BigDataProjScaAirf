from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
#from airflow.sensors.external_task import ExternalTaskSensor

def print_second_dag():
    print("Hello, the first DAG ended successfully. Now I'm the second DAG.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag2 = DAG(
    'secondDag',
    default_args=default_args,
    schedule_interval=None,  # Will wait for the first DAG to finish
)

# wait_for_first_dag = ExternalTaskSensor(
#     task_id='wait_for_first_dag',
#     external_dag_id='firstdag',
#     external_task_id='print_first',  # Wait for this task in the first DAG
#     mode='poke',
#     timeout=600,
#     poke_interval=30,
#     dag=dag2,
# )

second_task = PythonOperator(
    task_id='print_second',
    python_callable=print_second_dag,
    dag=dag2,
)

# wait_for_first_dag >>
second_task  # Set task dependencies
