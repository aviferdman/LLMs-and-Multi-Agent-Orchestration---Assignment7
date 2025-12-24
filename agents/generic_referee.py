"""Generic referee agent - supports all game types."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import argparse, asyncio, os
import uvicorn
from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse
from agents.referee_game_logic import get_game_rules
from agents.referee_http_handlers import (
    handle_broadcast_message, handle_game_join_ack, handle_parity_choice, handle_round_announcement)
from agents.referee_match_runner import run_match_phases
from SHARED.constants import (
    AGENT_VERSION, HTTP_PROTOCOL, LOCALHOST, MCP_PATH, SERVER_HOST,
    Field, GameID, LogEvent, MessageType, Status)
from SHARED.contracts import build_referee_register_request
from SHARED.contracts.jsonrpc_helpers import (
    extract_jsonrpc_params,
    get_jsonrpc_id,
    is_jsonrpc_request,
    is_jsonrpc_response,
    wrap_jsonrpc_response,
)
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
                raw = await request.json()
                self.logger.log_message(LogEvent.RECEIVED, raw)
                message = extract_jsonrpc_params(raw) if is_jsonrpc_request(raw) else raw
                request_id = get_jsonrpc_id(raw) if is_jsonrpc_request(raw) else None
                msg_type = message.get(Field.MESSAGE_TYPE)
                if msg_type == MessageType.ROUND_ANNOUNCEMENT:
                    response = handle_round_announcement(message, self, background_tasks, request_id)
                elif msg_type == MessageType.GAME_JOIN_ACK:
                    response = handle_game_join_ack(message, self, request_id)
                elif msg_type == MessageType.PARITY_CHOICE:
                    response = handle_parity_choice(message, self, request_id)
                elif msg_type in (MessageType.ROUND_COMPLETED, MessageType.LEAGUE_STANDINGS_UPDATE,
                                  MessageType.LEAGUE_COMPLETED):
                    response = handle_broadcast_message(message, self, request_id)
                    if msg_type == MessageType.LEAGUE_COMPLETED:
                        asyncio.create_task(self._shutdown_gracefully())
                elif msg_type == MessageType.SHUTDOWN_COMMAND:
                    self.logger.log_message("SHUTDOWN_RECEIVED", {})
                    result = {Field.STATUS: Status.ACKNOWLEDGED}
                    response = wrap_jsonrpc_response(result, request_id) if request_id else result
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
            register_msg = build_referee_register_request(
                referee_id=self.referee_id,
                display_name=f"Referee {self.referee_id}",
                version=AGENT_VERSION,
                contact_endpoint=self.endpoint,
                game_types=[self.game_type],
            )
            self.logger.log_message("REGISTERING", {"endpoint": _lm_endpoint})
            response = await send_with_retry(
                _lm_endpoint,
                register_msg,
                max_retries=_system_config.retry_policy["max_retries"],
                timeout=_system_config.timeouts["http_request"],
                retry_delay=_system_config.retry_policy["retry_delay"],
            )
            # Extract content from JSON-RPC response (result or params)
            if response:
                if is_jsonrpc_response(response):
                    inner = response.get("result", {})
                else:
                    inner = extract_jsonrpc_params(response)
                status = inner.get(Field.STATUS)
                if status in (Status.ACCEPTED, Status.REGISTERED):
                    self.auth_token = inner.get(Field.AUTH_TOKEN)
                    self.logger.log_message(
                        LogEvent.REFEREE_REGISTERED, {Field.REFEREE_ID: self.referee_id}
                    )
                else:
                    self.logger.log_error(LogEvent.ERROR, f"Registration failed: {response}")
            else:
                self.logger.log_error(LogEvent.ERROR, "Registration failed: No response")
        except Exception as e:
            self.logger.log_error("REGISTRATION_EXCEPTION", f"{type(e).__name__}: {e}")

    async def run_match(self, league_id, round_id, match_id, player_a, player_b, ep_a, ep_b):
        await run_match_phases(self, league_id, round_id, match_id, player_a, player_b, ep_a, ep_b)

    async def _shutdown_gracefully(self):
        await asyncio.sleep(1)
        self.logger.log_message("SHUTDOWN_INITIATED", {Field.REFEREE_ID: self.referee_id})
        os._exit(0)

    def run(self):
        uvicorn.run(self.app, host=SERVER_HOST, port=self.port)


def create_app(referee_id: str, port: int, game_type: str = GameID.EVEN_ODD) -> FastAPI:
    return GenericReferee(referee_id, port, game_type).app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--referee-id", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--game-type", default=GameID.EVEN_ODD)
    args = parser.parse_args()
    GenericReferee(args.referee_id, args.port, args.game_type).run()


if __name__ == "__main__":
    main()