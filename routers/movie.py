# Python
from typing import Optional, List

# Pydantic
from pydantic import BaseModel, Field

# Files
from config.database import Session
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

# FastAPI
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }

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

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
  
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie)-> dict:
    
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code=404,content={'message': 'Movie/s not found'})
    else:
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code=404,content={'message': 'Movie/s not found'})
    else:
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})