import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import boto3
import base_model

app =FastAPI()

load_dotenv()

s3client = boto3.client('s3', 
                        region_name = 'us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )

@app.get("/say_hello")
async def say_hello() -> dict:
    return {"message":"Hello World"}


@app.post("/fetch_url_nexrad")
async def fetch_url_nexrad(userinput: base_model.UserInputNexrad) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date
    aws_url = f"https://noaa-nexrad-level2.s3.amazonaws.com/index.html#{userinput.year:04}/{userinput.month:02}/{userinput.date:02}/{userinput.station}"
    
    return {'url': aws_url }

@app.post("/fetch_url_goes")
async def fetch_url_goes(userinput: base_model.UserInputGOES) -> dict:
    # if userinput.date > 31:
    #     return 400 bad request . return incorrect date
    aws_url = f"https://noaa-nexrad-level2.s3.amazonaws.com/index.html#{userinput.year:04}/{userinput.day:02}/{userinput.hour:02}"
    return {'url': aws_url }

# goes18_bucket = 'noaa-goes18'
# user_bucket_name = os.environ.get('USER_BUCKET_NAME')
# user_object_key = f'logs/goes18/{UserInputName.name}'

# @app.post("/fetch_url_from_name")
# async def fetch_url_from_name(userinputname: UserInputName) -> dict:
#     aws_goes_url
#     return {'url': aws_goes_url }