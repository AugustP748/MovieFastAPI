# Python
from typing import List

# Files
from config.database import Session
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

# FastAPI
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

movie_router = APIRouter()

# Get all movies
@movie_router.get('/movies', 
         tags=['movies'], 
         response_model=List[Movie], 
         status_code=200, 
         dependencies=[Depends(JWTBearer())],
         summary="Show all Movies")
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_all_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# Get a movie
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie,summary="Show a movie")
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    
    db = Session()
    result = MovieService(db).get_a_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={'message': 'Movie not found'})
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))


# Show movies by category
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404,content={'message': 'Movie/s not found'})
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Create a new movie
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "The movie was created successfully"})

# Update a movie
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie)-> dict:
    
    db = Session()
    result = MovieService(db).get_a_movie(id)
    
    if not result:
        return JSONResponse(status_code=404,content={'message': 'Movie/s not found'})
    else:
        MovieService(db).update_movie(id, movie)
        return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

# Delete a movie
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    
    db = Session()
    result = MovieService(db).get_a_movie(id)
    
    if not result:
        return JSONResponse(status_code=404,content={'message': 'Movie/s not found'})
    else:
        MovieService(db).delete_movie(id)
        return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})