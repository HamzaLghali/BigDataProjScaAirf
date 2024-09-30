from datetime import datetime
from airflow import DAG
from airflow.operators.email import EmailOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 30),
    'retries': 1,
}

with DAG(
    dag_id='mailhogtesting',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    

    send_email = EmailOperator(
        task_id='send_email',
        to='recipient@example.com',
        subject='Sample Email from Airflow',
        html_content='<h3>This is a test email sent from Airflow using MailHog!</h3>',
    )

    
    send_email
