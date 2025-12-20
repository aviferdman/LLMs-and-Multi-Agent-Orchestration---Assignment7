"""Player message handlers - extracted for line count compliance."""

from SHARED.constants import Field, LogEvent, MessageType, Status
from SHARED.contracts import build_game_join_ack, build_parity_choice
from SHARED.league_sdk.repositories import PlayerHistoryRepository


def handle_invitation(player_id: str, msg: dict, logger, conversation_id: str) -> dict:
    """Handle GAME_INVITATION message."""
    logger.log_message(
        LogEvent.GAME_INVITATION_RECEIVED,
        {
            Field.MATCH_ID: msg.get(Field.MATCH_ID),
            Field.OPPONENT_ID: msg.get(Field.OPPONENT_ID),
        },
    )
    return build_game_join_ack(
        msg.get(Field.LEAGUE_ID),
        msg.get(Field.ROUND_ID),
        msg.get(Field.MATCH_ID),
        player_id,
        conversation_id,
    )


def handle_parity_call(player_id: str, msg: dict, strategy, logger) -> dict:
    """Handle CHOOSE_PARITY_CALL message."""
    history = (
        PlayerHistoryRepository(player_id)
        .load_history()
        .get(Field.OPPONENT_CHOICES, [])
    )
    choice = strategy.choose_parity(history)
    logger.log_message(
        LogEvent.PARITY_CHOICE_MADE,
        {Field.MATCH_ID: msg.get(Field.MATCH_ID), Field.CHOICE: choice},
    )
    return build_parity_choice(
        msg.get(Field.LEAGUE_ID),
        msg.get(Field.ROUND_ID),
        msg.get(Field.MATCH_ID),
        player_id,
        choice,
        msg.get(Field.CONVERSATION_ID),
    )


def handle_game_over(msg: dict, logger):
    """Handle GAME_OVER message."""
    logger.log_message(
        LogEvent.GAME_OVER_RECEIVED,
        {
            Field.MATCH_ID: msg.get(Field.MATCH_ID),
            Field.WINNER: msg.get(Field.WINNER),
        },
    )
