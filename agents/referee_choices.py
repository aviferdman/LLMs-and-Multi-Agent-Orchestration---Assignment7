"""Choice collection logic for referee matches."""

from SHARED.constants import Field, LogEvent, Winner
from SHARED.contracts import build_choose_parity_call
from SHARED.league_sdk.agent_comm import send


async def collect_choices(
    referee, context, league_id, round_id, match_id, player_a, player_b, ep_a, ep_b
):
    """Collect parity choices. Returns (both_responded, timeout_winner_or_None)."""
    # Get player standings for context (empty dict if not available)
    player_standings = {}
    req_a = build_choose_parity_call(
        league_id=league_id,
        round_id=round_id,
        match_id=match_id,
        referee_id=referee.referee_id,
        player_id=player_a,
        opponent_id=player_b,
        player_standings=player_standings,
        timeout_seconds=30,
    )
    req_b = build_choose_parity_call(
        league_id=league_id,
        round_id=round_id,
        match_id=match_id,
        referee_id=referee.referee_id,
        player_id=player_b,
        opponent_id=player_a,
        player_standings=player_standings,
        timeout_seconds=30,
    )
    resp_a, resp_b = await send(ep_a, req_a), await send(ep_b, req_b)
    choice_a = (
        resp_a.get(Field.PARITY_CHOICE)
        if resp_a and Field.PARITY_CHOICE in resp_a
        else None
    )
    choice_b = (
        resp_b.get(Field.PARITY_CHOICE)
        if resp_b and Field.PARITY_CHOICE in resp_b
        else None
    )
    if choice_a:
        context.record_choice(player_a, choice_a)
    if choice_b:
        context.record_choice(player_b, choice_b)
    # Handle timeout scenarios
    if not choice_a and not choice_b:
        referee.logger.log_error(LogEvent.TIMEOUT, "Both players timed out - DRAW")
        return (False, Winner.DRAW)
    if not choice_a:
        referee.logger.log_error(
            LogEvent.TIMEOUT, f"{player_a} timed out - {player_b} wins"
        )
        return (False, Winner.PLAYER_B)
    if not choice_b:
        referee.logger.log_error(
            LogEvent.TIMEOUT, f"{player_b} timed out - {player_a} wins"
        )
        return (False, Winner.PLAYER_A)
    return (True, None)
