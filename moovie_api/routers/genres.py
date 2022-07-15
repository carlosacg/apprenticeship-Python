from fastapi import APIRouter
from typing import List as TList
from moovie_api.models import Genre
from moovie_api.schemas import Genre as SGenre, GenreCreate
from moovie_api.dependencies import get_token_header
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from moovie_api.database import get_db


router = APIRouter(
    prefix='/genres',
    tags=['genres'],
    dependencies=[Depends(get_token_header)],

)


@router.post("/", response_model=SGenre)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create genres
    """
    db_genre = Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


@router.get("/", response_model=TList[SGenre])
def get_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint to get all genres
    """
    genres = db.query(Genre).offset(skip).limit(limit).all()
    return genres


@router.get("/{genre_id}", response_model=SGenre)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a specific genre by id
    """
    db_genre = db.query(Genre).filter(
        Genre.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre
