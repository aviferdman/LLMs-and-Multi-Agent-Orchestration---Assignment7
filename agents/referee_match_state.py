"""Match state management for referee."""

from enum import Enum
from typing import Any, Dict, Optional

from SHARED.constants import Field, GameStatus, ParityChoice
from SHARED.league_sdk.logger import LeagueLogger


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
            MatchState.FINISHED: [],
        }

    def transition(self, new_state: MatchState) -> bool:
        """Attempt state transition."""
        if new_state in self.valid_transitions[self.current_state]:
            self.current_state = new_state
            return True
        return False

    def is_finished(self) -> bool:
        """Check if match is finished."""
        return self.current_state == MatchState.FINISHED


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
        return self.player_a_choice is not None and self.player_b_choice is not None


def handle_game_join_ack(
    message: Dict[str, Any], match_context: MatchContext, logger: LeagueLogger
) -> bool:
    """Handle game join acknowledgment."""
    player_id = message.get(Field.SENDER)
    conversation_id = message.get(Field.CONVERSATION_ID)
    match_context.record_join(player_id, conversation_id)
    logger.log_message(
        "PLAYER_JOINED",
        {Field.PLAYER_ID: player_id, Field.MATCH_ID: match_context.match_id},
    )
    return True


def handle_parity_choice(
    message: Dict[str, Any], match_context: MatchContext, logger: LeagueLogger
) -> bool:
    """Handle parity choice from player."""
    player_id = message.get(Field.SENDER)
    choice = message.get(Field.CHOICE)
    valid_choices = [ParityChoice.EVEN, ParityChoice.ODD]

    if choice.upper() not in valid_choices:
        logger.log_error("INVALID_CHOICE", f"Player {player_id}: {choice}")
        return False

    match_context.record_choice(player_id, choice)
    logger.log_message("CHOICE_RECEIVED", {Field.PLAYER_ID: player_id, Field.CHOICE: choice})
    return True
