import os
import sqlite3
from fastapi import FastAPI, Response
from dotenv import load_dotenv
import boto3
import base_model
import basic_func
import pandas as pd
import streamlit as st
from passlib.context import CryptContext

app =FastAPI()


load_dotenv()


s3client = boto3.client('s3', 
                        region_name = 'us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )


goes18_bucket = 'noaa-goes18'
user_bucket_name = os.environ.get('USER_BUCKET_NAME')
nexrad_bucket = 'noaa-nexrad-level2'


@app.get("/say-hello")
async def say_hello() -> dict:
    return {"message":"Hello World"}

@app.post("/landing_page")
async def landing_page(data: dict):
    menu = ["Home", "Login"]
    choice = data["choice"]
    result = {}
    
    if choice == "Home":
        result["subheader"] = "Home"
        result["message"] = "Welcome to NOAA dashboard!"
        
    elif choice == "Login":
        result["subheader"] = "Login"
        email = data["email"]
        password = data["password"]

        fixed_salt = "MyFixedSaltererererere"
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hash_pass=pwd_context.hash(password, salt=str(fixed_salt))
        db = sqlite3.connect('users.db')
        df = pd.read_sql_query('''SELECT email, hashed_password FROM users''', db)
        count=0
        ind=0
        for i, em in enumerate(df['email']):
            if em==email:
                count+=1
                ind=i
        if count==0:
            result["warning"] = "Incorrect email"
        else:
            if df['hashed_password'][ind]==hash_pass:
                result["success"] = "Logged in as {}".format(email)
            else:
                result["warning"] = "Incorrect password"
    return result

@app.post("/fetch_url")
async def fetch_url(userinput: base_model.UserInput) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date
    aws_nexrad_url = f"https://noaa-nexrad-level2.s3.amazonaws.com/index.html#{userinput.year:04}/{userinput.month:02}/{userinput.date:02}/{userinput.station}"
    return {'url': aws_nexrad_url }


@app.get("/list-years-nexrad", tags=["Nexrad filters"])
async def list_years_nexrad() -> dict:

    # Establishes a connection to the nexrad database
    c = basic_func.conn_filenames_nexrad()

    # Lists the years present in nexrad database
    year_list = basic_func.list_years_nexrad(c)

    # Clean up
    basic_func.conn_close(c)

    return {"year_list":year_list}


@app.post("/list-months-nexrad", tags=["Nexrad filters"])
async def list_months_nexrad(year: str) -> dict:

    # Establishes a connection to the nexrad database
    c = basic_func.conn_filenames_nexrad()

    # Lists the months for the selected year from nexrad database
    month_list = basic_func.list_months_nexrad(c, year)

    # Clean up
    basic_func.conn_close(c)

    return {"month_list":month_list}


@app.post("/list-days-nexrad", tags=["Nexrad filters"])
async def list_days_nexrad(year: str, month: str) -> dict:

    # Establishes a connection to the nexrad database
    c = basic_func.conn_filenames_nexrad()

    # Lists the days for the selected year and month from nexrad database
    days_list = basic_func.list_days_nexrad(c, year, month)

    # Clean up
    basic_func.conn_close(c)

    return {"days_list":days_list}


@app.post("/list-stations-nexrad", tags=["Nexrad filters"])
async def list_stations_nexrad(year: str, month: str, day:str) -> dict:

    # Establishes a connection to the nexrad database
    c = basic_func.conn_filenames_nexrad()

    # Lists the stations for the selected year, month and day from nexrad database
    stations_list = basic_func.list_stations_nexrad(c, year, month, day)

    # Clean up
    basic_func.conn_close(c)

    return {"stations_list":stations_list}


@app.post("/list-files-nexrad", tags=["Nexrad filters"])
async def list_files_nexrad(year: str, month: str, day:str, station:str) -> dict:

    # Lists the files present in the nexrad bucket for the selected year, month, day and station
    file_list = basic_func.list_filenames_nexrad(year, month, day, station)

    return {"file_list":file_list}


@app.post("/fetch-url-nexrad", tags=["Nexrad filters"])
async def fetch_url_nexrad(name:str) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date

    # Generates file path in nexrad bucket from file name
    file_path = basic_func.path_from_filename_nexrad(name)

    # Define path where the file has to be written
    user_object_key = f'logs/nexrad/{name}'

    # Copies the specified file from source bucket to destination bucket 
    basic_func.copy_to_public_bucket(nexrad_bucket, file_path, user_bucket_name, user_object_key)

    # Generates the download URL of the specified file present in the given bucket and write logs in S3
    aws_url = basic_func.generate_download_link_nexrad(user_bucket_name, user_object_key) 

    return {'url': aws_url.split("?")[0] }


@app.post("/validate-url-nexrad", tags=["Nexrad filters"])
async def validate_url_nexrad(name:str) -> dict:

    # Generates file path in goes18 bucket from file name
    file_path = basic_func.path_from_filename_nexrad(name)

    # Generates the download URL of the specified file present in the given bucket
    aws_url = basic_func.generate_download_link_nexrad(nexrad_bucket, file_path) 

    return {'url': aws_url.split("?")[0] }


@app.get("/list-years-goes", tags=["GOES18 filters"])
async def list_years_goes() -> dict:

    # Establishes a connection to the goes database
    c = basic_func.conn_filenames_goes()

    # Lists the years present in goes database
    year_list = basic_func.list_years_goes(c)

    # Clean up
    basic_func.conn_close(c)

    return {"year_list":year_list}


@app.post("/list-days-goes", tags=["GOES18 filters"])
async def list_days_goes(year:str) -> dict:

    # Establishes a connection to the goes database
    c = basic_func.conn_filenames_goes()

    # Lists the days for the selected year from goes database
    days_list = basic_func.list_days_goes(c, year)

    # Clean up
    basic_func.conn_close(c)

    return {"days_list":days_list}


@app.post("/list-hours-goes", tags=["GOES18 filters"])
async def list_hours_goes(year:str, day:str) -> dict:

    # Establishes a connection to the goes database
    c = basic_func.conn_filenames_goes()

    # Lists the hours for the selected year and day goes database
    hours_list = basic_func.list_hours_goes(c, year, day)

    # Clean up
    basic_func.conn_close(c)

    return {"hours_list":hours_list}


@app.post("/list-files-goes", tags=["GOES18 filters"])
async def fetch_url_goes(year:str, day:str, hour:str) -> dict:

    # Lists the files present in the goes18 bucket for the selected year, day and hour
    file_list = basic_func.list_filenames_goes(year, day, hour)

    return {"file_list":file_list}


@app.post("/fetch-url-goes", tags=["GOES18 filters"])
async def fetch_url_goes(name:str) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date

    # Generates file path in goes18 bucket from file name
    file_path = basic_func.path_from_filename_goes(name)

    # Define path where the file has to be written
    user_object_key = f'logs/goes18/{name}'

    # Copies the specified file from source bucket to destination bucket 
    basic_func.copy_to_public_bucket(goes18_bucket, file_path, user_bucket_name, user_object_key)

    # Generates the download URL of the specified file present in the given bucket and write logs in S3
    aws_url = basic_func.generate_download_link_goes(user_bucket_name, user_object_key) 

    return {'url': aws_url.split("?")[0] }


@app.post("/validate-url-goes", tags=["GOES18 filters"])
async def validate_url_goes(name:str) -> dict:

    # Generates file path in goes18 bucket from file name
    file_path = basic_func.path_from_filename_goes(name)

    # Generates the download URL of the specified file present in the given bucket
    aws_url = basic_func.generate_download_link_goes(goes18_bucket, file_path) 

    return {'url': aws_url.split("?")[0] }


# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request: Request, exc: ValidationError):
#     return JSONResponse(
#         status_code=400,
#         content={"detail": exc.errors()}
#     )


@app.post("/fetch-url-goes-from-name", tags=["GOES18 name"])
async def fetch_url_goes_from_name(name:str) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date

    # Generate file path from filename
    src_object_key = basic_func.path_from_filename_goes(name)

    # Checks if the provided file exists in goes bucket
    if basic_func.check_if_file_exists_in_s3_bucket(goes18_bucket, src_object_key):

        # Define path where the file has to be written
        user_object_key = f'logs/goes18/{name}'

        # Copy file from GOES18 bucket to user bucket
        basic_func.copy_to_public_bucket(goes18_bucket, src_object_key, user_bucket_name, user_object_key)

        # Generate link from user bucket
        aws_url = basic_func.generate_download_link_goes(user_bucket_name, user_object_key)

        # Returns the generated URL
        return {'url': aws_url.split("?")[0] }
    
    else:
        # Returns a message saying file does not exist in the bucket
        return {"message":"404: File not found"}


@app.post("/fetch-url-nexrad-from-name", tags=["Nexrad name"])
async def fetch_url_nexrad_from_name(name:str) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date

    # Generate file path from filename
    src_object_key = basic_func.path_from_filename_nexrad(name)

    # Checks if the provided file exists in nexrad bucket
    if basic_func.check_if_file_exists_in_s3_bucket(nexrad_bucket, src_object_key):

        # Define path where the file has to be written
        user_object_key = f'logs/nexrad/{name}'

        # Copy file from nexrad bucket to user bucket
        basic_func.copy_to_public_bucket(nexrad_bucket, src_object_key, user_bucket_name, user_object_key)

        # Generate link from user bucket
        aws_url = basic_func.generate_download_link_nexrad(user_bucket_name, user_object_key)

        # Returns the generated URL
        return {'url': aws_url.split("?")[0] }
    
    else:
        # Returns a message saying file does not exist in the bucket
        return {"message":"404: File not found"}


@app.get("/mapping-stations", tags=["Mapping"], response_class=Response)
async def mapping_stations(response: Response) -> str:
    # Retrieve data from database
    db = sqlite3.connect('location.db')
    cursor = db.cursor()
    cursor.execute('''SELECT lat, long, City FROM loaction_radar''')
    data = cursor.fetchall()
    
    # Create DataFrame and convert to CSV string
    df = pd.DataFrame(data, columns=["column1", "column2", "column3"])
    csv_string = df.to_csv(index=False)

    # # Set response headers and return CSV string
    response.headers["Content-Disposition"] = "attachment; filename=my_data.csv"
    response.headers["Content-Type"] = "text/csv"
    return csv_string

