"""Match control contract builders.

Handles match assignment and control messages.
"""

from typing import Any, Dict, Optional

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, Status
from SHARED.protocol_constants import (
    JSONRPCMethod,
    format_sender,
    generate_conversation_id,
    generate_timestamp,
)

from .jsonrpc_helpers import wrap_jsonrpc_request, wrap_jsonrpc_response


def build_match_result_ack(
    match_id: str,
    status: str = Status.RECORDED,
    conversation_id: Optional[str] = None,
    request_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Build MATCH_RESULT_ACK message."""
    result = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.MATCH_RESULT_ACK,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.MATCH_ID: match_id,
        Field.STATUS: status,
    }
    if request_id is not None:
        return wrap_jsonrpc_response(result, request_id)
    return wrap_jsonrpc_request(JSONRPCMethod.MATCH_RESULT_ACK, result, agent_id="LM")


def build_start_league(
    league_id: str,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build START_LEAGUE message."""
    params = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.START_LEAGUE,
        Field.SENDER: "launcher",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
    }
    return wrap_jsonrpc_request(JSONRPCMethod.START_LEAGUE, params, agent_id="LAUNCHER")


def build_league_status(
    league_id: str,
    status: str,
    current_round: int = 0,
    total_rounds: int = 0,
    matches_completed: int = 0,
    conversation_id: Optional[str] = None,
    request_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_STATUS response message."""
    result = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_STATUS,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.STATUS: status,
        "current_round": current_round,
        "total_rounds": total_rounds,
        "matches_completed": matches_completed,
    }
    if request_id is not None:
        return wrap_jsonrpc_response(result, request_id)
    return wrap_jsonrpc_request(JSONRPCMethod.LEAGUE_STATUS, result, agent_id="LM")


def build_run_match(
    league_id: str,
    round_id: int,
    match_id: str,
    player_a_id: str,
    player_a_endpoint: str,
    player_b_id: str,
    player_b_endpoint: str,
    game_type: str = "even_odd",
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build RUN_MATCH message."""
    params = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.RUN_MATCH,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        Field.MATCH_ID: match_id,
        Field.GAME_TYPE: game_type,
        Field.PLAYER_A_ID: player_a_id,
        Field.PLAYER_A_ENDPOINT: player_a_endpoint,
        Field.PLAYER_B_ID: player_b_id,
        Field.PLAYER_B_ENDPOINT: player_b_endpoint,
    }
    return wrap_jsonrpc_request(JSONRPCMethod.RUN_MATCH, params, agent_id="LM")


def build_shutdown_command(
    reason: Optional[str] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build SHUTDOWN_COMMAND message."""
    params = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.SHUTDOWN_COMMAND,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
    }
    if reason:
        params[Field.REASON] = reason
    return wrap_jsonrpc_request(JSONRPCMethod.SHUTDOWN, params, agent_id="LM")


def build_shutdown_ack(
    sender_type: str,
    sender_id: str,
    status: str = Status.ACKNOWLEDGED,
    conversation_id: Optional[str] = None,
    request_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Build SHUTDOWN_ACK message."""
    result = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.SHUTDOWN_ACK,
        Field.SENDER: format_sender(sender_type, sender_id),
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.STATUS: status,
    }
    if request_id is not None:
        return wrap_jsonrpc_response(result, request_id)
    return wrap_jsonrpc_request(JSONRPCMethod.SHUTDOWN_ACK, result, agent_id=sender_id)
