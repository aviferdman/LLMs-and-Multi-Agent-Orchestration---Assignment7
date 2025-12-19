"""Generic referee agent - supports all game types."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import argparse

from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.http_client import send_message
from SHARED.contracts import build_game_invitation, build_choose_parity_call, build_game_over, build_match_result_report
from SHARED.constants import MessageType, Field, Status, LogEvent, Endpoint, Timeout, MCP_PATH, SERVER_HOST
from agents.referee_game_logic import EvenOddGameRules
from agents.referee_match_state import MatchStateMachine, MatchContext, MatchState, handle_game_join_ack, handle_parity_choice

class GenericReferee:
    """Generic referee that can manage any game type."""
    
    def __init__(self, referee_id: str, port: int):
        """Initialize referee."""
        self.referee_id = referee_id
        self.port = port
        self.logger = LeagueLogger(referee_id)
        self.game_rules = EvenOddGameRules()
        self.active_matches = {}
        self.app = FastAPI(title=f"{LogEvent.REFEREE_REGISTERED} {referee_id}")
        self.setup_routes()
    
    def setup_routes(self):
        """Setup FastAPI routes."""
        
        @self.app.post(MCP_PATH)
        async def mcp_endpoint(request: Request) -> JSONResponse:
            """Handle MCP messages."""
            try:
                message = await request.json()
                self.logger.log_message(LogEvent.RECEIVED, message)
                message_type = message.get(Field.MESSAGE_TYPE)
                
                if message_type == MessageType.GAME_JOIN_ACK:
                    match_id = message.get(Field.MATCH_ID)
                    if match_id in self.active_matches:
                        handle_game_join_ack(message, self.active_matches[match_id]["context"], self.logger)
                elif message_type == MessageType.PARITY_CHOICE:
                    match_id = message.get(Field.MATCH_ID)
                    if match_id in self.active_matches:
                        handle_parity_choice(message, self.active_matches[match_id]["context"], self.logger)
                
                return JSONResponse(content={Field.STATUS: Status.OK})
            except Exception as e:
                self.logger.log_error(LogEvent.REQUEST_ERROR, str(e))
                return JSONResponse(content={Status.ERROR: "Internal error"}, status_code=500)
    
    async def run_match(self, league_id: str, round_id: int, match_id: str, player_a: str, player_b: str, player_a_endpoint: str, player_b_endpoint: str):
        """Orchestrate a complete match."""
        self.logger.log_message(LogEvent.MATCH_START, {Field.MATCH_ID: match_id})
        
        state_machine = MatchStateMachine()
        context = MatchContext(match_id, player_a, player_b)
        self.active_matches[match_id] = {"state_machine": state_machine, "context": context}
        
        # Send invitations
        inv_a = build_game_invitation(league_id, round_id, match_id, self.referee_id, player_a, player_b)
        inv_b = build_game_invitation(league_id, round_id, match_id, self.referee_id, player_b, player_a)
        await send_message(player_a_endpoint, inv_a, timeout=Timeout.GAME_JOIN_ACK)
        await send_message(player_b_endpoint, inv_b, timeout=Timeout.GAME_JOIN_ACK)
        await asyncio.sleep(Timeout.GAME_JOIN_ACK)
        
        if not context.both_players_joined():
            self.logger.log_error(LogEvent.TIMEOUT, "Players did not join")
            return
        
        state_machine.transition(MatchState.COLLECTING_CHOICES)
        
        # Request choices
        choice_a = build_choose_parity_call(league_id, round_id, match_id, self.referee_id, player_a)
        choice_b = build_choose_parity_call(league_id, round_id, match_id, self.referee_id, player_b)
        await send_message(player_a_endpoint, choice_a, timeout=Timeout.PARITY_CHOICE)
        await send_message(player_b_endpoint, choice_b, timeout=Timeout.PARITY_CHOICE)
        await asyncio.sleep(Timeout.PARITY_CHOICE)
        
        if not context.both_choices_received():
            self.logger.log_error(LogEvent.TIMEOUT, "Choices not received")
            return
        
        # Determine winner
        state_machine.transition(MatchState.DRAWING_NUMBER)
        drawn_number = self.game_rules.draw_number()
        winner = self.game_rules.determine_winner(context.player_a_choice, context.player_b_choice, drawn_number)
        
        # Send game over
        game_over_msg = build_game_over(league_id, round_id, match_id, self.referee_id, winner, drawn_number, context.player_a_choice, context.player_b_choice)
        await send_message(player_a_endpoint, game_over_msg)
        await send_message(player_b_endpoint, game_over_msg)
        
        # Report result
        result_report = build_match_result_report(league_id, round_id, match_id, self.referee_id, player_a, player_b, winner)
        await send_message(Endpoint.LEAGUE_MANAGER, result_report)
        
        state_machine.transition(MatchState.FINISHED)
        self.logger.log_message(LogEvent.MATCH_COMPLETE, {Field.MATCH_ID: match_id})
    
    def run(self):
        """Run the referee server."""
        uvicorn.run(self.app, host=SERVER_HOST, port=self.port)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--referee-id", required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    
    referee = GenericReferee(args.referee_id, args.port)
    referee.run()

if __name__ == "__main__":
    main()
