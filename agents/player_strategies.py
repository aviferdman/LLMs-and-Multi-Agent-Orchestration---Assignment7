"""Player strategy implementations for Even-Odd game."""

import random
from collections import Counter

from SHARED.constants import ParityChoice


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
        return (
            ParityChoice.ODD if most_common == ParityChoice.EVEN else ParityChoice.EVEN
        )


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
            return (
                ParityChoice.ODD
                if predicted == ParityChoice.EVEN
                else ParityChoice.EVEN
            )

        return random.choice([ParityChoice.EVEN, ParityChoice.ODD])


# Strategy mapping
STRATEGIES = {
    "random": RandomStrategy,
    "frequency": FrequencyStrategy,
    "pattern": PatternStrategy,
}
