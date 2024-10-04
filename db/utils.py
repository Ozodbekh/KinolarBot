from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select

from db import db


# ----------------------------- ABSTRACTS ----------------------------------
class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def create(cls, **kwargs):
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get(cls, id_):
        query = select(cls).where(cls.id == id_)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return []

    @classmethod
    async def delete(cls, id_):
        query = sqlalchemy_delete(cls).where(cls.id == id_)
        await db.execute(query)
        await cls.commit()
        return True

    @classmethod
    async def get_all(cls):
        query = select(cls)
        objects = await db.execute(query)
        result = []
        for i in objects.all():
            result.append(i[0])
        return result

    @classmethod
    async def get_by_file_id(cls, file_id):
        query = select(cls).where(cls.file_id == file_id)
        objects = await db.execute(query)
        object_ = objects.first()
        if object_:
            return object_[0]
        else:
            return None
