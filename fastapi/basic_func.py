import sqlite3
from dotenv import load_dotenv
import boto3
import os
import botocore
import time

s3client = boto3.client('s3', 
                        region_name = 'us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )

#Establish connection to logs
clientlogs = boto3.client('logs', 
                        region_name = 'us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )

def say_hello():
    return "Hello World"


def fetch_url(
    year=int,
    month=int,
    date=int,
    station=str
):
    aws_nexrad_url = f"https://noaa-nexrad-level2.s3.amazonaws.com/index.html#{year:04}/{month:02}/{date:02}/{station:02}"
    return aws_nexrad_url
    

print(say_hello())
func_op = fetch_url(2022, 6, 21, 'KAMX')
print(func_op)


# Generates file path in goes18 bucket from file name
def path_from_filename_goes(filename):

    ind = filename.index('s')
    file_path = f"ABI-L1b-RadC/{filename[ind+1: ind+5]}/{filename[ind+5: ind+8]}/{filename[ind+8: ind+10]}/{filename}"
    return file_path


# Generates file path in nexrad bucket from file name
def path_from_filename_nexrad(filename):
   
    details_list =[]
    details_list.append(filename[:4])
    details_list.append(filename[4:8])
    details_list.append(filename[8:10])
    details_list.append(filename[10:12])
    details_list.append(filename)
    file_path = f"{details_list[1]}/{details_list[2]}/{details_list[3]}/{details_list[0]}/{details_list[4]}"
    return file_path


# Checks if the passed file exists in the specified bucket
def check_if_file_exists_in_s3_bucket(bucket_name, file_name):
    try:
        s3client.head_object(Bucket=bucket_name, Key=file_name)
        return True

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise


# Generates the download URL of the specified file present in the given bucket and write logs in S3
def generate_download_link_goes(bucket_name, object_key, expiration=3600):
    response = s3client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_key
        },
        ExpiresIn=expiration
    )
    write_logs_goes(f"{[object_key.rsplit('/', 1)[-1],response]}")
    return response


# Generates the download URL of the specified file present in the given bucket and write logs in S3
def generate_download_link_nexrad(bucket_name, object_key, expiration=3600):
    response = s3client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_key
        },
        ExpiresIn=expiration
    )
    write_logs_nexrad(f"{[object_key.rsplit('/', 1)[-1],response]}")
    return response


#Generating logs with given message in cloudwatch
def write_logs_goes(message : str):
    clientlogs.put_log_events(
    logGroupName = "assignment2-logs",
    logStreamName = "goes-logs",
    logEvents = [
        {
            'timestamp' : int(time.time() * 1e3),
            'message' : message
        }
    ]                            
    )


#Generating logs with given message in cloudwatch
def write_logs_nexrad(message : str):
    clientlogs.put_log_events(
    logGroupName = "assignment2-logs",
    logStreamName = "nexrad-logs",
    logEvents = [
        {
            'timestamp' : int(time.time() * 1e3),
            'message' : message
        }
    ]                            
    )


# Copies the specified file from source bucket to destination bucket 
def copy_to_public_bucket(src_bucket_name, src_object_key, dest_bucket_name, dest_object_key):
    copy_source = {
        'Bucket': src_bucket_name,
        'Key': src_object_key
    }
    s3client.copy_object(Bucket=dest_bucket_name, CopySource=copy_source, Key=dest_object_key)


# Establishes a connection to the goes database
def conn_filenames_goes():
    conn = sqlite3.connect("filenames_goes.db")
    c = conn.cursor()
    return c


# Lists the years present in goes database
def list_years_goes(c):
    query = c.execute("SELECT DISTINCT Year FROM filenames_goes")
    year_list = [row[0] for row in query]
    return year_list


# Lists the days for the selected year from goes database
def list_days_goes(c, year):
    query = "SELECT DISTINCT Day FROM filenames_goes where Year = ?"
    result = c.execute(query, (year,))
    day_list = [row[0] for row in result]
    return day_list


# Lists the hours for the selected year and day goes database
def list_hours_goes(c, year, day):
    query = "SELECT DISTINCT Hour FROM filenames_goes where Year=? and Day=?"
    result = c.execute(query, (year, day,))
    hour_list = [row[0] for row in result]
    return hour_list


# Lists the files present in the goes18 bucket for the selected year, day and hour
def list_filenames_goes(c, year, day, hour):
    result = s3client.list_objects(Bucket='noaa-goes18', Prefix=f"ABI-L1b-RadC/{year}/{day}/{hour}/")
    file_list = []
    files = result.get("Contents", [])
    for file in files:
        file_list.append(file["Key"].split('/')[-1])
    return file_list


# Establishes a connection to the nexrad database
def conn_filenames_nexrad():
    conn = sqlite3.connect("filenames_nexrad.db")
    c = conn.cursor()
    return c


# Lists the years present in nexrad database
def list_years_nexrad(c):
    query = c.execute("SELECT DISTINCT Year FROM filenames_nexrad")
    year_list = [row[0] for row in query]
    return year_list


# Lists the months for the selected year from nexrad database
def list_months_nexrad(c, year):
    query = "SELECT DISTINCT Month FROM filenames_nexrad where Year = ?"
    result = c.execute(query, (year,))
    month_list = [row[0] for row in result]
    return month_list


# Lists the days for the selected year and month from nexrad database
def list_days_nexrad(c, year, month):
    query = "SELECT DISTINCT Day FROM filenames_nexrad where Year = ? and Month = ?"
    result = c.execute(query, (year, month))
    day_list = [row[0] for row in result]
    return day_list


# Lists the stations for the selected year, month and day from nexrad database
def list_stations_nexrad(c, year, month, day):
    query = "SELECT DISTINCT Station FROM filenames_nexrad where Year = ? and Month = ? and Day = ?"
    result = c.execute(query, (year, month, day))
    station_list = [row[0] for row in result] 
    return station_list   


# Lists the files present in the nexrad bucket for the selected year, month, day and station
def list_filenames_nexrad(c, year, month, day, station):
    result = s3client.list_objects(Bucket='noaa-nexrad-level2', Prefix=f"{year}/{month}/{day}/{station}/")
    file_list = []
    files = result.get("Contents", [])
    for file in files:
        file_list.append(file["Key"].split('/')[-1])
    return file_list