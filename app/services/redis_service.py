from typing import Optional, Any, Dict
from app.clients.redis_client import get_redis_client
from app.core.config import settings
import json


async def set_session(
    phone_number: str,
    session_data: Dict[str, Any],
    ttl: Optional[int] = None
) -> bool:
    """
    Store session data in Redis.
    
    Args:
        phone_number: User's phone number (used as key prefix)
        session_data: Session data to store
        ttl: Time to live in seconds (defaults to settings.session_timeout_minutes * 60)
    
    Returns:
        bool: True if successful
    """
    client = await get_redis_client()
    key = f"session:{phone_number}"
    ttl = ttl or (settings.session_timeout_minutes * 60)
    
    await client.setex(
        key,
        ttl,
        json.dumps(session_data)
    )
    return True


async def get_session(phone_number: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve session data from Redis.
    
    Args:
        phone_number: User's phone number
    
    Returns:
        Optional[Dict[str, Any]]: Session data or None if not found
    """
    client = await get_redis_client()
    key = f"session:{phone_number}"
    
    data = await client.get(key)
    if data:
        return json.loads(data)
    return None


async def delete_session(phone_number: str) -> bool:
    """
    Delete session data from Redis.
    
    Args:
        phone_number: User's phone number
    
    Returns:
        bool: True if deleted, False if not found
    """
    client = await get_redis_client()
    key = f"session:{phone_number}"
    
    result = await client.delete(key)
    return result > 0


async def set_cache(
    key: str,
    value: Any,
    ttl: Optional[int] = None
) -> bool:
    """
    Set a cache value in Redis.
    
    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (optional)
    
    Returns:
        bool: True if successful
    """
    client = await get_redis_client()
    
    if ttl:
        await client.setex(key, ttl, json.dumps(value))
    else:
        await client.set(key, json.dumps(value))
    return True


async def get_cache(key: str) -> Optional[Any]:
    """
    Get a cache value from Redis.
    
    Args:
        key: Cache key
    
    Returns:
        Optional[Any]: Cached value or None if not found
    """
    client = await get_redis_client()
    
    data = await client.get(key)
    if data:
        return json.loads(data)
    return None


async def delete_cache(key: str) -> bool:
    """
    Delete a cache value from Redis.
    
    Args:
        key: Cache key
    
    Returns:
        bool: True if deleted, False if not found
    """
    client = await get_redis_client()
    result = await client.delete(key)
    return result > 0

