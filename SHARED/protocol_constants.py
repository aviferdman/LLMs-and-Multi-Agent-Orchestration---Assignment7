"""Protocol and network-related constants.

This module re-exports all protocol constants from split modules.
Import from this module for backward compatibility.
"""

import uuid
from datetime import datetime, timedelta

# Protocol version
PROTOCOL_VERSION = "league.v2"
MCP_PATH = "/mcp"
LOCALHOST = "localhost"
SERVER_HOST = "0.0.0.0"
HTTP_PROTOCOL = "http"

# Re-export from split modules
from .protocol_types import MessageType, Status, Timeout
from .protocol_fields import Field
from .protocol_network import Port, Endpoint


def generate_timestamp() -> str:
    """Generate ISO-8601 timestamp with Z suffix."""
    return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


def generate_deadline(seconds: int) -> str:
    """Generate deadline timestamp (current time + seconds)."""
    deadline = datetime.utcnow() + timedelta(seconds=seconds)
    return deadline.isoformat(timespec="milliseconds") + "Z"


def generate_conversation_id() -> str:
    """Generate unique conversation ID."""
    return str(uuid.uuid4())


def format_sender(entity_type: str, entity_id: str) -> str:
    """Format sender field according to protocol.

    Args:
        entity_type: 'player', 'referee', 'league_manager', or 'launcher'
        entity_id: The entity's identifier (e.g., 'P01', 'REF01')

    Returns:
        Formatted sender string (e.g., 'player:P01', 'referee:REF01')
    """
    if entity_type in ("league_manager", "launcher"):
        return entity_type
    return f"{entity_type}:{entity_id}"


# Schema versions for data structures
STANDINGS_SCHEMA_VERSION = 1

