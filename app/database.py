"""Database configuration and session management.

This module handles SQLAlchemy async engine setup and provides
database session dependency for FastAPI routes.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@db/blogdb")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    """Provide database session dependency for FastAPI routes.
    
    Yields:
        AsyncSession: Database session that automatically closes after use.
    """
    async with SessionLocal() as session:
        yield session 