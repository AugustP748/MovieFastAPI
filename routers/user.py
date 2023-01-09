
# Files
from utils.jwt_manager import create_token
from schemas.user import User

# FastAPI
from fastapi.responses import JSONResponse
from fastapi import APIRouter

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)