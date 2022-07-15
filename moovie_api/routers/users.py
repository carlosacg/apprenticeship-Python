from fastapi import APIRouter
from typing import List as TList
from moovie_api.models import User
from moovie_api.schemas import User as SUser, UserCreate, UserPhoto
from moovie_api.dependencies import get_token_header
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from moovie_api.database import get_db
from moovie_api.auth import get_current_active_user

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(get_token_header)],

)


@router.post("/", response_model=SUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create users
    """
    db_user = db.query(User).filter(
        User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_hashed_password = user.password + "notreallyhashed"
    fake_salted_password = user.password + "notreallysalted"
    db_user = User(email=user.email, password_hash=fake_hashed_password,
                   full_name=user.full_name, password_salt=fake_salted_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=TList[SUser])
def get_users(current_user: User = Depends(get_current_active_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint to get all users
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=SUser)
def get_user(current_user: User = Depends(get_current_active_user), user_id: int = 0, db: Session = Depends(get_db)):
    """
    Endpoint to get a specific user by id
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=SUser)
def update_user(user_id: str, user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to update a specific user
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email
    db_user.full_name = user.full_name
    fake_hashed_password = user.password + "notreallyhashed"
    fake_salted_password = user.password + "notreallysalted"
    db_user.password_salt = fake_salted_password
    db_user.password_hash = fake_hashed_password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.patch("/{user_id}/upload_picture", response_model=UserPhoto)
def upload_profile_picture(user_id: str, picture_url: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to upload profile photo path
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.photo_path = picture_url
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.patch("/{user_id}/remove_upload_picture", response_model=SUser)
def remove_profile_picture(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Endpoint to remove profile photo path
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.photo_path = None
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
