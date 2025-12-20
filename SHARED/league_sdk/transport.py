"""Transport abstraction layer - supports HTTP, STDIO, and future transports.

This module provides transport independence as required by the spec:
"If changing transport (HTTP ↔ STDIO) affects business logic, the design is invalid"
"""

import asyncio
import json
import random
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import httpx


class BaseTransport(ABC):
    """Abstract base class for all transports - defines the interface."""

    @abstractmethod
    async def send(
        self, endpoint: str, message: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Send a message and return the response."""

    @abstractmethod
    async def send_with_retry(
        self,
        endpoint: str,
        message: Dict[str, Any],
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> Optional[Dict[str, Any]]:
        """Send a message with retry logic."""


class HTTPTransport(BaseTransport):
    """HTTP transport implementation using httpx."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def send(
        self, endpoint: str, message: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Send HTTP POST message to endpoint."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    endpoint, json=message, headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
        except (httpx.TimeoutException, httpx.HTTPError):
            return None

    async def send_with_retry(
        self,
        endpoint: str,
        message: Dict[str, Any],
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> Optional[Dict[str, Any]]:
        """Send message with exponential backoff and jitter."""
        for attempt in range(max_retries):
            result = await self.send(endpoint, message)
            if result is not None:
                return result
            if attempt < max_retries - 1:
                base_delay = retry_delay * (2**attempt)
                jitter = random.uniform(0, retry_delay * 0.5)
                await asyncio.sleep(base_delay + jitter)
        return None


class STDIOTransport(BaseTransport):
    """STDIO transport for future MCP compatibility (JSON lines via stdin/stdout)."""

    async def send(
        self, endpoint: str, message: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Send message via stdout and read response from stdin."""
        try:
            sys.stdout.write(json.dumps(message) + "\n")
            sys.stdout.flush()
            response_line = sys.stdin.readline()
            return json.loads(response_line.strip()) if response_line else None
        except (json.JSONDecodeError, IOError):
            return None

    async def send_with_retry(
        self,
        endpoint: str,
        message: Dict[str, Any],
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> Optional[Dict[str, Any]]:
        """Send with retry logic."""
        for attempt in range(max_retries):
            result = await self.send(endpoint, message)
            if result is not None:
                return result
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay * (attempt + 1))
        return None


class TransportType:
    """Transport type identifiers."""

    HTTP = "http"
    STDIO = "stdio"


_TRANSPORT_REGISTRY = {
    TransportType.HTTP: HTTPTransport,
    TransportType.STDIO: STDIOTransport,
}


def create_transport(
    transport_type: str = TransportType.HTTP, **kwargs
) -> BaseTransport:
    """Factory function to create a transport instance."""
    transport_class = _TRANSPORT_REGISTRY.get(transport_type)
    if transport_class is None:
        raise ValueError(f"Unknown transport type: {transport_type}")
    return transport_class(**kwargs)


def register_transport(transport_type: str, transport_class: type) -> None:
    """Register a new transport type (for extensions)."""
    if not issubclass(transport_class, BaseTransport):
        raise TypeError("Transport class must extend BaseTransport")
    _TRANSPORT_REGISTRY[transport_type] = transport_class
