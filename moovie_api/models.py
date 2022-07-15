from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import Date
from pydantic import BaseModel
from .database import Base
from typing import Union

list_movies = Table('list_movies', Base.metadata,
                    Column('list_id', Integer, ForeignKey('lists.id')),
                    Column('movie_id', Integer, ForeignKey('movies.id'))
                    )

movies_genres = Table('movies_genres', Base.metadata,
                      Column('movie_id', Integer, ForeignKey('movies.id')),
                      Column('genre_id', Integer, ForeignKey('genres.id'))
                      )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    photo_path = Column(String)
    password_salt = Column(String)
    password_hash = Column(String)

    lists = relationship("List", backref="owner")


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    public = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    tagline = Column(String)
    overview = Column(String)
    release_date = Column(Date)
    poster_url = Column(String)
    backdrop_url = Column(String)
    imdbi_id = Column(String)

    videos = relationship("Video", backref="movie")
    lists = relationship(
        "List",
        secondary=list_movies,
        backref="movies")
    genres = relationship(
        "Genre",
        secondary=movies_genres,
        backref="movies")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    size = Column(Integer)
    type = Column(String)
    url = Column(String)
    movie_id = Column(Integer, ForeignKey("movies.id"))


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
