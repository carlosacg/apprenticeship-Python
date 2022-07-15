from fastapi import APIRouter
from typing import List as TList
from moovie_api.models import List, User, Movie
from moovie_api.schemas import SchemaList, SchemaListCreate, UserList
from fastapi import Depends, HTTPException
from moovie_api.dependencies import get_token_header
from sqlalchemy.orm import Session
from moovie_api.database import get_db


router = APIRouter(
    prefix='/lists',
    tags=['lists'],
    dependencies=[Depends(get_token_header)],
)


@router.get("/get_user_list/{user_id}", response_model=UserList)
def get_user_lists(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=SchemaListCreate)
def create_list(list_obj: SchemaList, db: Session = Depends(get_db)):
    """
    Endpoint to create lists
    """
    try:
        db_list = List(
            name=list_obj.name, description=list_obj.description, public=list_obj.public)
        db.add(db_list)
        db.commit()
        db.refresh(db_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return db_list


@router.get("/", response_model=TList[SchemaListCreate])
def get_lists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint to get all lists
    """
    lists = db.query(List).offset(skip).limit(limit).all()
    return lists


@router.get("/{list_id}", response_model=SchemaListCreate)
def get_list(list_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a specific list by id
    """
    db_list = db.query(List).filter(List.id == list_id).first()
    if db_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    return db_list


@router.put("/{list_id}", response_model=SchemaListCreate)
def update_list(list_id: str, list: SchemaList, db: Session = Depends(get_db)):
    """
    Endpoint to update a specific user
    """
    db_list = db.query(List).filter(List.id == list_id).first()
    if db_list is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_list.name = list.name
    db_list.description = list.description
    db_list.public = list.public
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


@router.delete("/{list_id}")
def delete_list(list_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to delete a specific list
    """
    try:
        db_list = db.query(List).filter(
            List.id == list_id).first()
        if db_list is None:
            raise HTTPException(status_code=404, detail="List not found")
        db.delete(db_list)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        return "List deleted successfully"


@router.get("/{list_id}/add_movie")
def add_movie_to_list(list_id: str, movie_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to add a movie to a specific list
    """
    try:
        db_list = db.query(List).filter(
            List.id == list_id).first()
        if db_list is None:
            raise HTTPException(status_code=404, detail="List not found")

        db_movie = db.query(Movie).filter(
            Movie.id == movie_id).first()
        if db_movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")

        db_list.movies.append(db_movie)
        db.add(db_list)
        db.commit()
        db.refresh(db_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        return "Movie added to the list successfully"


@router.delete("/{list_id}/remove_movie")
def remove_movie_from_list(list_id: str, movie_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to remove a movie from a specific list
    """
    try:
        db_list = db.query(List).filter(
            List.id == list_id).first()
        if db_list is None:
            raise HTTPException(status_code=404, detail="List not found")

        db_movie = db.query(Movie).filter(
            Movie.id == movie_id).first()
        if db_movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")

        db_list.movies.remove(db_movie)
        db.add(db_list)
        db.commit()
        db.refresh(db_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        return "Movie removed from the list successfully"
