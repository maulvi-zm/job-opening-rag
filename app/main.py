import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.routers import webhooks

app = FastAPI(
    title="Job Opening WhatsApp Bot",
    description="WhatsApp bot for job opening recommendations using RAG",
    version="0.1.0"
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
    return {
        "status": "healthy",
        "database": "not connected",  # TODO: Add DB health check
        "redis": "not connected"  # TODO: Add Redis health check
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
