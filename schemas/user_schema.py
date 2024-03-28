from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re
from settings import settings

class UserNameSchema(BaseModel):
    username : str = Field(min_length=3,max_length=10)

class UserPasswordSchema(BaseModel):
    password:str
    @field_validator('password')
    @classmethod
    def validate_password(cls,value):
        password_pattern = r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@*#$%^&]).{8,}$'
        if re.match(password_pattern,value):
            return value
        raise ValueError("Password must contain atleast one uppercase, one special character, one number and minimum length of 8")
    

class UserSchema(UserNameSchema,UserPasswordSchema):
    email: EmailStr
    superkey: Optional[str] = None
    @field_validator('superkey')
    @classmethod
    def validate_superkey(cls,value):
        if not value :
            return False
        if value == settings.superkey:
            return True
        raise ValueError("Invalid superkey")
