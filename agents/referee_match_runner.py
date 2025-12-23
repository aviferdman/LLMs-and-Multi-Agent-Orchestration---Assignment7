"""Match execution logic for referee - Facade module.

This module provides the main match execution entry point.
Implementation is split into smaller modules for maintainability.
"""

from agents.referee_choices import collect_choices
from agents.referee_comm import notify_game_over, report_result
from agents.referee_invite import invite_players
from agents.referee_match_state import MatchContext, MatchState, MatchStateMachine
from SHARED.constants import Field, LogEvent


async def run_match_phases(
    referee,
    league_id: str,
    round_id: int,
    match_id: str,
    player_a: str,
    player_b: str,
    player_a_endpoint: str,
    player_b_endpoint: str,
):
    """Orchestrate a complete match (called when LM sends RUN_MATCH)."""
    referee.logger.log_message(
        LogEvent.MATCH_START,
        {
            Field.MATCH_ID: match_id,
            Field.PLAYER_A_ID: player_a,
            Field.PLAYER_B_ID: player_b,
        },
    )
    state_machine = MatchStateMachine()
    context = MatchContext(match_id, player_a, player_b)
    referee.active_matches[match_id] = {
        "state_machine": state_machine,
        "context": context,
    }
    # Phase 1: Invite players
    if not await invite_players(
        referee,
        context,
        league_id,
        round_id,
        match_id,
        player_a,
        player_b,
        player_a_endpoint,
        player_b_endpoint,
    ):
        return
    state_machine.transition(MatchState.COLLECTING_CHOICES)
    # Phase 2: Collect choices (handles timeout gracefully)
    both_responded, timeout_winner = await collect_choices(
        referee,
        context,
        league_id,
        round_id,
        match_id,
        player_a,
        player_b,
        player_a_endpoint,
        player_b_endpoint,
    )
    # Phase 3: Determine winner
    state_machine.transition(MatchState.DRAWING_NUMBER)
    if both_responded:
        # Normal case: both players responded, determine winner by game rules
        drawn_number = referee.game_rules.draw_number()
        winner = referee.game_rules.determine_winner(
            context.player_a_choice, context.player_b_choice, drawn_number
        )
    else:
        # Timeout case: winner determined by who responded
        drawn_number = 0  # No draw needed for timeout
        winner = timeout_winner
        referee.logger.log_message(
            "TIMEOUT_WINNER",
            {
                Field.MATCH_ID: match_id,
                Field.WINNER: winner,
                "reason": "opponent_timeout",
            },
        )
    referee.logger.log_message(
        "WINNER_DETERMINED",
        {
            Field.MATCH_ID: match_id,
            Field.WINNER: winner,
            Field.DRAWN_NUMBER: drawn_number,
            Field.PLAYER_A_CHOICE: context.player_a_choice,
            Field.PLAYER_B_CHOICE: context.player_b_choice,
        },
    )
    # Phase 4: Notify players
    await notify_game_over(
        referee,
        league_id,
        round_id,
        match_id,
        winner,
        drawn_number,
        context,
        player_a_endpoint,
        player_b_endpoint,
    )
    # Phase 5: Report to LM
    await report_result(
        referee, league_id, round_id, match_id, player_a, player_b, winner
    )
    state_machine.transition(MatchState.FINISHED)
    referee.logger.log_message(
        LogEvent.MATCH_COMPLETE, {Field.MATCH_ID: match_id, Field.WINNER: winner}
    )
    del referee.active_matches[match_id]
