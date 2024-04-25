from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Define the DAG's properties and configurations
automation_name = 'open_ai_call'
script_directory = f'/opt/airflow/src/{automation_name}'  # Define the stable directory for scripts

with DAG(
    dag_id=automation_name,
    default_args={
        "depends_on_past": False,
        "retries": 0,
        "retry_delay": timedelta(minutes=2),
    },
    schedule_interval="*/5 2-20 * * *",  # Runs every 5 minutes between 2am and 8pm
    start_date=datetime(2023, 5, 18, 6, 0, 0),
    catchup=False,
    max_active_runs=1,
) as dag:

    # Task to create a stable working directory (if not already existing)
    create_dir_task = BashOperator(
        task_id='create_working_directory',
        bash_command=f'mkdir -p {script_directory}'
    )

    # Task to debug and print the current working directory and environment variables
    debug_info = BashOperator(
        task_id='debug_info',
        bash_command='echo "Current directory: $(pwd)" && echo "Environment variables:" && printenv'
    )

    # Main script execution task
    main_task = BashOperator(
        task_id=automation_name,
        bash_command=f'python "{script_directory}/{automation_name}.py" >> "{script_directory}/{automation_name}.log" 2>&1'
    )

    # Set task dependencies
    create_dir_task >> debug_info >> main_task

