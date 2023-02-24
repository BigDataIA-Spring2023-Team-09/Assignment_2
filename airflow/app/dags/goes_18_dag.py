import boto3
import sqlite3
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from dotenv import load_dotenv
import os
from airflow.models import Variable
import csv
import io

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
USER_BUCKET_NAME = Variable.get('USER_BUCKET_NAME')


s3client = boto3.client(
    's3',
    aws_access_key_id=Variable.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=Variable.get('AWS_SECRET_ACCESS_KEY')

)



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 22),
    'retries': 0
}

dag = DAG('goes18_etl',
          default_args=default_args,
          schedule_interval='0 4 * * *',
          catchup=False
          )

def extract_transform_load():
    """Gathers data from the GOES18 S3 bucket and creates metadata containing file paths for every files present 
    in that bucket in the form of a database"""
    # logging.debug("fetching objects in NOAA s3 bucket")
    paginator = s3client.get_paginator('list_objects_v2')
    noaa_bucket = paginator.paginate(Bucket='noaa-goes18', Prefix="ABI-L1b-RadC")
    
    # Connect to the database
    conn = sqlite3.connect("filenames_goes.db")
    c = conn.cursor()

    # Create a table if it does not exist
    c.execute("""CREATE TABLE IF NOT EXISTS filenames_goes (Product text, Year text, Day text, Hour text, PKey text primary key)""")

    # Truncates the table before filling metadata
    # c.execute("""DELETE FROM filenames_goes""")
    # logging.info("Printing Files in NOAA bucket")

    # Fills the data in the database
    for count, page in enumerate (noaa_bucket):
        files = page.get("Contents")
        if (count%5 == 0):
            conn.commit()
        for file in files:
            # print('\t' * 4 + file['Key'])
            filename = file['Key'].split('/')
            # print(filename)
            pkey = "" + filename[0] + filename[1] + filename[2] + filename[3] 
            c.execute("INSERT OR IGNORE INTO filenames_goes (Product , Year , Day , Hour, PKey) VALUES ('{}', '{}', '{}', '{}', '{}')"
                      .format(filename[0], filename[1], filename[2], filename[3], pkey))
    
    conn.commit()

    # Retrieve data from SQLite database
    c.execute('SELECT * FROM filenames_goes')
    data = c.fetchall()

    # Save data as CSV file in memory
    csv_file = io.StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(['Product', 'Year', 'Day', 'Hour', 'Pkey'])
    writer.writerows(data)



    # Upload CSV file and db file to S3 bucket
    s3client.put_object(Body=csv_file.getvalue().encode('utf-8'), Bucket=USER_BUCKET_NAME, Key='goes18_data.csv')
    s3client.upload_file('filenames_goes.db', USER_BUCKET_NAME, 'filenames_goes.db')


    conn.close()



run_etl = PythonOperator(
    task_id='run_etl',
    python_callable=extract_transform_load,
    dag=dag
)
