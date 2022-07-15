from fastapi import APIRouter
from typing import List as TList
from moovie_api.models import Movie
from moovie_api.schemas import Movie as SMovie, MovieCreate
from moovie_api.dependencies import get_token_header
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from moovie_api.database import get_db


router = APIRouter(
    prefix='/movies',
    tags=['movies'],
    dependencies=[Depends(get_token_header)],

)


@router.post("/", response_model=MovieCreate)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create movies
    """
    try:
        db_movie = Movie(title=movie.title, tagline=movie.tagline, overview=movie.overview, release_date=movie.release_date,
                         poster_url=movie.poster_url, backdrop_url=movie.backdrop_url, imdbi_id=movie.imdbi_id)
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return db_movie


@router.get("/", response_model=TList[SMovie])
def get_movies(skip: int = 0, limit: int = 100, query: str = '', sort: str = '+', db: Session = Depends(get_db)):
    """
    Endpoint to get all movies with sorting, pagination, and filtering
    """
    movies = db.query(Movie)
    if query:
        movies = movies.filter(Movie.title.contains(query))
    if sort == '+':
        movies = movies.order_by(Movie.title.asc())
    else:
        movies = movies.order_by(Movie.title.desc())

    return movies.offset(skip).limit(limit).all()


@router.get("/{movie_id}", response_model=SMovie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a specific user by id
    """
    db_movie = db.query(Movie).filter(
        Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie
