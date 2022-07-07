from uuid import uuid4
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from settings import settings

ORMBaseModel = declarative_base()


class AbstractORMBaseModel(ORMBaseModel):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)


class Customer(AbstractORMBaseModel):
    __tablename__ = 'customer'

    tg_id = Column(Integer(), unique=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True, index=True)
    first_name = Column(String(255), nullable=False, unique=True)
    is_bot = Column(Boolean, nullable=False, default=False)
    language_code = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_activity = Column(DateTime(timezone=settings.USE_TIMEZONE), onupdate=func.now(), nullable=True)
    registration_date = Column(DateTime(timezone=settings.USE_TIMEZONE), server_default=func.now(), nullable=False)

