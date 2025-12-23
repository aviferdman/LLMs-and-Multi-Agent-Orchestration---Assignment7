"""Game flow contract builders.

Handles game invitation and choice request messages.
"""

from typing import Any, Dict, Optional

from SHARED.constants import Field, MessageType
from SHARED.protocol_constants import generate_deadline

from .base_contract import create_base_message, create_game_message


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

    Args:
        league_id: League identifier
        round_id: Round number
        match_id: Match identifier
        referee_id: Referee identifier (e.g., 'REF01')
        player_id: Target player identifier
        opponent_id: Opponent player identifier
        role_in_match: Player's role ('PLAYER_A' or 'PLAYER_B')
        game_type: Type of game (default: 'even_odd')
        conversation_id: Optional conversation ID

    Returns:
        GAME_INVITATION message dictionary
    """
    msg = create_game_message(
        message_type=MessageType.GAME_INVITATION,
        sender_type="referee",
        sender_id=referee_id,
        league_id=league_id,
        round_id=round_id,
        match_id=match_id,
        conversation_id=conversation_id,
    )
    msg[Field.GAME_TYPE] = game_type
    msg[Field.ROLE_IN_MATCH] = role_in_match
    msg[Field.OPPONENT_ID] = opponent_id
    return msg


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

    Args:
        league_id: League identifier
        round_id: Round number
        match_id: Match identifier
        referee_id: Referee identifier
        player_id: Target player identifier
        opponent_id: Opponent player identifier
        player_standings: Player's current standings (wins, losses, draws)
        game_type: Type of game (default: 'even_odd')
        timeout_seconds: Response timeout in seconds (default: 30)
        conversation_id: Optional conversation ID

    Returns:
        CHOOSE_PARITY_CALL message dictionary
    """
    msg = create_base_message(
        message_type=MessageType.CHOOSE_PARITY_CALL,
        sender_type="referee",
        sender_id=referee_id,
        conversation_id=conversation_id,
    )
    msg[Field.MATCH_ID] = match_id
    msg[Field.PLAYER_ID] = player_id
    msg[Field.GAME_TYPE] = game_type
    msg[Field.CONTEXT] = {
        "opponent_id": opponent_id,
        "round_id": round_id,
        "your_standings": player_standings,
    }
    msg[Field.DEADLINE] = generate_deadline(timeout_seconds)
    return msg
