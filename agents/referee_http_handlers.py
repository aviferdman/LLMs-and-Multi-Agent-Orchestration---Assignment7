"""HTTP handlers for referee agent."""

from SHARED.constants import Field, LogEvent, MessageType, Status
from SHARED.contracts import build_run_match_ack


def handle_run_match(message: dict, referee, background_tasks) -> dict:
    """Handle RUN_MATCH message from LM."""
    match_id = message.get(Field.MATCH_ID)
    background_tasks.add_task(
        referee.run_match,
        message.get(Field.LEAGUE_ID),
        message.get(Field.ROUND_ID),
        match_id,
        message.get(Field.PLAYER_A),
        message.get(Field.PLAYER_B),
        message.get("player_a_endpoint"),
        message.get("player_b_endpoint"),
    )
    return build_run_match_ack(match_id)


def handle_game_join_ack(message: dict, referee) -> dict:
    """Handle GAME_JOIN_ACK from player."""
    match_id = message.get(Field.MATCH_ID)
    player_id = message.get(Field.SENDER)
    if match_id in referee.active_matches:
        ctx = referee.active_matches[match_id]["context"]
        ctx.record_join(player_id, message.get(Field.CONVERSATION_ID))
        referee.logger.log_message(
            "PLAYER_JOINED", {Field.MATCH_ID: match_id, Field.PLAYER_ID: player_id}
        )
    return {Field.STATUS: Status.OK}


def handle_parity_choice(message: dict, referee) -> dict:
    """Handle PARITY_CHOICE from player."""
    match_id = message.get(Field.MATCH_ID)
    player_id = message.get(Field.SENDER)
    choice = message.get(Field.CHOICE)
    if match_id in referee.active_matches:
        ctx = referee.active_matches[match_id]["context"]
        ctx.record_choice(player_id, choice)
        referee.logger.log_message(
            "CHOICE_RECEIVED",
            {
                Field.MATCH_ID: match_id,
                Field.PLAYER_ID: player_id,
                Field.CHOICE: choice,
            },
        )
    return {Field.STATUS: Status.OK}
