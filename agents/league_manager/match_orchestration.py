"""Match orchestration logic for League Manager."""

import asyncio
from typing import Dict, Any, List

from SHARED.league_sdk.repositories import StandingsRepository
from SHARED.constants import Field, GameStatus
from SHARED.contracts import (
    build_round_announcement,
    build_round_completed,
    build_league_completed,
    build_league_standings_update
)
from scheduler import get_match_schedule
from broadcast import broadcast_to_agents
from match_execution import execute_match_via_referee


async def run_league_matches(
    league_config,
    registered_players: Dict[str, Any],
    registered_referees: Dict[str, Any],
    logger,
    state: Dict[str, Any]
):
    """Execute all league matches by delegating to referees."""
    try:
        logger.log_message("LEAGUE_ORCHESTRATION_START", {
            Field.LEAGUE_ID: league_config.league_id,
            "registered_players": list(registered_players.keys()),
            "registered_referees": list(registered_referees.keys())
        })
        
        state["league_status"] = GameStatus.ACTIVE
        schedule = get_match_schedule()
        total_rounds = len(schedule)
        
        logger.log_message("SCHEDULE_LOADED", {
            "total_rounds": total_rounds,
            "total_matches": sum(len(r) for r in schedule)
        })
        
        round_results: List[Dict[str, Any]] = []
        
        for round_num, round_matches in enumerate(schedule, start=1):
            state["current_round"] = round_num
            current_round_results = await _execute_round(
                round_num, total_rounds, round_matches, league_config,
                registered_players, registered_referees, logger, state
            )
            round_results.extend(current_round_results)
            await asyncio.sleep(2)
        
        state["league_status"] = GameStatus.COMPLETED
        await _send_league_completed(league_config, registered_players, registered_referees, logger, state)
    except Exception as e:
        logger.log_error("LEAGUE_ORCHESTRATION_ERROR", f"Exception: {e}")
        state["league_status"] = GameStatus.ERROR


async def _execute_round(
    round_num: int, total_rounds: int, round_matches: list,
    league_config, registered_players, registered_referees, logger, state
) -> List[Dict[str, Any]]:
    """Execute a single round of matches."""
    # Send ROUND_ANNOUNCEMENT
    announcement = build_round_announcement(
        league_config.league_id, round_num, total_rounds,
        [{"match_id": m["match_id"], "player_a": m["player_a"], "player_b": m["player_b"]} 
         for m in round_matches]
    )
    await broadcast_to_agents(announcement, registered_players, registered_referees, logger)
    logger.log_message("ROUND_ANNOUNCEMENT_SENT", {"round": round_num})
    
    current_round_results = []
    for match in round_matches:
        result = await execute_match_via_referee(
            match, league_config, registered_players, registered_referees, logger, state
        )
        if result:
            current_round_results.append(result)
        await asyncio.sleep(1)
    
    # Send ROUND_COMPLETED and STANDINGS_UPDATE
    await _send_round_completed(round_num, current_round_results, league_config,
                                 registered_players, registered_referees, logger)
    return current_round_results


async def _send_round_completed(
    round_num: int, results: list, league_config,
    registered_players, registered_referees, logger
):
    """Send ROUND_COMPLETED and STANDINGS_UPDATE messages."""
    try:
        completed_msg = build_round_completed(league_config.league_id, round_num, results)
        await broadcast_to_agents(completed_msg, registered_players, registered_referees, logger)
        logger.log_message("ROUND_COMPLETED_SENT", {"round": round_num})
        
        standings_repo = StandingsRepository(league_config.league_id)
        standings_data = standings_repo.load()
        standings_list = standings_data.get("standings", [])
        standings_list.sort(key=lambda x: (-x.get("points", 0), -x.get("wins", 0)))
        
        standings_update = build_league_standings_update(league_config.league_id, round_num, standings_list)
        await broadcast_to_agents(standings_update, registered_players, registered_referees, logger)
        logger.log_message("STANDINGS_UPDATE_SENT", {"round": round_num})
    except Exception as e:
        logger.log_error("SEND_ROUND_COMPLETED_ERROR", f"{type(e).__name__}: {e}")


async def _send_league_completed(league_config, registered_players, registered_referees, logger, state):
    """Send LEAGUE_COMPLETED message."""
    standings_repo = StandingsRepository(league_config.league_id)
    standings_data = standings_repo.load()
    final_list = standings_data.get("standings", [])
    final_list.sort(key=lambda x: (-x.get("points", 0), -x.get("wins", 0)))
    
    msg = build_league_completed(league_config.league_id, final_list, state["matches_completed"])
    await broadcast_to_agents(msg, registered_players, registered_referees, logger)
    logger.log_message("LEAGUE_COMPLETED_SENT", {"standings": final_list})
