
"""
This script generates a large dataset of random user records and saves them as Parquet files.
Each record includes fields such as id, name, age, country, signup date, and active status.
"""

import random
import pandas as pd
from datetime import datetime, timedelta
import os
import awswrangler as wr
import boto3 
from dotenv import load_dotenv
from aws_session import aws_session

load_dotenv()


num_records = random.randint(500_000, 1_000_000)
print(f"Generating {num_records} records...")



def random_date(start_date, end_date):
    """
    Generate a random datetime between start_date and end_date.
    Args:
        start_date (datetime): The earliest possible date.
        end_date (datetime): The latest possible date.
    Returns:
        datetime: A random date between start_date and end_date.
    """
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def generate_random_name():
    """
    Generate a random full name by combining a random first and last name.
    Returns:
        str: A random full name.
    """
    first_names = ['Wofai', 'Titilope', 'Obinna', 'Samson', 'Victor', 'Chigozie', 'Chizoba', 'Kaycee', 'Botafli', 'Tolu']
    last_names = ['Oladipo', 'Eyong', 'Inakoju', 'Adekunle', 'Abdulkareem', 'Akinbami', 'Ade', 'Joy']
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def generate_data():
    """
    Generate a list of dictionaries, each representing a random user record.
    Args:
        num_records (int): Number of records to generate.
    Returns:
        list: List of dictionaries with user data.
    """
    countries = ['USA', 'UK', 'Canada', 'Germany', 'Australia', 'Nigeria', 'India', 'Brazil']
    # Set the date range for signup dates (last 5 years)
    start_date = datetime.now() - timedelta(days=5*365)
    end_date = datetime.now()

    data = []
    for i in range(1, num_records + 1):
        # Create a record with random values for each field
        record = {
            'id': i,
            'name': generate_random_name(),
            'age': random.randint(18, 70),
            'country': random.choice(countries),
            'signup_date': random_date(start_date, end_date).date(),
            'is_active': random.choice([True, False]),
            'is_serious': random.choice([True, False]),
            'Class': 'Elite Data Engineers'
        }
        data.append(record)

    df = pd.DataFrame(data)
    print(f"successfully generated data")
    return df



date_str = datetime.today().strftime("%Y-%m-%d")
s3_path = "s3://tolu-de-bucket/random_users/" f"{date_str}"
def upload_to_aws():
# Upload the DataFrame to S3 as Parquet using awswrangler
    print(f"Uploading data to S3...")
    wr.s3.to_parquet(
        df=generate_data(),
        path=s3_path,
        boto3_session=aws_session(),
        mode="overwrite",
        dataset=True

    )
    return


