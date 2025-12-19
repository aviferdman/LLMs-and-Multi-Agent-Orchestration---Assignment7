"""Match orchestration logic for League Manager."""

import asyncio
from typing import Dict, Any

from SHARED.league_sdk.http_client import send_with_retry
from SHARED.league_sdk.repositories import StandingsRepository, MatchRepository
from SHARED.constants import Field, LogEvent, Timeout, GameStatus
from SHARED.contracts import build_run_match
from scheduler import get_match_schedule


async def run_league_matches(
    league_config,
    registered_players: Dict[str, Any],
    registered_referees: Dict[str, Any],
    logger,
    state: Dict[str, Any]
):
    """Execute all league matches by delegating to referees."""
    logger.log_message("LEAGUE_ORCHESTRATION_START", {
        Field.LEAGUE_ID: league_config.league_id,
        "registered_players": list(registered_players.keys()),
        "registered_referees": list(registered_referees.keys())
    })
    
    state["league_status"] = GameStatus.ACTIVE
    schedule = get_match_schedule()
    
    logger.log_message("SCHEDULE_LOADED", {
        "total_rounds": len(schedule),
        "total_matches": sum(len(r) for r in schedule)
    })
    
    for round_num, round_matches in enumerate(schedule, start=1):
        state["current_round"] = round_num
        logger.log_message("ROUND_START", {"round": round_num})
        
        for match in round_matches:
            await execute_match_via_referee(
                match, league_config, registered_players,
                registered_referees, logger, state
            )
            await asyncio.sleep(1)
        
        logger.log_message("ROUND_COMPLETE", {"round": round_num})
        await asyncio.sleep(2)
    
    state["league_status"] = GameStatus.COMPLETED
    
    standings_repo = StandingsRepository(league_config.league_id)
    final_standings = standings_repo.load()
    logger.log_message("LEAGUE_COMPLETE", {"standings": final_standings})


async def execute_match_via_referee(
    match: Dict[str, Any],
    league_config,
    registered_players: Dict[str, Any],
    registered_referees: Dict[str, Any],
    logger,
    state: Dict[str, Any]
):
    """Send RUN_MATCH to referee to execute a match."""
    referee_id = match["referee_id"]
    referee_info = registered_referees.get(referee_id)
    
    if not referee_info:
        logger.log_error(LogEvent.ERROR, f"Referee {referee_id} not registered")
        return
    
    player_a = match["player_a"]
    player_b = match["player_b"]
    player_a_info = registered_players.get(player_a)
    player_b_info = registered_players.get(player_b)
    
    if not player_a_info or not player_b_info:
        logger.log_error(LogEvent.ERROR, "Players not registered")
        return
    
    run_match_msg = build_run_match(
        league_id=league_config.league_id,
        round_id=match["round_id"],
        match_id=match["match_id"],
        referee_id=referee_id,
        player_a=player_a,
        player_a_endpoint=player_a_info[Field.ENDPOINT],
        player_b=player_b,
        player_b_endpoint=player_b_info[Field.ENDPOINT]
    )
    
    logger.log_message("MATCH_ASSIGNED", {
        Field.MATCH_ID: match["match_id"],
        Field.REFEREE_ID: referee_id
    })
    
    response = await send_with_retry(
        referee_info[Field.ENDPOINT],
        run_match_msg,
        max_retries=3,
        timeout=Timeout.HTTP_REQUEST
    )
    
    if response:
        state["matches_completed"] += 1
