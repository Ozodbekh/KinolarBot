from sqlalchemy import create_engine
from config import Conf


class DB:
    DB_NAME = Conf.DB.DB_NAME
    DB_USER = Conf.DB.DB_USER
    DB_PASSWORD = Conf.DB.DB_PASSWORD
    DB_HOST = Conf.DB.DB_HOST
    DB_PORT = Conf.DB.DB_PORT
    engine = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"