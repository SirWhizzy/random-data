"""
Airflow DAG to generate random user data and upload to S3.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
import boto3
import awswrangler as wr
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from generate import generate_data, upload_to_aws


load_dotenv()




default_args = {
    'owner': 'airflow',
}

dag = DAG(
    dag_id='agenerate_and_upload_random_data',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily', 
    catchup=False,
)

generate_data = PythonOperator(
    task_id='generate_data',
    python_callable=generate_data,
    dag=dag,
)


upload_data = PythonOperator(
    task_id='upload_to_s3',
    python_callable=upload_to_aws,
    dag=dag,
)

date_str = datetime.today().strftime("%Y-%m-%d")
#s3_path = "/random_users/" f"{date_str}.parquet"
s3_path = "random_users/2025-08-14.parquet"
#iam_role_arn = "arn:aws:iam::700507433812:role/redshift_role"

s3_to_redshift = S3ToRedshiftOperator(
    task_id="s3_to_redshift",
    schema='public',
    table='random_data',
    s3_bucket='tolu-de-bucket',
    s3_key=s3_path,
    redshift_conn_id="aws_redshift",
    aws_conn_id="aws_credentials",
    method='REPLACE',
    copy_options=["FORMAT AS PARQUET"],
    dag=dag,
)

generate_data >> upload_data >> s3_to_redshift