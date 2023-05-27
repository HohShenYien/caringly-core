from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.sql import func

from server.extensions import db

BaseModel = declarative_base()


class Base(BaseModel):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        unique=True,
        type_=UUID(as_uuid=False),
        server_default=text("uuid_generate_v4()"),
    )

    def apply_kwargs(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        return self

    @classmethod
    def query(cls, **kw):
        q = db.session.query(cls)

        if kw:
            q = q.filter_by(**kw)

        return q

    @classmethod
    def get(cls, id):
        return cls.query().get(id)

    @classmethod
    def exists(cls, **kw):
        return cls.query(**kw).first() is not None
