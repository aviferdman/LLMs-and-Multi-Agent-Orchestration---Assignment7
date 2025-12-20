"""Referee communication helpers - message sending functions."""

from SHARED.constants import Field, Timeout
from SHARED.contracts import build_game_over, build_match_result_report
from SHARED.league_sdk.agent_comm import send, send_with_retry
from SHARED.league_sdk.config_loader import load_agent_config, load_system_config

_system_config = load_system_config()
_agents_config = load_agent_config()
_lm_endpoint = _agents_config["league_manager"]["endpoint"]


async def notify_game_over(
    referee, league_id, round_id, match_id, winner, drawn_number, context, ep_a, ep_b
):
    """Send game over notifications to players."""
    msg = build_game_over(
        league_id,
        round_id,
        match_id,
        referee.referee_id,
        winner,
        drawn_number,
        context.player_a_choice,
        context.player_b_choice,
    )
    await send(ep_a, msg)
    await send(ep_b, msg)


async def report_result(referee, league_id, round_id, match_id, player_a, player_b, winner):
    """Report match result to League Manager with retry."""
    msg = build_match_result_report(
        league_id, round_id, match_id, referee.referee_id, player_a, player_b, winner
    )
    await send_with_retry(
        _lm_endpoint,
        msg,
        max_retries=_system_config.retry_policy["max_retries"],
        timeout=_system_config.timeouts[Timeout.HTTP_REQUEST],
        retry_delay=_system_config.retry_policy["retry_delay"],
    )
