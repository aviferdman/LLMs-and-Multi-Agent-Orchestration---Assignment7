"""Player strategy implementations for Even-Odd game."""

import random
import time
from collections import Counter

from SHARED.constants import ParityChoice
from SHARED.league_sdk.config_loader import load_system_config


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
            pattern = tuple(opponent_history[i : i + 3])
            next_choice = opponent_history[i + 3]
            if pattern not in pattern_predictions:
                pattern_predictions[pattern] = []
            pattern_predictions[pattern].append(next_choice)

        if last_three in pattern_predictions:
            predictions = pattern_predictions[last_three]
            predicted = Counter(predictions).most_common(1)[0][0]
            return ParityChoice.ODD if predicted == ParityChoice.EVEN else ParityChoice.EVEN

        return random.choice([ParityChoice.EVEN, ParityChoice.ODD])


class TimeoutStrategy:
    """Losing strategy that deliberately times out to test timeout handling.

    This strategy waits longer than the configured parity_choice timeout,
    causing the player to always lose due to timeout.
    """

    def __init__(self):
        """Initialize with system config timeout values."""
        self._system_config = load_system_config()
        self._timeout = self._system_config.timeouts.get("parity_choice", 30)

    def choose_parity(self, opponent_history: list) -> str:
        """Sleep longer than timeout, then return a choice (which will be too late)."""
        # Wait 1 second longer than the configured timeout
        delay = self._timeout + 1
        time.sleep(delay)
        return random.choice([ParityChoice.EVEN, ParityChoice.ODD])


# Strategy mapping
STRATEGIES = {
    "random": RandomStrategy,
    "frequency": FrequencyStrategy,
    "pattern": PatternStrategy,
    "timeout": TimeoutStrategy,
}
