# Pydantic
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    email: EmailStr = Field(default=...)
    password:str = Field(default=...)
    
    class Config:
        schema_extra = {
            "example": {
                "email":"admin@gmail.com",
                "password":"admin"
            }
        }