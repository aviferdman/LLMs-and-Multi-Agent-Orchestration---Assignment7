"""Round state tracking for League Manager."""

from typing import Any, Dict, List


class RoundState:
    """Track state of rounds in a league."""

    def __init__(self, total_rounds: int, matches_per_round: int = 2):
        """Initialize round state tracker.

        Args:
            total_rounds: Total number of rounds in the league
            matches_per_round: Number of matches per round
        """
        self.total_rounds = total_rounds
        self.matches_per_round = matches_per_round
        self.current_round = 0
        self.rounds_completed: Dict[int, bool] = {}
        self.round_results: Dict[int, List[Dict[str, Any]]] = {}

    def start_round(self, round_num: int) -> bool:
        """Start a new round.

        Args:
            round_num: The round number to start (1-indexed)

        Returns:
            True if round started successfully, False otherwise
        """
        if round_num < 1 or round_num > self.total_rounds:
            return False
        if round_num in self.rounds_completed:
            return False  # Round already started
        self.current_round = round_num
        self.rounds_completed[round_num] = False
        self.round_results[round_num] = []
        return True

    def add_match_result(self, round_num: int, result: Dict[str, Any]) -> None:
        """Add a match result to a round."""
        if round_num in self.round_results:
            self.round_results[round_num].append(result)

    def check_round_complete(self, round_num: int) -> bool:
        """Check if a round is complete.

        Args:
            round_num: The round number to check

        Returns:
            True if all matches in the round are complete
        """
        if round_num not in self.round_results:
            return False
        return len(self.round_results[round_num]) >= self.matches_per_round


def start_round(state: RoundState, round_num: int) -> bool:
    """Start a round in the league.

    Args:
        state: The round state tracker
        round_num: Round number to start

    Returns:
        True if round started successfully
    """
    return state.start_round(round_num)


def check_round_complete(state: RoundState, round_num: int) -> bool:
    """Check if a round is complete.

    Args:
        state: The round state tracker
        round_num: Round number to check

    Returns:
        True if all matches in the round are complete
    """
    return state.check_round_complete(round_num)
