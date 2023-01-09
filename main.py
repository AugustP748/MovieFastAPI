
# Files
from config.database import engine, Base

# middlewares
from middlewares.error_handler import ErrorHandler

#routers
from routers.movie import movie_router
from routers.user import user_router

# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')




