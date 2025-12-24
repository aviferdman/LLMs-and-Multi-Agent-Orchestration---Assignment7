"""Transport abstraction layer with circuit breaker support."""

import asyncio
import json
import random
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import httpx

from SHARED.league_sdk.circuit_breaker import get_circuit_breaker_registry


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open."""

    def __init__(self, endpoint: str):
        super().__init__(f"Circuit OPEN: {endpoint}")


class BaseTransport(ABC):
    """Abstract transport interface."""

    @abstractmethod
    async def send(self, endpoint: str, message: Dict[str, Any]) -> Optional[Dict]:
        """Send message and return response."""

    @abstractmethod
    async def send_with_retry(
        self, endpoint: str, message: Dict[str, Any],
        max_retries: int = 3, retry_delay: float = 1.0, use_circuit_breaker: bool = True
    ) -> Optional[Dict]:
        """Send with retry and optional circuit breaker."""


class HTTPTransport(BaseTransport):
    """HTTP transport with circuit breaker."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self._cb = get_circuit_breaker_registry()

    async def send(self, endpoint: str, message: Dict[str, Any]) -> Optional[Dict]:
        """Send HTTP POST."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(endpoint, json=message)
                resp.raise_for_status()
                return resp.json()
        except (httpx.TimeoutException, httpx.HTTPError):
            return None

    async def send_with_retry(
        self, endpoint: str, message: Dict[str, Any],
        max_retries: int = 3, retry_delay: float = 1.0, use_circuit_breaker: bool = True
    ) -> Optional[Dict]:
        """Send with exponential backoff and circuit breaker."""
        if use_circuit_breaker and not self._cb.can_execute(endpoint):
            raise CircuitOpenError(endpoint)

        for attempt in range(max_retries):
            result = await self.send(endpoint, message)
            if result is not None:
                if use_circuit_breaker:
                    self._cb.record_success(endpoint)
                return result
            if use_circuit_breaker:
                self._cb.record_failure(endpoint)
            if attempt < max_retries - 1:
                delay = retry_delay * (2**attempt) + random.uniform(0, retry_delay * 0.5)
                await asyncio.sleep(delay)
        return None


class STDIOTransport(BaseTransport):
    """STDIO transport for MCP compatibility."""

    async def send(self, endpoint: str, message: Dict[str, Any]) -> Optional[Dict]:
        """Send via stdout/stdin."""
        try:
            sys.stdout.write(json.dumps(message) + "\n")
            sys.stdout.flush()
            line = sys.stdin.readline()
            return json.loads(line.strip()) if line else None
        except (json.JSONDecodeError, IOError):
            return None

    async def send_with_retry(
        self, endpoint: str, message: Dict[str, Any],
        max_retries: int = 3, retry_delay: float = 1.0, use_circuit_breaker: bool = False
    ) -> Optional[Dict]:
        """Send with retry (no circuit breaker for STDIO)."""
        for attempt in range(max_retries):
            result = await self.send(endpoint, message)
            if result is not None:
                return result
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay * (attempt + 1))
        return None


class TransportType:
    """Transport type constants."""
    HTTP = "http"
    STDIO = "stdio"


_REGISTRY = {TransportType.HTTP: HTTPTransport, TransportType.STDIO: STDIOTransport}


def create_transport(transport_type: str = TransportType.HTTP, **kwargs) -> BaseTransport:
    """Factory to create transport."""
    cls = _REGISTRY.get(transport_type)
    if cls is None:
        raise ValueError(f"Unknown transport: {transport_type}")
    return cls(**kwargs)


def register_transport(transport_type: str, transport_class: type) -> None:
    """Register custom transport type."""
    if not issubclass(transport_class, BaseTransport):
        raise TypeError("Must extend BaseTransport")
    _REGISTRY[transport_type] = transport_class
