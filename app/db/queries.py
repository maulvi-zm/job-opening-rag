from typing import Optional, List, Dict, Any
from app.clients.database import get_db_pool


async def execute_query(
    query: str,
    *args,
    **kwargs
) -> str:
    """
    Execute a query that doesn't return results (INSERT, UPDATE, DELETE).
    
    Args:
        query: SQL query string
        *args: Query parameters
        **kwargs: Additional parameters
    
    Returns:
        str: Status message from the database
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        return await conn.execute(query, *args, **kwargs)


async def fetch_one(
    query: str,
    *args,
    **kwargs
) -> Optional[Dict[str, Any]]:
    """
    Fetch a single row from the database.
    
    Args:
        query: SQL query string
        *args: Query parameters
        **kwargs: Additional parameters
    
    Returns:
        Optional[Dict[str, Any]]: Row as a dictionary or None if not found
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, *args, **kwargs)
        return dict(row) if row else None


async def fetch_all(
    query: str,
    *args,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Fetch all rows from the database.
    
    Args:
        query: SQL query string
        *args: Query parameters
        **kwargs: Additional parameters
    
    Returns:
        List[Dict[str, Any]]: List of rows as dictionaries
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *args, **kwargs)
        return [dict(row) for row in rows]


async def fetch_val(
    query: str,
    *args,
    column: int = 0,
    **kwargs
) -> Any:
    """
    Fetch a single value from the database.
    
    Args:
        query: SQL query string
        *args: Query parameters
        column: Column index to fetch (default: 0)
        **kwargs: Additional parameters
    
    Returns:
        Any: The value or None if not found
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval(query, *args, column=column, **kwargs)

