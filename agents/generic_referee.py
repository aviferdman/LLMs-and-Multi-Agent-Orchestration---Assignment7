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
from SHARED.contracts import (
    build_game_invitation,
    build_choose_parity_call,
    build_game_over,
    build_match_result_report
)
from SHARED.constants import (
    MessageType,
    Field,
    Status,
    LogEvent,
    Endpoint,
    Timeout,
    MCP_PATH,
    ParityChoice,
    Winner,
    GameStatus,
    EVEN_ODD_MIN_NUMBER,
    EVEN_ODD_MAX_NUMBER
)
import random
from enum import Enum
from typing import Optional, Dict, Any

# ============================================================================
# GAME LOGIC
# ============================================================================

class EvenOddGameRules:
    """Game rules for Even-Odd game."""
    
    def __init__(self):
        """Initialize game rules."""
        self.draw_range = (EVEN_ODD_MIN_NUMBER, EVEN_ODD_MAX_NUMBER)
        self.valid_choices = [ParityChoice.EVEN.lower(), ParityChoice.ODD.lower()]
    
    def draw_number(self) -> int:
        """Draw random number between 1 and 10 inclusive."""
        return random.randint(self.draw_range[0], self.draw_range[1])
    
    def get_parity(self, number: int) -> str:
        """Get parity of number (even or odd)."""
        return ParityChoice.EVEN.lower() if number % 2 == 0 else ParityChoice.ODD.lower()
    
    def validate_parity_choice(self, choice: str) -> bool:
        """Validate if parity choice is valid."""
        return choice.lower() in self.valid_choices
    
    def determine_winner(
        self,
        choice_a: str,
        choice_b: str,
        drawn_number: int
    ) -> str:
        """Determine winner based on choices and drawn number."""
        parity = self.get_parity(drawn_number)
        
        a_correct = (choice_a.lower() == parity)
        b_correct = (choice_b.lower() == parity)
        
        if a_correct and not b_correct:
            return Winner.PLAYER_A
        elif b_correct and not a_correct:
            return Winner.PLAYER_B
        else:
            return Winner.DRAW

# ============================================================================
# STATE MACHINE
# ============================================================================

class MatchState(Enum):
    """Match states."""
    WAITING_FOR_PLAYERS = GameStatus.WAITING_FOR_PLAYERS
    COLLECTING_CHOICES = GameStatus.COLLECTING_CHOICES
    DRAWING_NUMBER = GameStatus.DRAWING_NUMBER
    FINISHED = GameStatus.FINISHED

class MatchStateMachine:
    """State machine for match lifecycle."""
    
    def __init__(self):
        """Initialize state machine."""
        self.current_state = MatchState.WAITING_FOR_PLAYERS
        self.valid_transitions = {
            MatchState.WAITING_FOR_PLAYERS: [MatchState.COLLECTING_CHOICES],
            MatchState.COLLECTING_CHOICES: [MatchState.DRAWING_NUMBER],
            MatchState.DRAWING_NUMBER: [MatchState.FINISHED],
            MatchState.FINISHED: []
        }
    
    def transition(self, new_state: MatchState) -> bool:
        """Attempt state transition."""
        if self.is_valid_transition(new_state):
            self.current_state = new_state
            return True
        return False
    
    def is_valid_transition(self, new_state: MatchState) -> bool:
        """Check if transition to new state is valid."""
        return new_state in self.valid_transitions[self.current_state]
    
    def get_state(self) -> MatchState:
        """Get current state."""
        return self.current_state
    
    def is_finished(self) -> bool:
        """Check if match is finished."""
        return self.current_state == MatchState.FINISHED

# ============================================================================
# MATCH CONTEXT
# ============================================================================

class MatchContext:
    """Context for managing match state."""
    
    def __init__(self, match_id: str, player_a: str, player_b: str):
        """Initialize match context."""
        self.match_id = match_id
        self.player_a = player_a
        self.player_b = player_b
        self.player_a_joined = False
        self.player_b_joined = False
        self.player_a_choice: Optional[str] = None
        self.player_b_choice: Optional[str] = None
        self.conversation_ids: Dict[str, str] = {}
    
    def record_join(self, player_id: str, conversation_id: str) -> None:
        """Record player join."""
        self.conversation_ids[player_id] = conversation_id
        if player_id == self.player_a:
            self.player_a_joined = True
        elif player_id == self.player_b:
            self.player_b_joined = True
    
    def both_players_joined(self) -> bool:
        """Check if both players have joined."""
        return self.player_a_joined and self.player_b_joined
    
    def record_choice(self, player_id: str, choice: str) -> None:
        """Record player choice."""
        if player_id == self.player_a:
            self.player_a_choice = choice
        elif player_id == self.player_b:
            self.player_b_choice = choice
    
    def both_choices_received(self) -> bool:
        """Check if both choices are received."""
        return (self.player_a_choice is not None and 
                self.player_b_choice is not None)

