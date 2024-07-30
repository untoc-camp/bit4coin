from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    api_key: str
    api_key_secret: str

class UserResponse(BaseModel):
    id: int
    user_name: str
    email: EmailStr

    class Config:
        orm_mode = True

class Userlogin(BaseModel):
    user_name_login: str
    password_login: str

class TokenData(BaseModel):
    token: str