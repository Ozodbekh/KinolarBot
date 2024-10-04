import datetime
from sqlalchemy import BigInteger, Boolean, Integer, Column, Text, DateTime, func, SMALLINT
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase, declared_attr
from db.utils import AbstractClass


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower() + "s"


class CreatedModel(Base, AbstractClass):
    __abstract__ = True

    created_at = Column(DateTime(), default=datetime.datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime(), onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow,
                        server_default=func.now())


class User(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fullname: Mapped[str] = mapped_column(VARCHAR(56))
    username: Mapped[str] = mapped_column(VARCHAR(56))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Movie(CreatedModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(VARCHAR(255))
    message_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class ChannelGroupList(CreatedModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(VARCHAR(255))
    username_: Mapped[str] = mapped_column(VARCHAR(56))

class Advertising(CreatedModel):
    id: Mapped[int] = mapped_column(SMALLINT, primary_key=True, autoincrement=True)
    admin_id: Mapped[int] = mapped_column(BigInteger)