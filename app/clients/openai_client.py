from openai import AsyncOpenAI
from app.core.config import settings
from typing import Optional

# Global client instance
_openai_client: Optional[AsyncOpenAI] = None


def get_openai_client() -> AsyncOpenAI:
    """
    Get or create the OpenAI async client instance.
    
    Returns:
        AsyncOpenAI: The OpenAI client instance
    """
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _openai_client

