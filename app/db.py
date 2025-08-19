# app/db.py
import os
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine as create_sync_engine  # used only when needed

from app.config import DATABASE_URL_ASYNC

# Declarative base - this is safe to import without connecting.
Base = declarative_base()

# Lazy async engine and sessionmaker (created only when get_async_engine() is called)
_async_engine = None
_async_sessionmaker = None

ngine = create_async_engine(DATABASE_URL_ASYNC, future=True, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

def get_async_engine():
    """Lazily create and return the async engine. Call at runtime only."""
    global _async_engine
    if _async_engine is None:
        _async_engine = create_async_engine(DATABASE_URL, future=True, echo=False)
    return _async_engine

def get_async_sessionmaker():
    """Lazily return an async sessionmaker bound to the async engine."""
    global _async_sessionmaker
    if _async_sessionmaker is None:
        _async_sessionmaker = sessionmaker(
            bind=get_async_engine(), class_=AsyncSession, expire_on_commit=False
        )
    return _async_sessionmaker

async def get_async_session() -> AsyncSession:
    """Use this in your endpoints to get an async session (async with ...)."""
    SessionLocal = get_async_sessionmaker()
    async with SessionLocal() as session:
        yield session

# Create a simple sync engine function for Alembic or synchronous scripts
def get_sync_engine():
    # Return a sync engine built from SYNC_DATABASE_URL (no +asyncpg)
    return create_sync_engine(SYNC_DATABASE_URL, future=True, echo=False)
