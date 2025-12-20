"""Match execution via referee for League Manager."""

from typing import Dict, Any

from SHARED.league_sdk.agent_comm import send_with_retry
from SHARED.league_sdk.config_loader import load_system_config
from SHARED.constants import Field, LogEvent, Timeout
from SHARED.contracts import build_run_match

# Load system config once at module level for timeout values
_system_config = load_system_config()


async def execute_match_via_referee(
    match: Dict[str, Any],
    league_config,
    registered_players: Dict[str, Any],
    registered_referees: Dict[str, Any],
    logger,
    state: Dict[str, Any]
) -> Dict[str, Any]:
    """Send RUN_MATCH to referee to execute a match.
    
    Returns:
        Match result dict or None on failure
    """
    referee_id = match["referee_id"]
    referee_info = registered_referees.get(referee_id)
    
    if not referee_info:
        logger.log_error(LogEvent.ERROR, f"Referee {referee_id} not registered")
        return None
    
    player_a = match["player_a"]
    player_b = match["player_b"]
    player_a_info = registered_players.get(player_a)
    player_b_info = registered_players.get(player_b)
    
    if not player_a_info or not player_b_info:
        logger.log_error(LogEvent.ERROR, "Players not registered")
        return None
    
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
        max_retries=_system_config.retry_policy["max_retries"],
        timeout=_system_config.timeouts[Timeout.HTTP_REQUEST],
        retry_delay=_system_config.retry_policy["retry_delay"]
    )
    
    if response:
        state["matches_completed"] += 1
        return {
            "match_id": match["match_id"],
            "player_a": player_a,
            "player_b": player_b,
            "referee_id": referee_id
        }
    
    return None
