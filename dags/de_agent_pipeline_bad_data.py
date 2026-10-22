from datetime import datetime
from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator

PROJECT = "/mnt/c/Users/dedee.DED/Ded codes/AI Agent system for data engineering"
PY = "$HOME/airflow/airflow-venv/bin/python"

@dag(
    dag_id="de_agent_pipeline_bad_data",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["de-agent", "failure-demo"],
)
def de_agent_pipeline_bad_data():
    seed = BashOperator(
        task_id="seed_data",
        bash_command=f'cd "{PROJECT}" && {PY} scripts/seed_data.py',
    )
    inject = BashOperator(
        task_id="inject_bad_data",
        bash_command=f'cd "{PROJECT}" && {PY} scripts/inject_bad_data.py',
    )
    quality = BashOperator(
        task_id="run_quality_checks",
        bash_command=f'cd "{PROJECT}" && {PY} src/pipelines/data_quality_checks.py',
    )
    transform = BashOperator(
        task_id="transform_customer_summary",
        bash_command=f'cd "{PROJECT}" && {PY} src/pipelines/transform_customer_summary.py',
    )
    seed >> inject >> quality >> transform

de_agent_pipeline_bad_data()
