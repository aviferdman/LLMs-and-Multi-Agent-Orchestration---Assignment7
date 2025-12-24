"""Game result contract builders for game over, match result, and error messages."""

from typing import Any, Dict, Optional

from SHARED.constants import Field, MessageType
from SHARED.protocol_constants import JSONRPCMethod

from .base_contract import create_base_message, create_game_message
from .jsonrpc_helpers import wrap_jsonrpc_request, wrap_jsonrpc_response


def build_game_over(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    status: str,
    winner_player_id: Optional[str],
    drawn_number: int,
    number_parity: str,
    choices: Dict[str, str],
    reason: str,
    game_type: str = "even_odd",
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build GAME_OVER message sent by referee to both players when game finishes."""
    params = create_base_message(
        message_type=MessageType.GAME_OVER,
        sender_type="referee",
        sender_id=referee_id,
        conversation_id=conversation_id,
    )
    params[Field.MATCH_ID] = match_id
    params[Field.GAME_TYPE] = game_type
    params[Field.GAME_RESULT] = {
        "status": status,
        "winner_player_id": winner_player_id,
        "drawn_number": drawn_number,
        "number_parity": number_parity,
        "choices": choices,
        "reason": reason,
    }
    return wrap_jsonrpc_request(JSONRPCMethod.GAME_OVER, params, agent_id=referee_id)


def build_match_result_report(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    winner: Optional[str],
    score: Dict[str, int],
    drawn_number: int,
    choices: Dict[str, str],
    game_type: str = "even_odd",
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build MATCH_RESULT_REPORT message sent by referee to LM after game completion."""
    params = create_game_message(
        message_type=MessageType.MATCH_RESULT_REPORT,
        sender_type="referee",
        sender_id=referee_id,
        league_id=league_id,
        round_id=round_id,
        match_id=match_id,
        conversation_id=conversation_id,
    )
    params[Field.GAME_TYPE] = game_type
    params[Field.RESULT] = {
        "winner": winner,
        "score": score,
        "details": {"drawn_number": drawn_number, "choices": choices},
    }
    return wrap_jsonrpc_request(JSONRPCMethod.MATCH_RESULT_REPORT, params, agent_id=referee_id)


def build_game_error(
    match_id: str,
    referee_id: str,
    error_code: str,
    error_description: str,
    affected_player: str,
    action_required: str,
    retry_info: Optional[Dict[str, Any]] = None,
    consequence: Optional[str] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build GAME_ERROR message sent by referee when a game-level error occurs."""
    params = create_base_message(
        message_type=MessageType.GAME_ERROR,
        sender_type="referee",
        sender_id=referee_id,
        conversation_id=conversation_id,
    )
    params[Field.MATCH_ID] = match_id
    params[Field.ERROR_CODE] = error_code
    params[Field.ERROR_DESCRIPTION] = error_description
    params[Field.AFFECTED_PLAYER] = affected_player
    params[Field.ACTION_REQUIRED] = action_required
    if retry_info:
        params[Field.RETRY_INFO] = retry_info
    if consequence:
        params[Field.CONSEQUENCE] = consequence
    return wrap_jsonrpc_request(JSONRPCMethod.GAME_ERROR, params, agent_id=referee_id)


def build_run_match_ack(
    match_id: str,
    referee_id: str,
    status: str = "acknowledged",
    conversation_id: Optional[str] = None,
    request_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Build RUN_MATCH_ACK message sent by referee acknowledging match assignment."""
    result = create_base_message(
        message_type=MessageType.RUN_MATCH_ACK,
        sender_type="referee",
        sender_id=referee_id,
        conversation_id=conversation_id,
    )
    result[Field.MATCH_ID] = match_id
    result[Field.STATUS] = status
    if request_id is not None:
        return wrap_jsonrpc_response(result, request_id)
    return wrap_jsonrpc_request(JSONRPCMethod.RUN_MATCH_ACK, result, agent_id=referee_id)
