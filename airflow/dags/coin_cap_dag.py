# airflow/dags/coin_cap_dag.py
from airflow import DAG
from datetime import timedelta
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

from src.extract.extract_coin_cap import fetch_coins
from src.transform.transform_coin_cap import transform_coins
from src.load.load_coin_cap import insert_coins

# Define tasks
def extract_task():
    """Extract data from CoinCap API"""
    limit = Variable.get("coin_cap_limit", default_var=10)
    coins = fetch_coins(limit=int(limit))
    return coins


def transform_task(coins):
    """Transform raw data"""
    return transform_coins(coins)


def load_task(coins):
    """Load data into database"""
    insert_coins(coins)

# Default args
default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=10),
}

# Define Dag for CoinCap ETL Pipeline
with DAG(
    dag_id="coin_cap_etl_pipeline",
    default_args=default_args,
    description="CoinCap ETL Pipeline",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["etl", "coin_cap"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_task,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_task,
        provide_context=True,
        op_args=["{{ ti.xcom_pull(task_ids='extract') }}"],
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_task,
        provide_context=True,
        op_args=["{{ ti.xcom_pull(task_ids='transform') }}"],
    )

    extract >> transform >> load