"""Agent communication service - transport-agnostic messaging layer.

This module provides a high-level API for agent communication that abstracts
away the transport mechanism. Agents should use this instead of http_client directly.
"""

from typing import Any, Dict, Optional

from SHARED.league_sdk.config_loader import load_system_config
from SHARED.league_sdk.transport import (BaseTransport, HTTPTransport,
                                         TransportType, create_transport)

# Module-level transport instance (singleton pattern)
_transport: Optional[BaseTransport] = None
_system_config = None


def get_transport() -> BaseTransport:
    """Get or create the global transport instance."""
    global _transport, _system_config
    if _transport is None:
        _system_config = load_system_config()
        # Transport type could be configurable via system config in future
        transport_type = getattr(_system_config, "transport_type", TransportType.HTTP)
        timeout = _system_config.timeouts.get("http_request", 30)
        _transport = create_transport(transport_type, timeout=timeout)
    return _transport


def get_config():
    """Get system config (lazy load)."""
    global _system_config
    if _system_config is None:
        _system_config = load_system_config()
    return _system_config


async def send(endpoint: str, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Send a message via the configured transport."""
    transport = get_transport()
    return await transport.send(endpoint, message)


async def send_with_retry(
    endpoint: str,
    message: Dict[str, Any],
    max_retries: int = None,
    timeout: int = None,
    retry_delay: float = None,
) -> Optional[Dict[str, Any]]:
    """Send a message with retry logic via the configured transport."""
    transport = get_transport()
    config = get_config()

    # Use config defaults if not specified
    if max_retries is None:
        max_retries = config.retry_policy.get("max_retries", 3)
    if retry_delay is None:
        retry_delay = config.retry_policy.get("retry_delay", 1)

    return await transport.send_with_retry(endpoint, message, max_retries, retry_delay)


def set_transport(transport: BaseTransport) -> None:
    """Override the global transport (useful for testing or switching transports)."""
    global _transport
    _transport = transport


def reset_transport() -> None:
    """Reset the transport to force re-initialization."""
    global _transport
    _transport = None
