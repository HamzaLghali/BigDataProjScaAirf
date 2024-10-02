from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import re
import pandas as pd

# Define the input string
input_string = 'ab12("fwjjw"), sdok("3232edsa")'

# Function to parse the input string and prepare the Hive query
def parse_and_prepare_hive_query(**kwargs):
    # Regular expression to match patterns like ab12("fwjjw")
    pattern = r'(\w+)\("([^"]+)"\)'
    
    # Parse the input string into key-value pairs
    parsed_data = re.findall(pattern, input_string)
    
    # Convert the parsed data into a Pandas DataFrame
    df = pd.DataFrame(parsed_data, columns=['Key', 'Value'])
    
    # Print the DataFrame to the Airflow logs
    print("DataFrame:")
    print(df)
    
    # Generate the values for the Hive query
    values = ", ".join([f"('{row['Key']}', '{row['Value']}')" for _, row in df.iterrows()])
    
    # Hive table name
    table_name = 'parsed_data_table'
    
    # Create the Hive insert query
    insert_query = f"INSERT INTO {table_name} (key, value) VALUES {values};"
    
    # Push the query to XCom so it can be used in the BashOperator
    kwargs['ti'].xcom_push(key='hive_query', value=insert_query)

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
}

with DAG('parse_text_to_hive_dag', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    
    # PythonOperator to parse and prepare the Hive query
    task_prepare_hive_query = PythonOperator(
        task_id='prepare_hive_query',
        python_callable=parse_and_prepare_hive_query,
        provide_context=True
    )
    
    # BashOperator to execute the Hive query using the CLI
    task_execute_hive_query = BashOperator(
        task_id='execute_hive_query',
        bash_command='hive -e "{{ ti.xcom_pull(key=\'hive_query\') }}"'
    )

    # Define task dependencies
    task_prepare_hive_query >> task_execute_hive_query
