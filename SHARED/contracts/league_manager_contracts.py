"""League Manager contract definitions."""

from typing import Dict, Any
from .base_contract import create_base_message
from SHARED.constants import (
    PROTOCOL_VERSION,
    MessageType,
    Field,
    Status
)

def build_referee_register_request(
    referee_id: str,
    endpoint: str
) -> Dict[str, Any]:
    """Build REFEREE_REGISTER_REQUEST message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.REFEREE_REGISTER_REQUEST,
        Field.REFEREE_ID: referee_id,
        Field.ENDPOINT: endpoint
    }

def build_referee_register_response(
    referee_id: str,
    auth_token: str,
    status: str = Status.REGISTERED
) -> Dict[str, Any]:
    """Build REFEREE_REGISTER_RESPONSE message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.REFEREE_REGISTER_RESPONSE,
        Field.REFEREE_ID: referee_id,
        Field.AUTH_TOKEN: auth_token,
        Field.STATUS: status
    }

def build_league_register_request(
    player_id: str,
    endpoint: str
) -> Dict[str, Any]:
    """Build LEAGUE_REGISTER_REQUEST message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_REGISTER_REQUEST,
        Field.PLAYER_ID: player_id,
        Field.ENDPOINT: endpoint
    }

def build_league_register_response(
    player_id: str,
    league_id: str,
    auth_token: str,
    status: str = Status.REGISTERED
) -> Dict[str, Any]:
    """Build LEAGUE_REGISTER_RESPONSE message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_REGISTER_RESPONSE,
        Field.PLAYER_ID: player_id,
        Field.LEAGUE_ID: league_id,
        Field.AUTH_TOKEN: auth_token,
        Field.STATUS: status
    }

def build_match_result_ack(
    match_id: str,
    status: str = Status.RECORDED
) -> Dict[str, Any]:
    """Build MATCH_RESULT_ACK message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.MATCH_RESULT_ACK,
        Field.MATCH_ID: match_id,
        Field.STATUS: status
    }