def handle_game_join_ack(
    message: Dict[str, Any],
    match_context: MatchContext,
    logger: LeagueLogger
) -> bool:
    """Handle game join acknowledgment."""
    player_id = message.get(Field.SENDER)
    conversation_id = message.get(Field.CONVERSATION_ID)
    
    match_context.record_join(player_id, conversation_id)
    logger.log_message("PLAYER_JOINED", {
        Field.PLAYER_ID: player_id,
        Field.MATCH_ID: match_context.match_id
    })
    
    return True

def handle_parity_choice(
    message: Dict[str, Any],
    match_context: MatchContext,
    logger: LeagueLogger
) -> bool:
    """Handle parity choice from player."""
    player_id = message.get(Field.SENDER)
    choice = message.get(Field.CHOICE)
    
    valid_choices = [ParityChoice.EVEN.lower(), ParityChoice.ODD.lower()]
    if choice.lower() not in valid_choices:
        logger.log_error("INVALID_CHOICE", f"Player {player_id}: {choice}")
        return False
    
    match_context.record_choice(player_id, choice)
    logger.log_message("CHOICE_RECEIVED", {
        Field.PLAYER_ID: player_id,
        Field.CHOICE: choice
    })
    
    return True

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
                        handle_game_join_ack(
                            message,
                            self.active_matches[match_id]["context"],
                            self.logger
                        )
                
                elif message_type == MessageType.PARITY_CHOICE:
                    match_id = message.get(Field.MATCH_ID)
                    if match_id in self.active_matches:
                        handle_parity_choice(
                            message,
                            self.active_matches[match_id]["context"],
                            self.logger
                        )
                
                return JSONResponse(content={Field.STATUS: Status.OK})
                
            except Exception as e:
                self.logger.log_error(LogEvent.REQUEST_ERROR, str(e))
                return JSONResponse(
                    content={Status.ERROR: "Internal error"},
                    status_code=500
                )
    
    async def run_match(
        self,
        league_id: str,
        round_id: int,
        match_id: str,
        player_a: str,
        player_b: str,
        player_a_endpoint: str,
        player_b_endpoint: str
    ):
        """Orchestrate a complete match."""
        self.logger.log_message(LogEvent.MATCH_START, {Field.MATCH_ID: match_id})
        
        state_machine = MatchStateMachine()
        context = MatchContext(match_id, player_a, player_b)
        self.active_matches[match_id] = {
            "state_machine": state_machine,
            "context": context
        }
        
        # Send invitations
        inv_a = build_game_invitation(
            league_id, round_id, match_id, self.referee_id, player_a, player_b
        )
        inv_b = build_game_invitation(
            league_id, round_id, match_id, self.referee_id, player_b, player_a
        )
        
        await send_message(player_a_endpoint, inv_a, timeout=Timeout.GAME_JOIN_ACK)
        await send_message(player_b_endpoint, inv_b, timeout=Timeout.GAME_JOIN_ACK)
        await asyncio.sleep(Timeout.GAME_JOIN_ACK)
        
        if not context.both_players_joined():
            self.logger.log_error(LogEvent.TIMEOUT, "Players did not join")
            return
        
        state_machine.transition(MatchState.COLLECTING_CHOICES)
        
        choice_a = build_choose_parity_call(
            league_id, round_id, match_id, self.referee_id, player_a
        )
        choice_b = build_choose_parity_call(
            league_id, round_id, match_id, self.referee_id, player_b
        )
        
        await send_message(player_a_endpoint, choice_a, timeout=Timeout.PARITY_CHOICE)
        await send_message(player_b_endpoint, choice_b, timeout=Timeout.PARITY_CHOICE)
        await asyncio.sleep(Timeout.PARITY_CHOICE)
        
        if not context.both_choices_received():
            self.logger.log_error(LogEvent.TIMEOUT, "Choices not received")
            return
        
        state_machine.transition(MatchState.DRAWING_NUMBER)
        drawn_number = self.game_rules.draw_number()
        winner = self.game_rules.determine_winner(
            context.player_a_choice,
            context.player_b_choice,
            drawn_number
        )
        
        game_over_msg = build_game_over(
            league_id, round_id, match_id, self.referee_id,
            winner, drawn_number,
            context.player_a_choice,
            context.player_b_choice
        )
        
        await send_message(player_a_endpoint, game_over_msg)
        await send_message(player_b_endpoint, game_over_msg)
        
        result_report = build_match_result_report(
            league_id, round_id, match_id, self.referee_id,
            player_a, player_b, winner
        )
        
        await send_message(Endpoint.LEAGUE_MANAGER, result_report)
        
        state_machine.transition(MatchState.FINISHED)
        self.logger.log_message(LogEvent.MATCH_COMPLETE, {Field.MATCH_ID: match_id})
    
    def run(self):
        """Run the referee server."""
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)

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
