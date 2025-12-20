"""Generic player agent - supports all strategies."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import argparse
import asyncio

from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.repositories import PlayerHistoryRepository
from SHARED.league_sdk.http_client import send_with_retry
from SHARED.league_sdk.config_loader import load_system_config, load_agent_config
from SHARED.contracts import build_game_join_ack, build_parity_choice, build_league_register_request
from SHARED.constants import (
    MessageType, Field, Status, LogEvent, StrategyType, SERVER_HOST, LOCALHOST, HTTP_PROTOCOL, MCP_PATH
)
from agents.player_strategies import STRATEGIES, RandomStrategy

# Load system config once at module level
_system_config = load_system_config()
_agents_config = load_agent_config()
_lm_endpoint = _agents_config["league_manager"]["endpoint"]


class GenericPlayer:
    """Generic player that can use any strategy."""
    
    def __init__(self, player_id: str, strategy_name: str, port: int):
        """Initialize player with strategy."""
        self.player_id = player_id
        self.port = port
        self.endpoint = f"{HTTP_PROTOCOL}://{LOCALHOST}:{port}{MCP_PATH}"
        self.logger = LeagueLogger(player_id)
        self.strategy = STRATEGIES.get(strategy_name, RandomStrategy)()
        self.auth_token = None
        self.app = FastAPI(title=f"Player {player_id}")
        self.setup_routes()
    
    def setup_routes(self):
        """Setup FastAPI routes."""
        @self.app.post("/mcp")
        async def mcp_endpoint(request: Request) -> JSONResponse:
            """Handle MCP protocol messages."""
            try:
                message = await request.json()
                self.logger.log_message(LogEvent.RECEIVED, message)
                msg_type = message.get(Field.MESSAGE_TYPE)
                
                if msg_type == MessageType.GAME_INVITATION:
                    response = self._handle_invitation(message)
                elif msg_type == MessageType.CHOOSE_PARITY_CALL:
                    response = self._handle_parity_call(message)
                elif msg_type == MessageType.GAME_OVER:
                    self._handle_game_over(message)
                    response = {Field.STATUS: Status.ACKNOWLEDGED}
                else:
                    response = {Field.STATUS: Status.ERROR, "message": "Unknown message type"}
                
                self.logger.log_message(LogEvent.SENT, response)
                return JSONResponse(content=response)
            except Exception as e:
                self.logger.log_error(LogEvent.REQUEST_ERROR, str(e))
                return JSONResponse(content={Field.STATUS: Status.ERROR}, status_code=500)
        
        @self.app.on_event("startup")
        async def startup():
            self.logger.log_message(LogEvent.STARTUP, {Field.PLAYER_ID: self.player_id, "port": self.port})
            asyncio.create_task(self._register_with_lm())
    
    async def _register_with_lm(self):
        """Register this player with the League Manager with retry."""
        try:
            await asyncio.sleep(2)
            msg = build_league_register_request(self.player_id, self.endpoint)
            self.logger.log_message("REGISTERING", {"endpoint": _lm_endpoint})
            resp = await send_with_retry(
                _lm_endpoint, msg,
                max_retries=_system_config.retry_policy["max_retries"],
                timeout=_system_config.timeouts["http_request"],
                retry_delay=_system_config.retry_policy["retry_delay"]
            )
            if resp and resp.get(Field.STATUS) == Status.REGISTERED:
                self.auth_token = resp.get(Field.AUTH_TOKEN)
                self.logger.log_message(LogEvent.PLAYER_REGISTERED, {Field.PLAYER_ID: self.player_id})
            else:
                self.logger.log_error(LogEvent.ERROR, f"Registration failed: {resp}")
        except Exception as e:
            self.logger.log_error("REGISTRATION_EXCEPTION", f"{type(e).__name__}: {e}")
    
    def _handle_invitation(self, msg: dict) -> dict:
        self.logger.log_message(LogEvent.GAME_INVITATION_RECEIVED, {Field.MATCH_ID: msg.get(Field.MATCH_ID)})
        return build_game_join_ack(
            msg.get(Field.LEAGUE_ID), msg.get(Field.ROUND_ID), msg.get(Field.MATCH_ID),
            self.player_id, msg.get(Field.CONVERSATION_ID)
        )
    
    def _handle_parity_call(self, msg: dict) -> dict:
        history = PlayerHistoryRepository(self.player_id).load_history().get("opponent_choices", [])
        choice = self.strategy.choose_parity(history)
        self.logger.log_message(LogEvent.PARITY_CHOICE_MADE, {Field.MATCH_ID: msg.get(Field.MATCH_ID), Field.CHOICE: choice})
        return build_parity_choice(
            msg.get(Field.LEAGUE_ID), msg.get(Field.ROUND_ID), msg.get(Field.MATCH_ID),
            self.player_id, choice, msg.get(Field.CONVERSATION_ID)
        )
    
    def _handle_game_over(self, msg: dict):
        self.logger.log_message(LogEvent.GAME_OVER_RECEIVED, {Field.MATCH_ID: msg.get(Field.MATCH_ID), Field.WINNER: msg.get(Field.WINNER)})
    
    def run(self):
        uvicorn.run(self.app, host=SERVER_HOST, port=self.port)


def create_app(player_id: str, port: int, strategy_name: str) -> FastAPI:
    return GenericPlayer(player_id, strategy_name, port).app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player-id", required=True)
    parser.add_argument("--strategy", required=True, choices=[StrategyType.RANDOM, StrategyType.FREQUENCY, StrategyType.PATTERN])
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    GenericPlayer(args.player_id, args.strategy, args.port).run()


if __name__ == "__main__":
    main()
