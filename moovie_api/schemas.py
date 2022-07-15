from typing import List, Union
from pydantic import BaseModel
import datetime


class Video(BaseModel):
    id: int
    size: int
    type: str
    url: str

    class Config:
        orm_mode = True


class SchemaListCreate(BaseModel):
    id: int
    name: str
    description: str
    public: bool

    class Config:
        orm_mode = True


class SchemaList(BaseModel):
    name: str
    description: str
    public: bool

    class Config:
        orm_mode = True


class Genre(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GenreCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserPhoto(BaseModel):
    id: int
    email: str
    full_name: str
    photo_path: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserList(UserBase):
    id: int
    lists: List[SchemaList] = []

    class Config:
        orm_mode = True


class MovieCreate(BaseModel):
    title: str
    tagline: str
    overview: str
    release_date: datetime.date
    poster_url: Union[str, None] = None
    backdrop_url: Union[str, None] = None
    imdbi_id: Union[str, None] = None

    class Config:
        orm_mode = True


class Movie(BaseModel):
    title: str
    tagline: str
    overview: str
    release_date: datetime.date
    poster_url: Union[str, None] = None
    backdrop_url: Union[str, None] = None
    imdbi_id: Union[str, None] = None
    lists: List[SchemaList] = []
    genres: List[Genre] = []

    class Config:
        orm_mode = True
