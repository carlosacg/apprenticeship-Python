from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Request
from conf.envs import USER_DB, PASSWORD_DB, HOST_DB, DB_NAME

SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@{host}/{db}".format(
    user=USER_DB,
    password=PASSWORD_DB,
    host=HOST_DB,
    db=DB_NAME
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_engine():
    return engine


def get_session_local():
    return SessionLocal()


def get_db(request: Request):
    return request.state.db


Base = declarative_base()
