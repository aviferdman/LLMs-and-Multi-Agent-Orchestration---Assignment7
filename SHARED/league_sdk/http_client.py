"""HTTP client utilities for agent communication."""

import httpx
from typing import Dict, Any, Optional
import asyncio

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
    timeout: int = 30
) -> Optional[Dict[str, Any]]:
    """Send message with retry logic."""
    for attempt in range(max_retries):
        result = await send_message(endpoint, message, timeout)
        if result is not None:
            return result
        
        if attempt < max_retries - 1:
            await asyncio.sleep(1 * (attempt + 1))
    
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
