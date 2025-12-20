"""HTTP client utilities for agent communication."""

import httpx
from typing import Dict, Any, Optional
import asyncio
import random


async def send_message(
    endpoint: str,
    message: Dict[str, Any],
    timeout: int = 30
) -> Optional[Dict[str, Any]]:
    """Send HTTP POST message to agent endpoint."""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                endpoint,
                json=message,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        return None
    except httpx.HTTPError:
        return None

async def send_with_retry(
    endpoint: str,
    message: Dict[str, Any],
    max_retries: int = 3,
    timeout: int = 30,
    retry_delay: int = 1,
    use_exponential_backoff: bool = True
) -> Optional[Dict[str, Any]]:
    """Send message with retry logic using exponential backoff with jitter.
    
    Args:
        endpoint: Target URL
        message: Message payload
        max_retries: Maximum retry attempts
        timeout: HTTP timeout in seconds
        retry_delay: Base delay in seconds
        use_exponential_backoff: If True, use exponential backoff with jitter
    
    Returns:
        Response dict or None on failure
    """
    for attempt in range(max_retries):
        result = await send_message(endpoint, message, timeout)
        if result is not None:
            return result
        
        if attempt < max_retries - 1:
            if use_exponential_backoff:
                # Exponential backoff: delay = base * (2^attempt) + jitter
                base_delay = retry_delay * (2 ** attempt)
                jitter = random.uniform(0, retry_delay * 0.5)
                delay = base_delay + jitter
            else:
                # Linear backoff (legacy)
                delay = retry_delay * (attempt + 1)
            await asyncio.sleep(delay)
    
    return None

def send_message_sync(
    endpoint: str,
    message: Dict[str, Any],
    timeout: int = 30
) -> Optional[Dict[str, Any]]:
    """Synchronous version of send_message."""
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                endpoint,
                json=message,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        return None
    except httpx.HTTPError:
        return None
