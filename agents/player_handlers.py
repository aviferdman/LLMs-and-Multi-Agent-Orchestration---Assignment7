"""Player message handlers - extracted for line count compliance."""

from SHARED.constants import Field, LogEvent, MessageType, Status
from SHARED.contracts import build_choose_parity_response, build_game_join_ack
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
        match_id=msg.get(Field.MATCH_ID),
        player_id=player_id,
        conversation_id=conversation_id,
        accept=True,
    )


def handle_parity_call(player_id: str, msg: dict, strategy, logger) -> dict:
    """Handle CHOOSE_PARITY_CALL message."""
    history = PlayerHistoryRepository(player_id).load_history().get(Field.OPPONENT_CHOICES, [])
    choice = strategy.choose_parity(history)
    logger.log_message(
        LogEvent.PARITY_CHOICE_MADE,
        {Field.MATCH_ID: msg.get(Field.MATCH_ID), Field.PARITY_CHOICE: choice},
    )
    return build_choose_parity_response(
        match_id=msg.get(Field.MATCH_ID),
        player_id=player_id,
        parity_choice=choice,
        conversation_id=msg.get(Field.CONVERSATION_ID),
    )


def handle_game_over(msg: dict, logger):
    """Handle GAME_OVER message."""
    game_result = msg.get(Field.GAME_RESULT, {})
    logger.log_message(
        LogEvent.GAME_OVER_RECEIVED,
        {
            Field.MATCH_ID: msg.get(Field.MATCH_ID),
            Field.WINNER: game_result.get("winner_player_id"),
        },
    )
