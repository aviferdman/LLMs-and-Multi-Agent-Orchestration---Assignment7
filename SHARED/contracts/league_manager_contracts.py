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

def build_start_league(
    league_id: str,
    sender: str
) -> Dict[str, Any]:
    """Build START_LEAGUE message (Launcher → LM)."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.START_LEAGUE,
        Field.LEAGUE_ID: league_id,
        Field.SENDER: sender
    }

def build_league_status(
    league_id: str,
    status: str,
    current_round: int = 0,
    total_rounds: int = 0,
    matches_completed: int = 0
) -> Dict[str, Any]:
    """Build LEAGUE_STATUS response message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_STATUS,
        Field.LEAGUE_ID: league_id,
        Field.STATUS: status,
        "current_round": current_round,
        "total_rounds": total_rounds,
        "matches_completed": matches_completed
    }

def build_run_match(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    player_a: str,
    player_a_endpoint: str,
    player_b: str,
    player_b_endpoint: str
) -> Dict[str, Any]:
    """Build RUN_MATCH message (LM → Referee)."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.RUN_MATCH,
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        Field.MATCH_ID: match_id,
        Field.REFEREE_ID: referee_id,
        Field.PLAYER_A: player_a,
        "player_a_endpoint": player_a_endpoint,
        Field.PLAYER_B: player_b,
        "player_b_endpoint": player_b_endpoint
    }

def build_run_match_ack(
    match_id: str,
    status: str = Status.ACKNOWLEDGED
) -> Dict[str, Any]:
    """Build RUN_MATCH_ACK message (Referee → LM)."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.RUN_MATCH_ACK,
        Field.MATCH_ID: match_id,
        Field.STATUS: status
    }
