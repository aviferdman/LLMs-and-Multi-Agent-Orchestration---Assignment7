"""HTTP handlers for referee agent."""

from SHARED.constants import Field, LogEvent, MessageType, Status
from SHARED.league_sdk.endpoint_resolver import get_player_endpoint


def handle_round_announcement(message: dict, referee, background_tasks) -> dict:
    """Handle ROUND_ANNOUNCEMENT message from LM.

    Referee filters matches assigned to its endpoint and starts them.
    """
    league_id = message.get(Field.LEAGUE_ID)
    round_id = message.get(Field.ROUND_ID)
    matches = message.get(Field.MATCHES, [])

    # Filter matches assigned to this referee (by referee_endpoint)
    my_matches = [
        m for m in matches
        if m.get("referee_endpoint") == referee.endpoint
    ]

    referee.logger.log_message(
        "ROUND_ANNOUNCEMENT_RECEIVED",
        {
            "round_id": round_id,
            "total_matches": len(matches),
            "my_matches": len(my_matches),
        },
    )

    # Start each assigned match in background
    for match in my_matches:
        match_id = match.get("match_id")
        player_a_id = match.get("player_A_id")
        player_b_id = match.get("player_B_id")

        # Resolve player endpoints from config
        player_a_endpoint = get_player_endpoint(player_a_id)
        player_b_endpoint = get_player_endpoint(player_b_id)

        if not player_a_endpoint or not player_b_endpoint:
            referee.logger.log_error(
                LogEvent.ERROR,
                f"Cannot resolve endpoints for {player_a_id} or {player_b_id}",
            )
            continue

        referee.logger.log_message(
            "STARTING_MATCH",
            {
                Field.MATCH_ID: match_id,
                Field.PLAYER_A_ID: player_a_id,
                Field.PLAYER_B_ID: player_b_id,
            },
        )

        background_tasks.add_task(
            referee.run_match,
            league_id,
            round_id,
            match_id,
            player_a_id,
            player_b_id,
            player_a_endpoint,
            player_b_endpoint,
        )

    return {Field.STATUS: Status.ACKNOWLEDGED, "matches_started": len(my_matches)}


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
    """Handle CHOOSE_PARITY_RESPONSE from player."""
    match_id = message.get(Field.MATCH_ID)
    player_id = message.get(Field.SENDER)
    choice = message.get(Field.PARITY_CHOICE)
    if match_id in referee.active_matches:
        ctx = referee.active_matches[match_id]["context"]
        ctx.record_choice(player_id, choice)
        referee.logger.log_message(
            "CHOICE_RECEIVED",
            {
                Field.MATCH_ID: match_id,
                Field.PLAYER_ID: player_id,
                Field.PARITY_CHOICE: choice,
            },
        )
    return {Field.STATUS: Status.OK}


def handle_broadcast_message(message: dict, referee) -> dict:
    """Handle broadcast messages: ROUND_COMPLETED, LEAGUE_STANDINGS_UPDATE, LEAGUE_COMPLETED."""
    msg_type = message.get(Field.MESSAGE_TYPE)
    if msg_type == MessageType.ROUND_COMPLETED:
        referee.logger.log_message("ROUND_COMPLETED_RECEIVED", {"round_id": message.get(Field.ROUND_ID)})
    elif msg_type == MessageType.LEAGUE_STANDINGS_UPDATE:
        referee.logger.log_message("STANDINGS_UPDATE_RECEIVED", {"round_id": message.get(Field.ROUND_ID)})
    elif msg_type == MessageType.LEAGUE_COMPLETED:
        referee.logger.log_message("LEAGUE_COMPLETED_RECEIVED", {})
    return {Field.STATUS: Status.ACKNOWLEDGED}
