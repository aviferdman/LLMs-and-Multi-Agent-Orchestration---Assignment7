"""Generic referee agent - supports all game types."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import argparse

from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.http_client import send_message
from SHARED.contracts import build_referee_register_request
from SHARED.constants import (
    MessageType, Field, Status, LogEvent, Endpoint, MCP_PATH, SERVER_HOST, LOCALHOST, HTTP_PROTOCOL
)
from agents.referee_game_logic import EvenOddGameRules
from agents.referee_http_handlers import handle_run_match, handle_game_join_ack, handle_parity_choice
from agents.referee_match_runner import run_match_phases


class GenericReferee:
    """Generic referee that can manage any game type."""
    
    def __init__(self, referee_id: str, port: int):
        """Initialize referee."""
        self.referee_id = referee_id
        self.port = port
        self.endpoint = f"{HTTP_PROTOCOL}://{LOCALHOST}:{port}{MCP_PATH}"
        self.logger = LeagueLogger(referee_id)
        self.game_rules = EvenOddGameRules()
        self.active_matches = {}
        self.auth_token = None
        self.app = FastAPI(title=f"Referee {referee_id}")
        self.setup_routes()
    
    def setup_routes(self):
        """Setup FastAPI routes."""
        @self.app.post(MCP_PATH)
        async def mcp_endpoint(request: Request, background_tasks: BackgroundTasks) -> JSONResponse:
            """Handle MCP messages."""
            try:
                message = await request.json()
                self.logger.log_message(LogEvent.RECEIVED, message)
                msg_type = message.get(Field.MESSAGE_TYPE)
                
                if msg_type == MessageType.RUN_MATCH:
                    response = handle_run_match(message, self, background_tasks)
                elif msg_type == MessageType.GAME_JOIN_ACK:
                    response = handle_game_join_ack(message, self)
                elif msg_type == MessageType.PARITY_CHOICE:
                    response = handle_parity_choice(message, self)
                else:
                    response = {Field.STATUS: Status.ERROR, "message": "Unknown message type"}
                
                self.logger.log_message(LogEvent.SENT, response)
                return JSONResponse(content=response)
            except Exception as e:
                self.logger.log_error(LogEvent.REQUEST_ERROR, str(e))
                return JSONResponse(content={Field.STATUS: Status.ERROR, "message": str(e)}, status_code=500)
        
        @self.app.on_event("startup")
        async def startup():
            """Register with League Manager on startup."""
            self.logger.log_message(LogEvent.STARTUP, {Field.REFEREE_ID: self.referee_id, "port": self.port})
            asyncio.create_task(self.register_with_league_manager())
    
    async def register_with_league_manager(self):
        """Register this referee with the League Manager."""
        await asyncio.sleep(2)
        register_msg = build_referee_register_request(self.referee_id, self.endpoint)
        self.logger.log_message("REGISTERING", {"endpoint": Endpoint.LEAGUE_MANAGER})
        response = await send_message(Endpoint.LEAGUE_MANAGER, register_msg)
        if response and response.get(Field.STATUS) == Status.REGISTERED:
            self.auth_token = response.get(Field.AUTH_TOKEN)
            self.logger.log_message(LogEvent.REFEREE_REGISTERED, {Field.REFEREE_ID: self.referee_id})
        else:
            self.logger.log_error(LogEvent.ERROR, f"Registration failed: {response}")
    
    async def run_match(self, league_id, round_id, match_id, player_a, player_b, ep_a, ep_b):
        """Run a match - delegates to match runner."""
        await run_match_phases(self, league_id, round_id, match_id, player_a, player_b, ep_a, ep_b)
    
    def run(self):
        """Run the referee server."""
        uvicorn.run(self.app, host=SERVER_HOST, port=self.port)


def create_app(referee_id: str, port: int) -> FastAPI:
    """Factory function to create referee FastAPI app."""
    return GenericReferee(referee_id, port).app


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--referee-id", required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    GenericReferee(args.referee_id, args.port).run()


if __name__ == "__main__":
    main()
