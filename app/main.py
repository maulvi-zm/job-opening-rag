import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.routers import webhooks
from app.clients.database import get_db_pool, close_db_pool
from app.clients.redis_client import get_redis_client, close_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup: Initialize connections
    try:
        await get_db_pool()
        await get_redis_client()
        print("✓ Database and Redis connections initialized")
    except Exception as e:
        print(f"✗ Failed to initialize connections: {e}")
    
    yield
    
    # Shutdown: Close connections
    try:
        await close_db_pool()
        await close_redis_client()
        print("✓ Database and Redis connections closed")
    except Exception as e:
        print(f"✗ Failed to close connections: {e}")


app = FastAPI(
    title="Job Opening WhatsApp Bot",
    description="WhatsApp bot for job opening recommendations using RAG",
    version="0.1.0",
    lifespan=lifespan
)

# Include routers
app.include_router(webhooks.router)


@app.get("/")
async def root():
    return {
        "message": "Job Opening WhatsApp Bot API",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint with database and Redis status.
    """
    from app.clients.database import get_db_pool
    from app.clients.redis_client import get_redis_client
    
    db_status = "healthy"
    redis_status = "healthy"
    
    # Check database
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Check Redis
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"
    
    overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded"
    
    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
