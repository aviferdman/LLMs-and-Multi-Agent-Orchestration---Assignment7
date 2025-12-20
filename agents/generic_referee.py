"""Generic referee agent - supports all game types."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import argparse
import asyncio

import uvicorn
from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse

from agents.referee_game_logic import get_game_rules
from agents.referee_http_handlers import (
    handle_game_join_ack,
    handle_parity_choice,
    handle_run_match,
)
from agents.referee_match_runner import run_match_phases
from SHARED.constants import (
    HTTP_PROTOCOL,
    LOCALHOST,
    MCP_PATH,
    SERVER_HOST,
    Field,
    GameID,
    LogEvent,
    MessageType,
    Status,
)
from SHARED.contracts import build_referee_register_request
from SHARED.league_sdk.agent_comm import send_with_retry
from SHARED.league_sdk.config_loader import load_agent_config, load_system_config
from SHARED.league_sdk.logger import LeagueLogger

_system_config = load_system_config()
_agents_config = load_agent_config()
_lm_endpoint = _agents_config["league_manager"]["endpoint"]


class GenericReferee:
    """Generic referee that can manage any game type."""

    def __init__(self, referee_id: str, port: int, game_type: str = GameID.EVEN_ODD):
        self.referee_id, self.port, self.game_type = referee_id, port, game_type
        self.endpoint = f"{HTTP_PROTOCOL}://{LOCALHOST}:{port}{MCP_PATH}"
        self.logger = LeagueLogger(referee_id)
        self.game_rules = get_game_rules(game_type)
        self.active_matches, self.auth_token = {}, None
        self.app = FastAPI(title=f"Referee {referee_id}")
        self.setup_routes()

    def setup_routes(self):
        @self.app.post(MCP_PATH)
        async def mcp_endpoint(request: Request, background_tasks: BackgroundTasks) -> JSONResponse:
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
                elif msg_type == MessageType.LEAGUE_COMPLETED:
                    self.logger.log_message("LEAGUE_COMPLETED_RECEIVED", {})
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
                return JSONResponse(
                    content={Field.STATUS: Status.ERROR, "message": str(e)}, status_code=500
                )

        @self.app.on_event("startup")
        async def startup():
            self.logger.log_message(
                LogEvent.STARTUP, {Field.REFEREE_ID: self.referee_id, "port": self.port}
            )
            asyncio.create_task(self.register_with_league_manager())

    async def register_with_league_manager(self):
        try:
            await asyncio.sleep(2)
            register_msg = build_referee_register_request(self.referee_id, self.endpoint)
            self.logger.log_message("REGISTERING", {"endpoint": _lm_endpoint})
            response = await send_with_retry(
                _lm_endpoint,
                register_msg,
                max_retries=_system_config.retry_policy["max_retries"],
                timeout=_system_config.timeouts["http_request"],
                retry_delay=_system_config.retry_policy["retry_delay"],
            )
            if response and response.get(Field.STATUS) == Status.REGISTERED:
                self.auth_token = response.get(Field.AUTH_TOKEN)
                self.logger.log_message(
                    LogEvent.REFEREE_REGISTERED, {Field.REFEREE_ID: self.referee_id}
                )
            else:
                self.logger.log_error(LogEvent.ERROR, f"Registration failed: {response}")
        except Exception as e:
            self.logger.log_error("REGISTRATION_EXCEPTION", f"{type(e).__name__}: {e}")

    async def run_match(self, league_id, round_id, match_id, player_a, player_b, ep_a, ep_b):
        await run_match_phases(self, league_id, round_id, match_id, player_a, player_b, ep_a, ep_b)

    async def _shutdown_gracefully(self):
        await asyncio.sleep(1)
        self.logger.log_message("SHUTDOWN_INITIATED", {Field.REFEREE_ID: self.referee_id})
        import os

        os._exit(0)

    def run(self):
        uvicorn.run(self.app, host=SERVER_HOST, port=self.port)


def create_app(referee_id: str, port: int, game_type: str = GameID.EVEN_ODD) -> FastAPI:
    return GenericReferee(referee_id, port, game_type).app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--referee-id", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--game-type", default=GameID.EVEN_ODD, help="Game type to referee")
    args = parser.parse_args()
    GenericReferee(args.referee_id, args.port, args.game_type).run()


if __name__ == "__main__":
    main()
