"""Generic player agent - supports all strategies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import argparse
import asyncio

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from agents.player_message_handlers import handle_mcp_message
from agents.player_strategies import STRATEGIES, RandomStrategy
from SHARED.constants import (
    AGENT_VERSION,
    HTTP_PROTOCOL,
    LOCALHOST,
    MCP_PATH,
    SERVER_HOST,
    Field,
    GameID,
    LogEvent,
    Status,
    StrategyType,
)
from SHARED.contracts import build_league_register_request
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params, is_jsonrpc_response
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
        self._setup_routes()

    def _setup_routes(self):
        @self.app.post("/mcp")
        async def mcp_endpoint(request: Request) -> JSONResponse:
            return await handle_mcp_message(self, request)

        @self.app.on_event("startup")
        async def startup():
            self.logger.log_message(
                LogEvent.STARTUP, {Field.PLAYER_ID: self.player_id, "port": self.port}
            )
            asyncio.create_task(self._register_with_lm())

    async def _register_with_lm(self):
        try:
            await asyncio.sleep(2)
            msg = build_league_register_request(
                player_id=self.player_id,
                display_name=f"Player {self.player_id}",
                version=AGENT_VERSION,
                contact_endpoint=self.endpoint,
                game_types=[GameID.EVEN_ODD],
            )
            self.logger.log_message("REGISTERING", {"endpoint": _lm_endpoint})
            resp = await send_with_retry(
                _lm_endpoint,
                msg,
                max_retries=_system_config.retry_policy["max_retries"],
                timeout=_system_config.timeouts["http_request"],
                retry_delay=_system_config.retry_policy["retry_delay"],
            )
            # Extract content from JSON-RPC response (result or params)
            if resp:
                if is_jsonrpc_response(resp):
                    inner = resp.get("result", {})
                else:
                    inner = extract_jsonrpc_params(resp)
                status = inner.get(Field.STATUS)
                if status in (Status.ACCEPTED, Status.REGISTERED):
                    self.auth_token = inner.get(Field.AUTH_TOKEN)
                    self.logger.log_message(LogEvent.PLAYER_REGISTERED, {Field.PLAYER_ID: self.player_id})
                else:
                    self.logger.log_error(LogEvent.ERROR, f"Registration failed: {resp}")
            else:
                self.logger.log_error(LogEvent.ERROR, "Registration failed: No response")
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
    all_strategies = [StrategyType.RANDOM, StrategyType.FREQUENCY, StrategyType.PATTERN, StrategyType.TIMEOUT]
    parser.add_argument("--strategy", required=True, choices=all_strategies)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    GenericPlayer(args.player_id, args.strategy, args.port).run()


if __name__ == "__main__":
    main()
