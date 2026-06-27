# backend/database.py
"""
PitchIQ Database Layer
Updated for PostgreSQL with connection pooling
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import event, text
from config import get_settings
import structlog
from typing import AsyncGenerator, Generator
import os

logger = structlog.get_logger(__name__)
settings = get_settings()


class Base(DeclarativeBase):
    """All SQLAlchemy ORM models inherit from this Base."""
    pass


def _build_async_engine() -> AsyncEngine:
    """
    Creates the async SQLAlchemy engine with connection pooling.
    """
    database_url = settings.database_url
    
    # Connection arguments
    connect_args = {}
    
    # SQLite specific
    if "sqlite" in database_url:
        connect_args = {"check_same_thread": False}
    
    # For PostgreSQL, use asyncpg
    if "postgresql" in database_url:
        # Ensure we're using asyncpg
        if "+asyncpg" not in database_url:
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(
        database_url,
        echo=settings.environment == "development",
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_timeout=settings.db_pool_timeout,
        pool_recycle=settings.db_pool_recycle,
        pool_pre_ping=settings.db_pool_pre_ping,
        connect_args=connect_args,
    )
    
    return engine


def _build_sync_engine() -> Engine:
    """
    Creates a sync engine for Alembic migrations.
    """
    database_url = settings.database_url
    
    # Convert async URL to sync for migrations
    if "postgresql" in database_url:
        sync_url = database_url.replace("+asyncpg", "+psycopg2")
        sync_url = sync_url.replace("postgresql+psycopg2", "postgresql")
    else:
        sync_url = database_url
    
    # For SQLite, use the same URL
    if "sqlite" in database_url:
        sync_url = database_url.replace("+aiosqlite", "")
    
    engine = create_engine(
        sync_url,
        echo=settings.environment == "development",
        pool_size=5,
        max_overflow=10,
    )
    
    return engine


# Module-level engines
async_engine: AsyncEngine = _build_async_engine()
sync_engine: Engine = _build_sync_engine()

# Session factories
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def init_db() -> None:
    """
    Creates all tables if they don't exist.
    """
    import models  # noqa: F401
    
    async with async_engine.begin() as conn:
        # For PostgreSQL, create extensions
        if "postgresql" in settings.database_url:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
        
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("database.initialized", url=settings.database_url)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session per request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> Generator[Session, None, None]:
    """
    Sync database session for Alembic and scripts.
    """
    with SyncSessionLocal() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


async def get_db_stats() -> dict:
    """
    Get database connection pool statistics.
    """
    if "postgresql" in settings.database_url:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("""
                SELECT 
                    pid,
                    usename,
                    application_name,
                    client_addr,
                    state,
                    query
                FROM pg_stat_activity
                WHERE datname = current_database()
            """))
            rows = result.fetchall()
            return {
                "total_connections": len(rows),
                "active_connections": len([r for r in rows if r.state == "active"]),
                "idle_connections": len([r for r in rows if r.state == "idle"]),
            }
    return {"status": "sqlite", "message": "Stats only available for PostgreSQL"}


async def test_connection() -> bool:
    """
    Test database connection.
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        logger.info("database.connection_test_successful")
        return True
    except Exception as e:
        logger.error("database.connection_test_failed", error=str(e))
        return False