"""Game flow contract builders.

Handles game invitation and choice request messages.
"""

from typing import Any, Dict, Optional

from SHARED.constants import Field, MessageType
from SHARED.protocol_constants import JSONRPCMethod, generate_deadline

from .base_contract import create_base_message, create_game_message
from .jsonrpc_helpers import wrap_jsonrpc_request


def build_game_invitation(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    player_id: str,
    opponent_id: str,
    role_in_match: str,
    game_type: str = "even_odd",
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build GAME_INVITATION message.

    Sent by referee to player to invite them to a match.
    Player must respond with GAME_JOIN_ACK within 5 seconds.
    """
    params = create_game_message(
        message_type=MessageType.GAME_INVITATION,
        sender_type="referee",
        sender_id=referee_id,
        league_id=league_id,
        round_id=round_id,
        match_id=match_id,
        conversation_id=conversation_id,
    )
    params[Field.GAME_TYPE] = game_type
    params[Field.ROLE_IN_MATCH] = role_in_match
    params[Field.OPPONENT_ID] = opponent_id
    return wrap_jsonrpc_request(JSONRPCMethod.GAME_INVITATION, params, agent_id=referee_id)


def build_choose_parity_call(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    player_id: str,
    opponent_id: str,
    player_standings: Dict[str, int],
    game_type: str = "even_odd",
    timeout_seconds: int = 30,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build CHOOSE_PARITY_CALL message.

    Sent by referee to player to request parity choice.
    Player must respond with CHOOSE_PARITY_RESPONSE within timeout.
    """
    params = create_base_message(
        message_type=MessageType.CHOOSE_PARITY_CALL,
        sender_type="referee",
        sender_id=referee_id,
        conversation_id=conversation_id,
    )
    params[Field.MATCH_ID] = match_id
    params[Field.PLAYER_ID] = player_id
    params[Field.GAME_TYPE] = game_type
    params[Field.CONTEXT] = {
        "opponent_id": opponent_id,
        "round_id": round_id,
        "your_standings": player_standings,
    }
    params[Field.DEADLINE] = generate_deadline(timeout_seconds)
    return wrap_jsonrpc_request(JSONRPCMethod.CHOOSE_PARITY, params, agent_id=referee_id)
