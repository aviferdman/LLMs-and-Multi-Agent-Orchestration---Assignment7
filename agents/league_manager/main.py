"""League Manager - Main HTTP server."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any

from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.config_loader import load_system_config, load_league_config, load_agent_config
from SHARED.league_sdk.repositories import StandingsRepository
from SHARED.constants import (
    MessageType, Field, AgentID, LogEvent, LeagueID, MCP_PATH, Status, GameStatus
)
from SHARED.contracts import build_league_status
from handlers import handle_referee_register, handle_league_register, handle_match_result_report
from match_orchestration import run_league_matches

app = FastAPI(title="League Manager")
logger = LeagueLogger(AgentID.LEAGUE_MANAGER)
system_config = load_system_config()
league_config = load_league_config(LeagueID.EVEN_ODD_2025)
agents_config = load_agent_config()

# Store registered agents
registered_referees: Dict[str, Any] = {}
registered_players: Dict[str, Any] = {}

# League state
league_state = {
    "league_status": GameStatus.WAITING_FOR_PLAYERS,
    "current_round": 0,
    "matches_completed": 0
}


@app.post(MCP_PATH)
async def mcp_endpoint(request: Request, background_tasks: BackgroundTasks) -> JSONResponse:
    """Handle all MCP protocol messages."""
    try:
        message = await request.json()
        logger.log_message(LogEvent.RECEIVED, message)
        msg_type = message.get(Field.MESSAGE_TYPE)
        
        if msg_type == MessageType.REFEREE_REGISTER_REQUEST:
            response = handle_referee_register(message, registered_referees, logger)
        elif msg_type == MessageType.LEAGUE_REGISTER_REQUEST:
            response = handle_league_register(message, registered_players, league_config, logger)
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
            
            background_tasks.add_task(
                run_league_matches, league_config, registered_players,
                registered_referees, logger, league_state
            )
            response = build_league_status(
                league_config.league_id, Status.SUCCESS,
                league_state["current_round"], league_config.total_rounds, league_state["matches_completed"]
            )
        elif msg_type == MessageType.LEAGUE_STATUS:
            response = build_league_status(
                league_config.league_id, league_state["league_status"],
                league_state["current_round"], league_config.total_rounds, league_state["matches_completed"]
            )
        elif msg_type == MessageType.MATCH_RESULT_REPORT:
            response = handle_match_result_report(message, league_config, logger)
        else:
            response = {Field.STATUS: Status.ERROR, "message": "Unknown message type"}
        
        logger.log_message(LogEvent.SENT, response)
        return JSONResponse(content=response)
    except Exception as e:
        logger.log_error(LogEvent.REQUEST_ERROR, str(e))
        return JSONResponse(content={Field.STATUS: Status.ERROR, "message": str(e)}, status_code=500)


@app.on_event("startup")
async def startup():
    """Initialize on startup."""
    lm_config = agents_config["league_manager"]
    logger.log_message(LogEvent.STARTUP, {Field.LEAGUE_ID: league_config.league_id, "port": lm_config["port"]})


if __name__ == "__main__":
    from SHARED.constants import SERVER_HOST
    lm_config = agents_config["league_manager"]
    uvicorn.run(app, host=SERVER_HOST, port=lm_config["port"])
