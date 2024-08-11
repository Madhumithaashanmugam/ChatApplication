import uuid
from pydantic import BaseModel  
from typing import Optional
from uuid import UUID
from datetime import datetime

class CreateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    user_name: str
    email: str
    phone_number: str
    hashed_password: str
    created_datetime: datetime
    updated_datetime: datetime

class UpdateUser(BaseModel):
    first_name: str
    last_name: Optional[str]
    user_name:str
    email: str
    phone_number: str
    created_datetime: datetime
    updated_datetime: datetime

class ViewUser(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    user_name:str
    email: str
    phone_number: str
    created_datetime: Optional[datetime]
    updated_datetime: Optional[datetime]



class UserDetails(BaseModel):
    email: str
    first_name: str
    last_name: str


class TokenData(BaseModel):
    access_token: str
    token_type: str
    user: UserDetails

class Data(BaseModel):
    username:str
    password:str