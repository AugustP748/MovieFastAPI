# Pydantic
from pydantic import BaseModel, Field, EmailStr

# Files
from jwt_manager import create_token

# FastAPI
from fastapi.responses import JSONResponse
from fastapi import APIRouter

user_router = APIRouter()

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

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)