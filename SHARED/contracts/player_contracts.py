"""Player contract definitions.

Player-sourced messages:
- LEAGUE_REGISTER_REQUEST: Player → League Manager
- GAME_JOIN_ACK: Player → Referee
- CHOOSE_PARITY_RESPONSE: Player → Referee
- LEAGUE_QUERY: Player → League Manager
"""

from typing import Any, Dict, Optional

from SHARED.constants import Field, MessageType
from SHARED.protocol_constants import JSONRPCMethod, generate_timestamp

from .base_contract import create_base_message, create_game_message
from .jsonrpc_helpers import wrap_jsonrpc_request, wrap_jsonrpc_response


def build_game_join_ack(
    match_id: str,
    player_id: str,
    conversation_id: str,
    accept: bool = True,
    request_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Build GAME_JOIN_ACK message.

    Sent by player to referee in response to GAME_INVITATION.
    Must be sent within 5 seconds or player forfeits.
    """
    result = create_base_message(
        message_type=MessageType.GAME_JOIN_ACK,
        sender_type="player",
        sender_id=player_id,
        conversation_id=conversation_id,
    )
    result[Field.MATCH_ID] = match_id
    result[Field.PLAYER_ID] = player_id
    result[Field.ARRIVAL_TIMESTAMP] = generate_timestamp()
    result[Field.ACCEPT] = accept
    if request_id is not None:
        return wrap_jsonrpc_response(result, request_id)
    return wrap_jsonrpc_request(JSONRPCMethod.GAME_JOIN_ACK, result, agent_id=player_id)


def build_choose_parity_response(
    match_id: str,
    player_id: str,
    parity_choice: str,
    conversation_id: str,
    request_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Build CHOOSE_PARITY_RESPONSE message.

    Sent by player to referee in response to CHOOSE_PARITY_CALL.
    Must be sent within 30 seconds or player gets technical loss.
    """
    result = create_base_message(
        message_type=MessageType.CHOOSE_PARITY_RESPONSE,
        sender_type="player",
        sender_id=player_id,
        conversation_id=conversation_id,
    )
    result[Field.MATCH_ID] = match_id
    result[Field.PLAYER_ID] = player_id
    result[Field.PARITY_CHOICE] = parity_choice
    if request_id is not None:
        return wrap_jsonrpc_response(result, request_id)
    return wrap_jsonrpc_request(JSONRPCMethod.CHOOSE_PARITY_RESPONSE, result, agent_id=player_id)


def build_league_query(
    player_id: str,
    league_id: str,
    auth_token: str,
    query_type: str,
    query_params: Optional[Dict[str, Any]] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_QUERY message. Sent by player to league manager to request information."""
    params = create_base_message(
        message_type=MessageType.LEAGUE_QUERY,
        sender_type="player",
        sender_id=player_id,
        conversation_id=conversation_id,
    )
    params[Field.AUTH_TOKEN] = auth_token
    params[Field.LEAGUE_ID] = league_id
    params[Field.QUERY_TYPE] = query_type
    if query_params:
        params[Field.QUERY_PARAMS] = query_params
    return wrap_jsonrpc_request(JSONRPCMethod.LEAGUE_QUERY, params, agent_id=player_id)


# DEPRECATED: Alias for backward compatibility
def build_parity_choice(
    league_id: str, round_id: int, match_id: str, player_id: str,
    choice: str, conversation_id: str,
) -> Dict[str, Any]:
    """DEPRECATED: Use build_choose_parity_response instead."""
    import warnings
    warnings.warn(
        "build_parity_choice is deprecated, use build_choose_parity_response",
        DeprecationWarning, stacklevel=2,
    )
    return build_choose_parity_response(
        match_id=match_id, player_id=player_id,
        parity_choice=choice, conversation_id=conversation_id,
    )

