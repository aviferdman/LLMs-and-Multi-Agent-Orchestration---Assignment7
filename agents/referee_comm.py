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
    from SHARED.constants import Winner
    
    try:
        # Map PLAYER_A/PLAYER_B/draw to actual player ID
        if winner == Winner.PLAYER_A:
            actual_winner = context.player_a
        elif winner == Winner.PLAYER_B:
            actual_winner = context.player_b
        else:
            actual_winner = None  # draw case
        
        # Determine status and reason
        if not context.player_a_choice or not context.player_b_choice:
            status = "TECHNICAL_LOSS"
            reason = "timeout"
        elif winner == Winner.DRAW:
            status = "DRAW"
            reason = "Both players chose the same parity"
        else:
            status = "WIN"
            reason = "normal"
        
        # Determine number parity
        number_parity = "odd" if drawn_number and drawn_number % 2 == 1 else "even"
        
        msg = build_game_over(
            league_id=league_id,
            round_id=round_id,
            match_id=match_id,
            referee_id=referee.referee_id,
            status=status,
            winner_player_id=actual_winner,
            drawn_number=drawn_number or 0,
            number_parity=number_parity,
            choices={
                context.player_a: context.player_a_choice or "NO_RESPONSE",
                context.player_b: context.player_b_choice or "NO_RESPONSE",
            },
            reason=reason,
        )
        referee.logger.log_message("SENDING_GAME_OVER", {"to_player_a": ep_a, "to_player_b": ep_b})
        await send(ep_a, msg)
        await send(ep_b, msg)
        referee.logger.log_message("GAME_OVER_SENT", {"match_id": match_id})
    except Exception as e:
        referee.logger.log_error("GAME_OVER_ERROR", f"Failed to send GAME_OVER: {e}", {"error": str(e)})


async def report_result(referee, league_id, round_id, match_id, player_a, player_b, winner):
    """Report match result to League Manager with retry."""
    from SHARED.constants import Winner
    
    try:
        # Map PLAYER_A/PLAYER_B/draw to actual player ID
        if winner == Winner.PLAYER_A:
            actual_winner = player_a
        elif winner == Winner.PLAYER_B:
            actual_winner = player_b
        else:
            actual_winner = None  # draw case
        
        msg = build_match_result_report(
            league_id=league_id,
            round_id=round_id,
            match_id=match_id,
            referee_id=referee.referee_id,
            winner=actual_winner,
            score={player_a: 1 if actual_winner == player_a else 0, player_b: 1 if actual_winner == player_b else 0},
            drawn_number=0,  # Will be updated when we have context
            choices={},  # Will be updated when we have context
        )
        referee.logger.log_message("SENDING_MATCH_RESULT_REPORT", {"to_lm": _lm_endpoint, "match_id": match_id})
        await send_with_retry(
            _lm_endpoint,
            msg,
            max_retries=_system_config.retry_policy["max_retries"],
            timeout=_system_config.timeouts[Timeout.HTTP_REQUEST],
            retry_delay=_system_config.retry_policy["retry_delay"],
        )
        referee.logger.log_message("MATCH_RESULT_REPORT_SENT", {"match_id": match_id})
    except Exception as e:
        referee.logger.log_error("MATCH_RESULT_REPORT_ERROR", f"Failed to send result: {e}", {"error": str(e)})
