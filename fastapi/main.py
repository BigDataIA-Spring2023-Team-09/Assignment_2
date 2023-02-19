import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import boto3
import base_model
import streamlit as st
from starlette.responses import HTMLResponse
import Assignment_2.fastapi.basic_func as basic_func


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


@app.get("/streamlit")
def streamlit_endpoint():
    return st.embed_iframe("https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/main/app.py")


@app.post("/fetch-url-nexrad")
async def fetch_url_nexrad(userinput: base_model.UserInputNexrad) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date
    aws_url = f"https://noaa-nexrad-level2.s3.amazonaws.com/index.html#{userinput.year:04}/{userinput.month:02}/{userinput.date:02}/{userinput.station}"   
    return {'url': aws_url }


@app.post("/fetch-url-goes")
async def fetch_url_goes(userinput: base_model.UserInputGOES) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date
    aws_url = f"https://noaa-goes18.s3.amazonaws.com/index.html#{userinput.year:04}/{userinput.day:02}/{userinput.hour:02}"
    return {'url': aws_url }


@app.post("/fetch-url-goes-from-name")
async def fetch_url_goes_from_name(userinput: base_model.UserInputName) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date

    # Checks if the provided file exists in goes bucket
    if basic_func.check_if_file_exists_in_s3_bucket(goes18_bucket, userinput.name):

        # Generate file path from filename
        src_object_key = basic_func.path_from_filename_goes(userinput.name)

        # Define path where the file has to be written
        user_object_key = f'logs/goes18/{userinput.name}'

        # Copy file from GOES18 bucket to user bucket
        basic_func.copy_to_public_bucket(goes18_bucket, src_object_key, user_bucket_name, user_object_key)

        # Generate link from user bucket
        aws_url = basic_func.generate_download_link_goes(user_bucket_name, user_object_key)

        # Returns the generated URL
        return {'url': aws_url }
    
    else:
        # Returns a message saying file does not exist in the bucket
        return {"message":"404: File not found"}


@app.post("/fetch-url-nexrad-from-name")
async def fetch_url_nexrad_from_name(userinput: base_model.UserInputName) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date

    # Checks if the provided file exists in nexrad bucket
    if basic_func.check_if_file_exists_in_s3_bucket(nexrad_bucket, userinput.name):

        # Generate file path from filename
        src_object_key = basic_func.path_from_filename_nexrad(userinput.name)

        # Define path where the file has to be written
        user_object_key = f'logs/nexrad/{userinput.name}'

        # Copy file from nexrad bucket to user bucket
        basic_func.copy_to_public_bucket(nexrad_bucket, src_object_key, user_bucket_name, user_object_key)

        # Generate link from user bucket
        aws_url = basic_func.generate_download_link_nexrad(user_bucket_name, user_object_key)

        # Returns the generated URL
        return {'url': aws_url }
    
    else:
        # Returns a message saying file does not exist in the bucket
        return {"message":"404: File not found"}


# user_bucket_name = os.environ.get('USER_BUCKET_NAME')
# user_object_key = f'logs/goes18/{UserInputName.name}'

# @app.post("/fetch_url_from_name")
# async def fetch_url_from_name(userinputname: UserInputName) -> dict:
#     aws_goes_url
#     return {'url': aws_goes_url }