from fastapi import FastAPI, Request, Response
from .models import Base
from typing import Union
from .database import get_session_local, get_engine
from .routers import movies, lists, genres, users
from moovie_api.database import get_db
from moovie_api.models import User, Token
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from moovie_api.schemas import User as SUser
from moovie_api.auth import get_user, get_current_active_user
from conf.envs import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Base.metadata.create_all(bind=get_engine())

app = FastAPI()


def verify_password(plain_password, hashed_password):
    """
        Fake verify hashed password
    """
    # return pwd_context.verify(plain_password, hashed_password)
    if plain_password == hashed_password:
        return True


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session = Depends(get_db), email: str = '', password: str = ''):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/users/me/", response_model=SUser)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = get_session_local()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

app.include_router(movies.router)
app.include_router(lists.router)
app.include_router(genres.router)
app.include_router(users.router)
