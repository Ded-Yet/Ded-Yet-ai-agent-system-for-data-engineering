from datetime import datetime
from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator

PROJECT = "/mnt/c/Users/dedee.DED/Ded codes/AI Agent system for data engineering"
PY = "$HOME/airflow/airflow-venv/bin/python"

@dag(
    dag_id="de_agent_pipeline",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["de-agent"],
)
def de_agent_pipeline():
    seed = BashOperator(
        task_id="seed_data",
        bash_command=f'cd "{PROJECT}" && {PY} scripts/seed_data.py',
    )
    quality = BashOperator(
        task_id="run_quality_checks",
        bash_command=f'cd "{PROJECT}" && {PY} src/pipelines/data_quality_checks.py',
    )
    transform = BashOperator(
        task_id="transform_customer_summary",
        bash_command=f'cd "{PROJECT}" && {PY} src/pipelines/transform_customer_summary.py',
    )
    evaluate = BashOperator(
        task_id="run_sql_eval",
        bash_command=f'cd "{PROJECT}" && {PY} scripts/run_eval.py',
    )
    seed >> quality >> transform >> evaluate

de_agent_pipeline()
