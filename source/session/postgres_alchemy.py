from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from settings import settings


engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_URL,
    echo=settings.SQLALCHEMY_ECHO,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
)

async_session = AsyncSession(engine)
