
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

DATABASE_URL = (
    "postgresql+asyncpg://postgres:password@localhost:5432/enterprise_db"
)

# 1. Create engine once
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# 2. Create reusable session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def get_db():

    async with AsyncSessionLocal() as session:

        yield session