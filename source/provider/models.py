from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from settings import settings
from source.service import domain

ORMBaseModel = declarative_base()


class AbstractORMBaseModel(ORMBaseModel):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True, nullable=False)


class Users(AbstractORMBaseModel):
    __tablename__ = 'users'

    tg_id = Column(BigInteger(), unique=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True, index=True)
    first_name = Column(String(255), nullable=False, unique=True)
    last_name = Column(String(255), nullable=True, unique=True)
    phone_number = Column(BigInteger(), nullable=True)
    is_bot = Column(Boolean, nullable=False, default=False)
    language_code = Column(String(255), nullable=False)
    added_to_attachment_menu = Column(Boolean, nullable=True, default=False)
    can_join_groups = Column(Boolean, nullable=True, default=False)
    can_read_all_group_messages = Column(Boolean, nullable=True, default=False)
    supports_inline_queries = Column(Boolean, nullable=True, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_activity = Column(DateTime(timezone=settings.USE_TIMEZONE), onupdate=func.now(), nullable=False)
    registration_date = Column(DateTime(timezone=settings.USE_TIMEZONE), server_default=func.now(), nullable=False)


class Assets(AbstractORMBaseModel):
    __tablename__ = 'assets'

    tg_id = Column(BigInteger, ForeignKey(f'{Users.__tablename__}.tg_id', ondelete='CASCADE'))
    type = Column(SmallInteger(), nullable=False, default=domain.AssetsTypes.CRYPTO.value)
    assets = Column(JSON)

    __table_args__ = (
        UniqueConstraint('tg_id', 'type', name='unique_tg_id_and_type'),
    )
