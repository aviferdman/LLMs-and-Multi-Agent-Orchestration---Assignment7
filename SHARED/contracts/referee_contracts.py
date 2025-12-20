"""Referee contract definitions."""

from typing import Any, Dict

from SHARED.constants import Field, MessageType

from .base_contract import create_base_message


def build_game_invitation(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    player_id: str,
    opponent_id: str,
) -> Dict[str, Any]:
    """Build GAME_INVITATION message."""
    msg = create_base_message(
        MessageType.GAME_INVITATION, league_id, round_id, match_id, referee_id
    )
    msg[Field.PLAYER_ID] = player_id
    msg[Field.OPPONENT_ID] = opponent_id
    return msg


def build_choose_parity_call(
    league_id: str, round_id: int, match_id: str, referee_id: str, player_id: str
) -> Dict[str, Any]:
    """Build CHOOSE_PARITY_CALL message."""
    msg = create_base_message(
        MessageType.CHOOSE_PARITY_CALL, league_id, round_id, match_id, referee_id
    )
    msg[Field.PLAYER_ID] = player_id
    return msg


def build_game_over(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    winner: str,
    drawn_number: int,
    player_a_choice: str,
    player_b_choice: str,
) -> Dict[str, Any]:
    """Build GAME_OVER message."""
    msg = create_base_message(MessageType.GAME_OVER, league_id, round_id, match_id, referee_id)
    msg[Field.WINNER] = winner
    msg[Field.DRAWN_NUMBER] = drawn_number
    msg[Field.PLAYER_A_CHOICE] = player_a_choice
    msg[Field.PLAYER_B_CHOICE] = player_b_choice
    return msg


def build_match_result_report(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    player_a: str,
    player_b: str,
    winner: str,
) -> Dict[str, Any]:
    """Build MATCH_RESULT_REPORT message."""
    msg = create_base_message(
        MessageType.MATCH_RESULT_REPORT, league_id, round_id, match_id, referee_id
    )
    msg[Field.PLAYER_A] = player_a
    msg[Field.PLAYER_B] = player_b
    msg[Field.WINNER] = winner
    return msg


def build_game_error(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    error_code: str,
    error_message: str,
    details: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Build GAME_ERROR message."""
    msg = create_base_message(MessageType.GAME_ERROR, league_id, round_id, match_id, referee_id)
    msg["error_code"] = error_code
    msg["error_message"] = error_message
    if details:
        msg["details"] = details
    return msg
