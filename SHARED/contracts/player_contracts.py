"""Player contract definitions."""

from typing import Dict, Any
from .base_contract import create_base_message
from SHARED.constants import Field, MessageType

def build_game_join_ack(
    league_id: str,
    round_id: int,
    match_id: str,
    player_id: str,
    conversation_id: str
) -> Dict[str, Any]:
    """Build GAME_JOIN_ACK message."""
    return create_base_message(
        MessageType.GAME_JOIN_ACK,
        league_id,
        round_id,
        match_id,
        player_id,
        conversation_id
    )

def build_parity_choice(
    league_id: str,
    round_id: int,
    match_id: str,
    player_id: str,
    choice: str,
    conversation_id: str
) -> Dict[str, Any]:
    """Build PARITY_CHOICE message."""
    msg = create_base_message(
        MessageType.PARITY_CHOICE,
        league_id,
        round_id,
        match_id,
        player_id,
        conversation_id
    )
    msg[Field.CHOICE] = choice
    return msg
