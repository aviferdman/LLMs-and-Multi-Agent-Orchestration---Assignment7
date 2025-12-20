"""Generic player agent - supports all strategies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import argparse
import asyncio

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from agents.player_handlers import handle_game_over, handle_invitation, handle_parity_call
from agents.player_strategies import STRATEGIES, RandomStrategy
from SHARED.constants import (
    HTTP_PROTOCOL,
    LOCALHOST,
    MCP_PATH,
    SERVER_HOST,
    Field,
    LogEvent,
    MessageType,
    Status,
    StrategyType,
)
from SHARED.contracts import build_league_register_request
from SHARED.league_sdk.agent_comm import send_with_retry
from SHARED.league_sdk.config_loader import load_agent_config, load_system_config
from SHARED.league_sdk.logger import LeagueLogger

_system_config = load_system_config()
_agents_config = load_agent_config()
_lm_endpoint = _agents_config["league_manager"]["endpoint"]


class GenericPlayer:
    """Generic player that can use any strategy."""

    def __init__(self, player_id: str, strategy_name: str, port: int):
        self.player_id, self.port = player_id, port
        self.endpoint = f"{HTTP_PROTOCOL}://{LOCALHOST}:{port}{MCP_PATH}"
        self.logger = LeagueLogger(player_id)
        self.strategy = STRATEGIES.get(strategy_name, RandomStrategy)()
        self.auth_token = None
        self.app = FastAPI(title=f"Player {player_id}")
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/mcp")
        async def mcp_endpoint(request: Request) -> JSONResponse:
            try:
                message = await request.json()
                self.logger.log_message(LogEvent.RECEIVED, message)
                msg_type = message.get(Field.MESSAGE_TYPE)
                if msg_type == MessageType.GAME_INVITATION:
                    response = handle_invitation(
                        self.player_id, message, self.logger, message.get(Field.CONVERSATION_ID)
                    )
                elif msg_type == MessageType.CHOOSE_PARITY_CALL:
                    response = handle_parity_call(
                        self.player_id, message, self.strategy, self.logger
                    )
                elif msg_type == MessageType.GAME_OVER:
                    handle_game_over(message, self.logger)
                    response = {Field.STATUS: Status.ACKNOWLEDGED}
                elif msg_type == MessageType.LEAGUE_COMPLETED:
                    self.logger.log_message(
                        "LEAGUE_COMPLETED_RECEIVED",
                        {"final_standings": message.get("final_standings", [])},
                    )
                    response = {Field.STATUS: Status.ACKNOWLEDGED}
                    asyncio.create_task(self._shutdown_gracefully())
                elif msg_type == MessageType.SHUTDOWN_COMMAND:
                    self.logger.log_message("SHUTDOWN_RECEIVED", {})
                    response = {Field.STATUS: Status.ACKNOWLEDGED}
                    asyncio.create_task(self._shutdown_gracefully())
                else:
                    response = {Field.STATUS: Status.ERROR, "message": "Unknown message type"}
                self.logger.log_message(LogEvent.SENT, response)
                return JSONResponse(content=response)
            except Exception as e:
                self.logger.log_error(LogEvent.REQUEST_ERROR, str(e))
                return JSONResponse(content={Field.STATUS: Status.ERROR}, status_code=500)

        @self.app.on_event("startup")
        async def startup():
            self.logger.log_message(
                LogEvent.STARTUP, {Field.PLAYER_ID: self.player_id, "port": self.port}
            )
            asyncio.create_task(self._register_with_lm())

    async def _register_with_lm(self):
        try:
            await asyncio.sleep(2)
            msg = build_league_register_request(self.player_id, self.endpoint)
            self.logger.log_message("REGISTERING", {"endpoint": _lm_endpoint})
            resp = await send_with_retry(
                _lm_endpoint,
                msg,
                max_retries=_system_config.retry_policy["max_retries"],
                timeout=_system_config.timeouts["http_request"],
                retry_delay=_system_config.retry_policy["retry_delay"],
            )
            if resp and resp.get(Field.STATUS) == Status.REGISTERED:
                self.auth_token = resp.get(Field.AUTH_TOKEN)
                self.logger.log_message(
                    LogEvent.PLAYER_REGISTERED, {Field.PLAYER_ID: self.player_id}
                )
            else:
                self.logger.log_error(LogEvent.ERROR, f"Registration failed: {resp}")
        except Exception as e:
            self.logger.log_error("REGISTRATION_EXCEPTION", f"{type(e).__name__}: {e}")

    async def _shutdown_gracefully(self):
        await asyncio.sleep(1)
        self.logger.log_message("SHUTDOWN_INITIATED", {Field.PLAYER_ID: self.player_id})
        import os

        os._exit(0)

    def run(self):
        uvicorn.run(self.app, host=SERVER_HOST, port=self.port)


def create_app(player_id: str, port: int, strategy_name: str) -> FastAPI:
    return GenericPlayer(player_id, strategy_name, port).app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player-id", required=True)
    parser.add_argument(
        "--strategy",
        required=True,
        choices=[StrategyType.RANDOM, StrategyType.FREQUENCY, StrategyType.PATTERN],
    )
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    GenericPlayer(args.player_id, args.strategy, args.port).run()


if __name__ == "__main__":
    main()
