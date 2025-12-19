"""League Manager - Main HTTP server."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any

from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.config_loader import load_system_config, load_league_config
from SHARED.constants import (
    MessageType,
    Field,
    AgentID,
    Port,
    LogEvent,
    LeagueID,
    MCP_PATH,
    Status
)
from handlers import (
    handle_referee_register,
    handle_league_register,
    handle_match_result_report
)

app = FastAPI(title="League Manager")
logger = LeagueLogger(AgentID.LEAGUE_MANAGER)
system_config = load_system_config()
league_config = load_league_config(LeagueID.EVEN_ODD_2025)

# Store registered agents
registered_referees = {}
registered_players = {}

@app.post(MCP_PATH)
async def mcp_endpoint(request: Request) -> JSONResponse:
    """Handle all MCP protocol messages."""
    try:
        message = await request.json()
        logger.log_message(LogEvent.RECEIVED, message)
        
        message_type = message.get(Field.MESSAGE_TYPE)
        
        if message_type == MessageType.REFEREE_REGISTER_REQUEST:
            response = handle_referee_register(
                message, registered_referees, logger
            )
        elif message_type == MessageType.LEAGUE_REGISTER_REQUEST:
            response = handle_league_register(
                message, registered_players, league_config, logger
            )
        elif message_type == MessageType.MATCH_RESULT_REPORT:
            response = handle_match_result_report(
                message, league_config, logger
            )
        else:
            response = {Status.ERROR: "Unknown message type"}
        
        logger.log_message(LogEvent.SENT, response)
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.log_error(LogEvent.REQUEST_ERROR, str(e))
        return JSONResponse(
            content={Status.ERROR: "Internal error"},
            status_code=500
        )

@app.on_event("startup")
async def startup():
    """Initialize on startup."""
    logger.log_message(LogEvent.STARTUP, {
        Field.LEAGUE_ID: league_config.league_id,
        "port": Port.LEAGUE_MANAGER
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=Port.LEAGUE_MANAGER)
