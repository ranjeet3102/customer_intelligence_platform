from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


default_args = {
    "owner": "cip",
    "retries": 1,
}


with DAG(
    dag_id="customer_intelligence_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="59 23 * * *",  # Runs daily at 11:59 PM
    catchup=False,
    default_args=default_args,
    description="CIP Full Daily Pipeline",
) as dag:

    ingestion = BashOperator(
        task_id="feature_pipeline",
        bash_command="""
        cd /opt/airflow/cip_project/backend &&
        export PYTHONPATH=/opt/airflow/cip_project/backend &&
        python -m scripts.run_feature_pipeline
        """,
    )

    inference = BashOperator(
        task_id="batch_inference",
        bash_command="""
        cd /opt/airflow/cip_project/backend &&
        export PYTHONPATH=/opt/airflow/cip_project/backend &&
        python -m src.inference.batch.batch_runner
        """,
    )

    clv = BashOperator(
        task_id="clv",
        bash_command="""
        cd /opt/airflow/cip_project/backend &&
        export PYTHONPATH=/opt/airflow/cip_project/backend &&
        python -m src.clv.clv_runner
        """,
    )

    segmentation = BashOperator(
        task_id="segmentation",
        bash_command="""
        cd /opt/airflow/cip_project/backend &&
        export PYTHONPATH=/opt/airflow/cip_project/backend &&
        python -m src.segmentation.runner
        """,
    )

    decisioning = BashOperator(
        task_id="decisioning",
        bash_command="""
        cd /opt/airflow/cip_project/backend &&
        export PYTHONPATH=/opt/airflow/cip_project/backend &&
        python -m src.decisioning.runner
        """,
    )

    ingestion >> inference >> clv >> segmentation >> decisioning