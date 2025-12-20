"""League Manager - Main HTTP server."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict

import uvicorn
from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse
from handlers import handle_league_register, handle_match_result_report, handle_referee_register
from match_orchestration import run_league_matches

from SHARED.constants import MCP_PATH, AgentID, Field, GameStatus, LogEvent, MessageType, Status
from SHARED.contracts import build_league_status
from SHARED.league_sdk.config_loader import (
    load_agent_config,
    load_league_config,
    load_system_config,
)
from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.repositories import StandingsRepository
from SHARED.league_sdk.session_manager import AgentType, get_session_manager

app = FastAPI(title="League Manager")
logger = LeagueLogger(AgentID.LEAGUE_MANAGER)
system_config = load_system_config()
# Load league ID from system config - game-agnostic approach
active_league_id = system_config.active_league_id
league_config = load_league_config(active_league_id)
agents_config = load_agent_config()

# Session manager handles all agent registrations
session_manager = get_session_manager()

# League state
league_state = {
    "league_status": GameStatus.WAITING_FOR_PLAYERS,
    "current_round": 0,
    "matches_completed": 0,
}


@app.post(MCP_PATH)
async def mcp_endpoint(request: Request, background_tasks: BackgroundTasks) -> JSONResponse:
    """Handle all MCP protocol messages."""
    try:
        message = await request.json()
        logger.log_message(LogEvent.RECEIVED, message)
        msg_type = message.get(Field.MESSAGE_TYPE)

        if msg_type == MessageType.REFEREE_REGISTER_REQUEST:
            response = handle_referee_register(message, logger)
        elif msg_type == MessageType.LEAGUE_REGISTER_REQUEST:
            response = handle_league_register(message, league_config, logger)
        elif msg_type == MessageType.START_LEAGUE:
            # Reset standings for fresh league start
            standings_repo = StandingsRepository(league_config.league_id)
            standings = standings_repo.load()
            for player in standings.get("standings", []):
                player["wins"] = 0
                player["losses"] = 0
                player["draws"] = 0
                player["points"] = 0
                player["games_played"] = 0
                player["rank"] = 0
            standings_repo.save(standings)
            league_state["matches_completed"] = 0
            league_state["current_round"] = 0

            # Get registered agents from session manager
            registered_players = session_manager.get_registered_agents_data(AgentType.PLAYER)
            registered_referees = session_manager.get_registered_agents_data(AgentType.REFEREE)

            background_tasks.add_task(
                run_league_matches,
                league_config,
                registered_players,
                registered_referees,
                logger,
                league_state,
            )
            response = build_league_status(
                league_config.league_id,
                Status.SUCCESS,
                league_state["current_round"],
                league_config.total_rounds,
                league_state["matches_completed"],
            )
        elif msg_type == MessageType.LEAGUE_STATUS:
            response = build_league_status(
                league_config.league_id,
                league_state["league_status"],
                league_state["current_round"],
                league_config.total_rounds,
                league_state["matches_completed"],
            )
        elif msg_type == MessageType.MATCH_RESULT_REPORT:
            response = handle_match_result_report(message, league_config, logger)
        else:
            response = {Field.STATUS: Status.ERROR, "message": "Unknown message type"}

        logger.log_message(LogEvent.SENT, response)
        return JSONResponse(content=response)
    except Exception as e:
        logger.log_error(LogEvent.REQUEST_ERROR, str(e))
        return JSONResponse(
            content={Field.STATUS: Status.ERROR, "message": str(e)}, status_code=500
        )


@app.on_event("startup")
async def startup():
    """Initialize on startup."""
    lm_config = agents_config["league_manager"]
    logger.log_message(
        LogEvent.STARTUP,
        {Field.LEAGUE_ID: league_config.league_id, "port": lm_config["port"]},
    )


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    logger.log_message(LogEvent.SHUTDOWN, {Field.LEAGUE_ID: league_config.league_id})
    session_manager.clear_all()


if __name__ == "__main__":
    from SHARED.constants import SERVER_HOST

    lm_config = agents_config["league_manager"]
    uvicorn.run(app, host=SERVER_HOST, port=lm_config["port"])
