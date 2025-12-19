"""Generic player agent - supports all strategies."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Optional
import argparse

from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.repositories import PlayerHistoryRepository
from SHARED.contracts import build_game_join_ack, build_parity_choice
from SHARED.constants import (
    MessageType,
    Field,
    Status,
    LogEvent,
    StrategyType,
    ParityChoice
)
import random
from collections import Counter

# ============================================================================
# STRATEGY IMPLEMENTATIONS
# ============================================================================

class RandomStrategy:
    """Random parity choice strategy."""
    
    def choose_parity(self, opponent_history: list) -> str:
        """Choose randomly between even and odd."""
        return random.choice([ParityChoice.EVEN, ParityChoice.ODD])

class FrequencyStrategy:
    """Counter opponent's most frequent choice."""
    
    def choose_parity(self, opponent_history: list) -> str:
        """Choose opposite of opponent's most frequent choice."""
        if not opponent_history:
            return random.choice([ParityChoice.EVEN, ParityChoice.ODD])
        
        counter = Counter(opponent_history)
        most_common = counter.most_common(1)[0][0]
        
        return ParityChoice.ODD if most_common == ParityChoice.EVEN else ParityChoice.EVEN

class PatternStrategy:
    """Detect and exploit patterns in opponent choices."""
    
    def choose_parity(self, opponent_history: list) -> str:
        """Look for 3-choice patterns to predict next move."""
        if len(opponent_history) < 3:
            return random.choice([ParityChoice.EVEN, ParityChoice.ODD])
        
        last_three = tuple(opponent_history[-3:])
        
        pattern_predictions = {}
        for i in range(len(opponent_history) - 3):
            pattern = tuple(opponent_history[i:i+3])
            next_choice = opponent_history[i+3]
            
            if pattern not in pattern_predictions:
                pattern_predictions[pattern] = []
            pattern_predictions[pattern].append(next_choice)
        
        if last_three in pattern_predictions:
            predictions = pattern_predictions[last_three]
            predicted = Counter(predictions).most_common(1)[0][0]
            return ParityChoice.ODD if predicted == ParityChoice.EVEN else ParityChoice.EVEN
        
        return random.choice([ParityChoice.EVEN, ParityChoice.ODD])

# Strategy mapping
STRATEGIES = {
    StrategyType.RANDOM: RandomStrategy,
    StrategyType.FREQUENCY: FrequencyStrategy,
    StrategyType.PATTERN: PatternStrategy
}

class GenericPlayer:
    """Generic player that can use any strategy."""
    
    def __init__(self, player_id: str, strategy_name: str, port: int):
        """Initialize player with strategy."""
        self.player_id = player_id
        self.port = port
        self.logger = LeagueLogger(player_id)
        
        strategy_class = STRATEGIES.get(strategy_name, RandomStrategy)
        self.strategy = strategy_class()
        
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
                
                message_type = message.get(Field.MESSAGE_TYPE)
                response = None
                
                if message_type == MessageType.GAME_INVITATION:
                    response = self.handle_game_invitation(message)
                
                elif message_type == MessageType.CHOOSE_PARITY_CALL:
                    response = self.handle_choose_parity_call(message)
                
                elif message_type == MessageType.GAME_OVER:
                    self.handle_game_over(message)
                    response = {Field.STATUS: Status.ACKNOWLEDGED}
                
                else:
                    response = {Status.ERROR: "Unknown message type"}
                
                if response:
                    self.logger.log_message(LogEvent.SENT, response)
                    return JSONResponse(content=response)
                
                return JSONResponse(content={Field.STATUS: Status.OK})
                
            except Exception as e:
                self.logger.log_error(LogEvent.REQUEST_ERROR, str(e))
                return JSONResponse(
                    content={Status.ERROR: "Internal error"},
                    status_code=500
                )
        
        @self.app.on_event("startup")
        async def startup():
            """Log startup."""
            self.logger.log_message(LogEvent.STARTUP, {
                Field.PLAYER_ID: self.player_id,
                "port": self.port
            })
    
    def handle_game_invitation(self, message: dict) -> dict:
        """Handle game invitation."""
        self.logger.log_message(LogEvent.GAME_INVITATION_RECEIVED, {
            Field.MATCH_ID: message.get(Field.MATCH_ID),
            "opponent": message.get(Field.OPPONENT_ID)
        })
        
        return build_game_join_ack(
            message.get(Field.LEAGUE_ID),
            message.get(Field.ROUND_ID),
            message.get(Field.MATCH_ID),
            self.player_id,
            message.get(Field.CONVERSATION_ID)
        )
    
    def handle_choose_parity_call(self, message: dict) -> dict:
        """Handle parity choice request."""
        history_repo = PlayerHistoryRepository(self.player_id)
        history = history_repo.load()
        opponent_history = history.get("opponent_choices", [])
        
        choice = self.strategy.choose_parity(opponent_history)
        
        self.logger.log_message(LogEvent.PARITY_CHOICE_MADE, {
            Field.MATCH_ID: message.get(Field.MATCH_ID),
            Field.CHOICE: choice
        })
        
        return build_parity_choice(
            message.get(Field.LEAGUE_ID),
            message.get(Field.ROUND_ID),
            message.get(Field.MATCH_ID),
            self.player_id,
            choice,
            message.get(Field.CONVERSATION_ID)
        )
    
    def handle_game_over(self, message: dict) -> None:
        """Handle game over notification."""
        self.logger.log_message(LogEvent.GAME_OVER_RECEIVED, {
            Field.MATCH_ID: message.get(Field.MATCH_ID),
            Field.WINNER: message.get(Field.WINNER)
        })
    
    def run(self):
        """Run the player server."""
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--player-id", required=True)
    parser.add_argument("--strategy", required=True, 
                       choices=[StrategyType.RANDOM, StrategyType.FREQUENCY, StrategyType.PATTERN])
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    
    player = GenericPlayer(args.player_id, args.strategy, args.port)
    player.run()

if __name__ == "__main__":
    main()
