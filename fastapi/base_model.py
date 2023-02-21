from pydantic import BaseModel, Field, validator
from typing import Dict

class UserInput(BaseModel):
    year:int
    month:int
    date:int
    station:str

class UserInputNexrad(BaseModel):
    year:int
    month:int
    date:int
    station:str

    @validator('year')
    def validate_year(cls, v):
        if len(str(v)) > 4:
            raise ValueError('Year must have at most 4 digits')
        return v

class UserInputGOES(BaseModel):
    year:int
    day:int
    hour:int

    @validator('year')
    def validate_year(cls, v):
        if len(str(v)) > 4:
            raise ValueError('Year must have at most 4 digits')
        return v

class UserInputName(BaseModel):
    name:str

class ResponseModel(BaseModel):
    message: str
    status_code: int
    data: Dict