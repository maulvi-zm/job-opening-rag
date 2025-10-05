import asyncpg
from typing import Optional
from app.core.config import settings

# Global connection pool
_db_pool: Optional[asyncpg.Pool] = None


async def get_db_pool() -> asyncpg.Pool:
    """
    Get or create the database connection pool.
    
    Returns:
        asyncpg.Pool: The database connection pool
    """
    global _db_pool
    if _db_pool is None:
        _db_pool = await asyncpg.create_pool(
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
            min_size=5,
            max_size=20,
            command_timeout=60
        )
    return _db_pool


async def close_db_pool():
    """
    Close the database connection pool.
    """
    global _db_pool
    if _db_pool is not None:
        await _db_pool.close()
        _db_pool = None

