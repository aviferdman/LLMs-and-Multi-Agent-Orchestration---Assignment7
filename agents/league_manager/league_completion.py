"""League completion logic for League Manager."""

import asyncio
import os
from typing import Any, Dict

from agents.league_manager.broadcast import broadcast_to_agents

from SHARED.constants import Field
from SHARED.contracts import build_league_completed
from SHARED.league_sdk.repositories import StandingsRepository


async def send_league_completed(
    league_config, registered_players, registered_referees, logger, state
):
    """Send LEAGUE_COMPLETED message and initiate graceful shutdown."""
    standings_repo = StandingsRepository(league_config.league_id)
    standings_data = standings_repo.load()
    final_list = standings_data.get("standings", [])
    final_list.sort(key=lambda x: (-x.get("points", 0), -x.get("wins", 0)))
    # Build champion object
    champion = None
    if final_list:
        top = final_list[0]
        champion = {
            "player_id": top.get(Field.PLAYER_ID),
            "total_wins": top.get("wins", 0),
            "total_points": top.get("points", 0),
        }
    msg = build_league_completed(
        league_id=league_config.league_id,
        final_standings=final_list,
        total_matches=state["matches_completed"],
        champion=champion,
        total_rounds=state.get("current_round", 1),
    )
    await broadcast_to_agents(msg, registered_players, registered_referees, logger)
    logger.log_message("LEAGUE_COMPLETED_SENT", {"standings": final_list})
    await asyncio.sleep(3)
    logger.log_message("SHUTDOWN_INITIATED", {"league_id": league_config.league_id})
    os._exit(0)
