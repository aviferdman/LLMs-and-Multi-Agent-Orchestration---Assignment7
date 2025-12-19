"""League Manager message handlers."""

import uuid
from typing import Dict, Any
from datetime import datetime

from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.config_models import LeagueConfig
from SHARED.league_sdk.repositories import StandingsRepository
from SHARED.contracts import (
    build_referee_register_response,
    build_league_register_response,
    build_match_result_ack
)
from SHARED.constants import Field, LogEvent, Status
from ranking import update_standings

def handle_referee_register(
    message: Dict[str, Any],
    registered_referees: Dict[str, Any],
    logger: LeagueLogger
) -> Dict[str, Any]:
    """Handle referee registration request."""
    referee_id = message.get(Field.REFEREE_ID)
    
    if referee_id in registered_referees:
        logger.log_error(LogEvent.DUPLICATE_REGISTRATION, f"Referee {referee_id}")
        return {Status.ERROR: "Already registered"}
    
    auth_token = str(uuid.uuid4())
    registered_referees[referee_id] = {
        Field.REFEREE_ID: referee_id,
        Field.AUTH_TOKEN: auth_token,
        Field.ENDPOINT: message.get(Field.ENDPOINT),
        "registered_at": datetime.utcnow().isoformat() + "Z"
    }
    
    logger.log_message(LogEvent.REFEREE_REGISTERED, {Field.REFEREE_ID: referee_id})
    
    return build_referee_register_response(referee_id, auth_token)

def handle_league_register(
    message: Dict[str, Any],
    registered_players: Dict[str, Any],
    league_config: LeagueConfig,
    logger: LeagueLogger
) -> Dict[str, Any]:
    """Handle player registration request."""
    player_id = message.get(Field.PLAYER_ID)
    
    if player_id in registered_players:
        logger.log_error(LogEvent.DUPLICATE_REGISTRATION, f"Player {player_id}")
        return {Status.ERROR: "Already registered"}
    
    auth_token = str(uuid.uuid4())
    registered_players[player_id] = {
        Field.PLAYER_ID: player_id,
        Field.AUTH_TOKEN: auth_token,
        Field.ENDPOINT: message.get(Field.ENDPOINT),
        "registered_at": datetime.utcnow().isoformat() + "Z"
    }
    
    logger.log_message(LogEvent.PLAYER_REGISTERED, {Field.PLAYER_ID: player_id})
    
    # Initialize player in standings
    standings_repo = StandingsRepository(league_config.league_id)
    standings = standings_repo.load()
    
    if not any(p[Field.PLAYER_ID] == player_id for p in standings["standings"]):
        standings["standings"].append({
            Field.PLAYER_ID: player_id,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "points": 0,
            "games_played": 0,
            "rank": 0
        })
        standings_repo.save(standings)
    
    return build_league_register_response(
        player_id,
        league_config.league_id,
        auth_token
    )

def handle_match_result_report(
    message: Dict[str, Any],
    league_config: LeagueConfig,
    logger: LeagueLogger
) -> Dict[str, Any]:
    """Handle match result report from referee."""
    match_id = message.get(Field.MATCH_ID)
    player_a = message.get(Field.PLAYER_A)
    player_b = message.get(Field.PLAYER_B)
    winner = message.get(Field.WINNER)
    
    logger.log_message(LogEvent.MATCH_RESULT, {
        Field.MATCH_ID: match_id,
        Field.WINNER: winner
    })
    
    # Update standings
    update_standings(player_a, player_b, winner, league_config)
    
    return build_match_result_ack(match_id)
