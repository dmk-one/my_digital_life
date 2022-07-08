from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from settings import settings

ORMBaseModel = declarative_base()


class AbstractORMBaseModel(ORMBaseModel):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True, nullable=False)


class User(AbstractORMBaseModel):
    __tablename__ = 'user'

    tg_id = Column(Integer(), unique=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True, index=True)
    first_name = Column(String(255), nullable=True, unique=True)
    last_name = Column(String(255), nullable=True, unique=True)
    phone_number = Column(Integer(), nullable=True)
    is_bot = Column(Boolean, nullable=False, default=False)
    language_code = Column(String(255), nullable=False)
    added_to_attachment_menu = Column(Boolean, nullable=True, default=False)
    can_join_groups = Column(Boolean, nullable=True, default=False)
    can_read_all_group_messages = Column(Boolean, nullable=True, default=False)
    supports_inline_queries = Column(Boolean, nullable=True, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_activity = Column(DateTime(timezone=settings.USE_TIMEZONE), onupdate=func.now(), nullable=False)
    registration_date = Column(DateTime(timezone=settings.USE_TIMEZONE), server_default=func.now(), nullable=False)

