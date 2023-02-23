from pydantic import BaseModel, Field, validator
from typing import Dict

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

class Login(BaseModel):
    username: str
    password: str

class UserInput(BaseModel):
    year:int
    month:int
    date:int
    station:str


# class UserInputNexrad(BaseModel):
#     year:int
#     month:int
#     date:int
#     station:str
#     filename:str


#     @validator('year')
#     def validate_year(cls, v):
#         if len(str(v)) > 4:
#             raise ValueError('Year must have at most 4 digits')
#         return v


# class UserInputGOES(BaseModel):
#     year:int
#     day:int
#     hour:int
#     filename:str


#     @validator('year')
#     def validate_year(cls, v):
#         if len(str(v)) > 4:
#             raise ValueError('Year must have at most 4 digits')
#         return v


class UserInputName(BaseModel):
    name:str


# class ResponseModel(BaseModel):
#     message: str
#     status_code: int
#     data: Dict