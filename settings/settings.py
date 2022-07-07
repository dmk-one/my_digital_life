from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DB_HOST = 'localhost'
DB_NAME = 'mdl'
DB_USER = 'dmk'
DB_PASSWORD = 'dmk5402'
DB_PORT = 5432

SQLALCHEMY_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
ASYNC_SQLALCHEMY_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(
    ASYNC_SQLALCHEMY_URL
)
a = engine.
session_factory = sessionmaker(engine, class_=AsyncSession)

session = session_factory()

# Datetime configs
USE_TIMEZONE = True
DATETIME_FORMAT = '%d-%m-%y %H:%M:%S'
DATE_FORMAT = '%d-%m-%y'
