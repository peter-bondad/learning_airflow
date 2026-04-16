from airflow import DAG
from airflow.decorators import task
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.models import Variable

from src.extract.extract_coin_cap import fetch_coins
from src.transform.transform_coin_cap import transform_coins
from src.load.load_coin_cap import insert_coins


default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=10),
}


with DAG(
    dag_id="coin_cap_etl_pipeline",
    default_args=default_args,
    description="CoinCap ETL Pipeline",
    schedule="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["etl", "coin_cap"],
) as dag:

    @task
    def extract():
        limit = Variable.get("coin_cap_limit", default_var=10)
        return fetch_coins(limit=int(limit))

    @task
    def transform(coins):
        return transform_coins(coins)

    @task
    def load(coins):
        insert_coins(coins)

    # Dependency graph (clean + type-safe)
    load(transform(extract()))