"""League Manager message handlers."""

from typing import Any, Dict

from ranking import update_standings

from SHARED.constants import Field, LogEvent, Status
from SHARED.contracts import (
    build_league_register_response,
    build_match_result_ack,
    build_referee_register_response,
)
from SHARED.league_sdk.config_models import LeagueConfig
from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.repositories import (
    MatchRepository,
    PlayerHistoryRepository,
    StandingsRepository,
)
from SHARED.league_sdk.session_manager import AgentType, get_session_manager


def handle_referee_register(message: Dict[str, Any], logger: LeagueLogger) -> Dict[str, Any]:
    """Handle referee registration request - delegates to SessionManager."""
    referee_id = message.get(Field.REFEREE_ID)
    endpoint = message.get(Field.ENDPOINT)
    session_mgr = get_session_manager()

    if session_mgr.is_registered(referee_id):
        logger.log_error(LogEvent.DUPLICATE_REGISTRATION, f"Referee {referee_id}")
        return {Status.ERROR: "Already registered"}

    # Create session - SessionManager generates auth token
    session = session_mgr.create_session(referee_id, AgentType.REFEREE, endpoint)

    logger.log_message(LogEvent.REFEREE_REGISTERED, {Field.REFEREE_ID: referee_id})

    return build_referee_register_response(referee_id, session.auth_token)


def handle_league_register(
    message: Dict[str, Any], league_config: LeagueConfig, logger: LeagueLogger
) -> Dict[str, Any]:
    """Handle player registration request - delegates to SessionManager."""
    player_id = message.get(Field.PLAYER_ID)
    endpoint = message.get(Field.ENDPOINT)
    session_mgr = get_session_manager()

    # Always ensure player is in standings
    standings_repo = StandingsRepository(league_config.league_id)
    standings = standings_repo.load()

    if not any(p[Field.PLAYER_ID] == player_id for p in standings["standings"]):
        standings["standings"].append(
            {
                Field.PLAYER_ID: player_id,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "points": 0,
                "games_played": 0,
                "rank": 0,
            }
        )
        standings_repo.save(standings)

    if session_mgr.is_registered(player_id):
        logger.log_error(LogEvent.DUPLICATE_REGISTRATION, f"Player {player_id}")
        return {Status.ERROR: "Already registered"}

    # Create session - SessionManager generates auth token
    session = session_mgr.create_session(player_id, AgentType.PLAYER, endpoint)

    logger.log_message(LogEvent.PLAYER_REGISTERED, {Field.PLAYER_ID: player_id})

    return build_league_register_response(player_id, league_config.league_id, session.auth_token)


def handle_match_result_report(
    message: Dict[str, Any], league_config: LeagueConfig, logger: LeagueLogger
) -> Dict[str, Any]:
    """Handle match result report from referee."""
    match_id = message.get(Field.MATCH_ID)
    player_a = message.get(Field.PLAYER_A)
    player_b = message.get(Field.PLAYER_B)
    winner = message.get(Field.WINNER)

    logger.log_message(LogEvent.MATCH_RESULT, {Field.MATCH_ID: match_id, Field.WINNER: winner})

    # Save match data
    match_repo = MatchRepository(league_config.league_id)
    match_data = {
        Field.MATCH_ID: match_id,
        Field.PLAYER_A: player_a,
        Field.PLAYER_B: player_b,
        Field.WINNER: winner,
        "round_id": message.get("round_id"),
        "timestamp": message.get("timestamp"),
    }
    match_repo.save_match(match_id, match_data)

    # Save match to player histories
    for player_id in [player_a, player_b]:
        history_repo = PlayerHistoryRepository(player_id)
        history_repo.append_match(match_data)

    # Update standings
    update_standings(player_a, player_b, winner, league_config)

    return build_match_result_ack(match_id)
