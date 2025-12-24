"""Protocol and network-related constants.

This module re-exports all protocol constants from split modules.
Import from this module for backward compatibility.
"""

import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict

# Protocol version
PROTOCOL_VERSION = "league.v2"
MCP_PATH = "/mcp"
LOCALHOST = "localhost"
SERVER_HOST = "0.0.0.0"
HTTP_PROTOCOL = "http"

# JSON-RPC 2.0 constants
JSONRPC_VERSION = "2.0"


class JSONRPCMethod(str, Enum):
    """JSON-RPC method names for protocol messages."""
    # Registration
    REGISTER_REFEREE = "register_referee"
    REGISTER_REFEREE_RESPONSE = "register_referee_response"
    REGISTER_PLAYER = "register_player"
    REGISTER_PLAYER_RESPONSE = "register_player_response"
    # Game flow
    GAME_INVITATION = "game_invitation"
    GAME_JOIN_ACK = "game_join_ack"
    CHOOSE_PARITY = "choose_parity"
    CHOOSE_PARITY_RESPONSE = "choose_parity_response"
    # Game results
    GAME_OVER = "game_over"
    MATCH_RESULT_REPORT = "match_result_report"
    MATCH_RESULT_ACK = "match_result_ack"
    GAME_ERROR = "game_error"
    # Match control
    RUN_MATCH = "run_match"
    RUN_MATCH_ACK = "run_match_ack"
    # Round lifecycle
    ROUND_ANNOUNCEMENT = "round_announcement"
    ROUND_COMPLETED = "round_completed"
    LEAGUE_STANDINGS_UPDATE = "league_standings_update"
    LEAGUE_COMPLETED = "league_completed"
    LEAGUE_ERROR = "league_error"
    # League control
    START_LEAGUE = "start_league"
    LEAGUE_STATUS = "league_status"
    LEAGUE_QUERY = "league_query"
    LEAGUE_QUERY_RESPONSE = "league_query_response"
    # Shutdown
    SHUTDOWN = "shutdown"
    SHUTDOWN_ACK = "shutdown_ack"


# Per-agent request ID counters
_request_id_counters: Dict[str, int] = {}


def generate_request_id(agent_id: str = "default") -> int:
    """Generate sequential request ID for an agent."""
    if agent_id not in _request_id_counters:
        _request_id_counters[agent_id] = 0
    _request_id_counters[agent_id] += 1
    return _request_id_counters[agent_id]


def reset_request_id_counter(agent_id: str = None) -> None:
    """Reset request ID counter (for testing)."""
    global _request_id_counters
    if agent_id is None:
        _request_id_counters = {}
    elif agent_id in _request_id_counters:
        del _request_id_counters[agent_id]


# Re-export from split modules
from .protocol_types import MessageType, Status, Timeout
from .protocol_fields import Field


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

