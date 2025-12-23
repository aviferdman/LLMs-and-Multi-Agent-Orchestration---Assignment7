"""League Manager message handlers."""

import asyncio
from typing import Any, Dict

from agents.league_manager.ranking import update_standings
from agents.league_manager.round_tracker import get_round_tracker

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
    # Extract referee_id from sender field (format: "referee:REF01")
    sender = message.get(Field.SENDER, "")
    referee_id = sender.split(":")[-1] if ":" in sender else sender
    # Extract endpoint from referee_meta
    referee_meta = message.get(Field.REFEREE_META, {})
    endpoint = referee_meta.get(Field.CONTACT_ENDPOINT)
    session_mgr = get_session_manager()

    if session_mgr.is_registered(referee_id):
        logger.log_error(LogEvent.DUPLICATE_REGISTRATION, f"Referee {referee_id}")
        return {Status.ERROR: "Already registered"}

    # Create session - SessionManager generates auth token
    session = session_mgr.create_session(referee_id, AgentType.REFEREE, endpoint)

    logger.log_message(LogEvent.REFEREE_REGISTERED, {Field.REFEREE_ID: referee_id})

    # Per CONTRACTS.md §2.1: status should be "ACCEPTED", reason is optional
    return build_referee_register_response(referee_id, Status.ACCEPTED)


def handle_league_register(
    message: Dict[str, Any], league_config: LeagueConfig, logger: LeagueLogger
) -> Dict[str, Any]:
    """Handle player registration request - delegates to SessionManager."""
    # Extract player_id from sender field (format: "player:P01")
    sender = message.get(Field.SENDER, "")
    player_id = sender.split(":")[-1] if ":" in sender else sender
    # Extract endpoint from player_meta
    player_meta = message.get(Field.PLAYER_META, {})
    endpoint = player_meta.get(Field.CONTACT_ENDPOINT)
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

    # Per CONTRACTS.md §3.1: status should be "ACCEPTED", reason is optional
    return build_league_register_response(player_id, Status.ACCEPTED)


def handle_match_result_report(
    message: Dict[str, Any], league_config: LeagueConfig, logger: LeagueLogger
) -> Dict[str, Any]:
    """Handle match result report from referee."""
    match_id = message.get(Field.MATCH_ID)
    round_id = message.get(Field.ROUND_ID)
    # Protocol v2: result is a nested object
    result = message.get(Field.RESULT, {})
    winner = result.get("winner")

    # Extract player IDs from the result's score keys or from sender context
    score = result.get("score", {})
    player_ids = list(score.keys())
    player_a = player_ids[0] if len(player_ids) > 0 else None
    player_b = player_ids[1] if len(player_ids) > 1 else None

    logger.log_message(
        LogEvent.MATCH_RESULT,
        {Field.MATCH_ID: match_id, Field.ROUND_ID: round_id, Field.WINNER: winner},
    )

    # Save match data
    match_repo = MatchRepository(league_config.league_id)
    match_data = {
        Field.MATCH_ID: match_id,
        Field.PLAYER_A_ID: player_a,
        Field.PLAYER_B_ID: player_b,
        Field.WINNER: winner,
        Field.ROUND_ID: round_id,
        "timestamp": message.get("timestamp"),
    }
    match_repo.save_match(match_id, match_data)

    # Save match to player histories
    for player_id in [player_a, player_b]:
        if player_id:
            history_repo = PlayerHistoryRepository(player_id)
            history_repo.append_match(match_data)

    # Update standings
    if player_a and player_b:
        update_standings(player_a, player_b, winner, league_config)

    # Record result in round tracker (for round completion detection)
    tracker = get_round_tracker()
    asyncio.create_task(
        tracker.record_result(
            round_id,
            match_id,
            {"match_id": match_id, "winner": winner, "player_a": player_a, "player_b": player_b},
        )
    )

    return build_match_result_ack(match_id)
