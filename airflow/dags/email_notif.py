from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator  # Import EmailOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'email': "lghali.hamza.ma@gmail.com",  # Your email for failure notification
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'email_notification_dag',
    default_args=default_args,
    description='DAG with email notifications',
    schedule_interval=timedelta(days=1),  # Runs daily
    start_date=datetime(2024, 9, 30),
    catchup=False,
) as dag:

    # Task 1: Bash command execution
    task1 = BashOperator(
        task_id="emailing",
        bash_command='echo "This is a valid command"'
    )

    # Task 2: Send email notification
    send_email = EmailOperator(
        task_id='send_email',
        to='vanhamzalghali@gmail.com',  # Your email address
        subject='Airflow Task Success',
        html_content='<p>The Bash task completed successfully.</p>',
    )

    # Set task dependencies
    task1 >> send_email  # Email will be sent after task1 succeeds
