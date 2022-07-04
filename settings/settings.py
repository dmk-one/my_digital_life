from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DB_HOST = 'localhost'
DB_NAME = 'ami'
DB_USER = 'ami'
DB_PASSWORD = 'secret'
DB_PORT = 5432

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(
    DATABASE_URL
)
session_factory = sessionmaker(engine, class_=AsyncSession)

session = session_factory()
