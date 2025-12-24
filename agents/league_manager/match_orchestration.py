"""Match orchestration logic for League Manager - Facade module.

This module provides the main entry point for league match execution.
Implementation is split into smaller modules for maintainability.
"""

import asyncio
from typing import Any, Dict, List

from agents.league_manager.broadcast import broadcast_to_agents
from agents.league_manager.league_completion import send_league_completed
from agents.league_manager.round_execution import execute_round, send_round_completed
from agents.league_manager.scheduler import get_match_schedule

from SHARED.constants import Field, GameStatus


async def run_league_matches(
    league_config,
    registered_players: Dict[str, Any],
    registered_referees: Dict[str, Any],
    logger,
    state: Dict[str, Any],
):
    """Execute all league matches by delegating to referees."""
    try:
        logger.log_message(
            "LEAGUE_ORCHESTRATION_START",
            {
                Field.LEAGUE_ID: league_config.league_id,
                "registered_players": list(registered_players.keys()),
                "registered_referees": list(registered_referees.keys()),
            },
        )
        state["league_status"] = GameStatus.ACTIVE
        schedule = get_match_schedule()
        total_rounds = len(schedule)
        logger.log_message(
            "SCHEDULE_LOADED",
            {
                "total_rounds": total_rounds,
                "total_matches": sum(len(r) for r in schedule),
            },
        )
        round_results: List[Dict[str, Any]] = []
        for round_num, round_matches in enumerate(schedule, start=1):
            state["current_round"] = round_num
            current_round_results = await execute_round(
                round_num,
                total_rounds,
                round_matches,
                league_config,
                registered_players,
                registered_referees,
                logger,
                state,
            )
            round_results.extend(current_round_results)
            await asyncio.sleep(2)
        state["league_status"] = GameStatus.COMPLETED
        await send_league_completed(
            league_config, registered_players, registered_referees, logger, state
        )
    except Exception as e:
        logger.log_error("LEAGUE_ORCHESTRATION_ERROR", f"Exception: {e}")
        state["league_status"] = GameStatus.ERROR


# Re-export for backward compatibility
_execute_round = execute_round
_send_round_completed = send_round_completed
_send_league_completed = send_league_completed
