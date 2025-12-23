"""Player contract definitions.

Player-sourced messages:
- LEAGUE_REGISTER_REQUEST: Player → League Manager
- GAME_JOIN_ACK: Player → Referee
- CHOOSE_PARITY_RESPONSE: Player → Referee
- LEAGUE_QUERY: Player → League Manager
"""

from typing import Any, Dict, Optional

from SHARED.constants import Field, MessageType
from SHARED.protocol_constants import generate_timestamp

from .base_contract import create_base_message, create_game_message


def build_game_join_ack(
    match_id: str,
    player_id: str,
    conversation_id: str,
    accept: bool = True,
) -> Dict[str, Any]:
    """Build GAME_JOIN_ACK message.

    Sent by player to referee in response to GAME_INVITATION.
    Must be sent within 5 seconds or player forfeits.

    Args:
        match_id: Match identifier
        player_id: Player identifier (e.g., 'P01')
        conversation_id: Conversation ID from the invitation
        accept: Whether player accepts the invitation

    Returns:
        GAME_JOIN_ACK message dictionary
    """
    msg = create_base_message(
        message_type=MessageType.GAME_JOIN_ACK,
        sender_type="player",
        sender_id=player_id,
        conversation_id=conversation_id,
    )
    msg[Field.MATCH_ID] = match_id
    msg[Field.PLAYER_ID] = player_id
    msg[Field.ARRIVAL_TIMESTAMP] = generate_timestamp()
    msg[Field.ACCEPT] = accept
    return msg


def build_choose_parity_response(
    match_id: str,
    player_id: str,
    parity_choice: str,
    conversation_id: str,
) -> Dict[str, Any]:
    """Build CHOOSE_PARITY_RESPONSE message.

    Sent by player to referee in response to CHOOSE_PARITY_CALL.
    Must be sent within 30 seconds or player gets technical loss.

    Args:
        match_id: Match identifier
        player_id: Player identifier (e.g., 'P01')
        parity_choice: Player's choice ('even' or 'odd')
        conversation_id: Conversation ID from the call

    Returns:
        CHOOSE_PARITY_RESPONSE message dictionary
    """
    msg = create_base_message(
        message_type=MessageType.CHOOSE_PARITY_RESPONSE,
        sender_type="player",
        sender_id=player_id,
        conversation_id=conversation_id,
    )
    msg[Field.MATCH_ID] = match_id
    msg[Field.PLAYER_ID] = player_id
    msg[Field.PARITY_CHOICE] = parity_choice
    return msg


def build_league_query(
    player_id: str,
    league_id: str,
    auth_token: str,
    query_type: str,
    query_params: Optional[Dict[str, Any]] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_QUERY message.

    Sent by player to league manager to request information.

    Args:
        player_id: Player identifier
        league_id: League identifier
        auth_token: Authentication token
        query_type: Type of query (e.g., 'GET_NEXT_MATCH', 'GET_STANDINGS')
        query_params: Optional query parameters
        conversation_id: Optional conversation ID

    Returns:
        LEAGUE_QUERY message dictionary
    """
    msg = create_base_message(
        message_type=MessageType.LEAGUE_QUERY,
        sender_type="player",
        sender_id=player_id,
        conversation_id=conversation_id,
    )
    msg[Field.AUTH_TOKEN] = auth_token
    msg[Field.LEAGUE_ID] = league_id
    msg[Field.QUERY_TYPE] = query_type
    if query_params:
        msg[Field.QUERY_PARAMS] = query_params
    return msg


# DEPRECATED: Alias for backward compatibility
def build_parity_choice(
    league_id: str,
    round_id: int,
    match_id: str,
    player_id: str,
    choice: str,
    conversation_id: str,
) -> Dict[str, Any]:
    """DEPRECATED: Use build_choose_parity_response instead."""
    import warnings
    warnings.warn(
        "build_parity_choice is deprecated, use build_choose_parity_response",
        DeprecationWarning,
        stacklevel=2,
    )
    return build_choose_parity_response(
        match_id=match_id,
        player_id=player_id,
        parity_choice=choice,
        conversation_id=conversation_id,
    )
