from typing import Optional, List, Dict
from app.clients.openai_client import get_openai_client
from app.core.config import settings


async def chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    **kwargs
) -> str:
    """
    Generate a chat completion using OpenAI's API.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        model: Model to use (defaults to settings.openai_model)
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens to generate
        **kwargs: Additional parameters to pass to the API
    
    Returns:
        str: The generated response content
    """
    client = get_openai_client()
    model = model or settings.openai_model
    
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )
    
    return response.choices[0].message.content


async def create_embeddings(
    text: str,
    model: str = "text-embedding-3-small"
) -> List[float]:
    """
    Create embeddings for the given text using OpenAI's API.
    
    Args:
        text: Text to create embeddings for
        model: Embedding model to use
    
    Returns:
        List[float]: The embedding vector
    """
    client = get_openai_client()
    
    response = await client.embeddings.create(
        model=model,
        input=text
    )
    
    return response.data[0].embedding


async def batch_create_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Create embeddings for multiple texts in a single API call.
    
    Args:
        texts: List of texts to create embeddings for
        model: Embedding model to use
    
    Returns:
        List[List[float]]: List of embedding vectors
    """
    client = get_openai_client()
    
    response = await client.embeddings.create(
        model=model,
        input=texts
    )
    
    return [item.embedding for item in response.data]

