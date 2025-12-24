# Agent Strategy Documentation

**Document Version**: 1.0  
**Last Updated**: December 2025

---

## Overview

This document describes the decision-making strategies implemented by each player agent in the Even-Odd game competition. Each player uses a distinct approach to choose between "even" and "odd" parity options.

---

## Player Strategies

### P01 - RandomStrategy

**Strategy Type**: Pure Random  
**Complexity**: O(1)

The Random strategy selects between "even" and "odd" with equal probability (50/50). This approach:
- Provides a baseline performance benchmark
- Is unpredictable to opponents
- Does not adapt to opponent behavior

```python
def choose_parity(opponent_history):
    return random.choice(["even", "odd"])
```

**Expected Win Rate**: 50% (theoretical baseline)

---

### P02 - FrequencyStrategy

**Strategy Type**: Statistical Counter  
**Complexity**: O(n) where n = history length

The Frequency strategy analyzes the opponent's historical choices and counters their most frequently used option:

1. Count occurrences of "even" and "odd" in opponent history
2. Identify the most common choice
3. Select the opposite parity

```python
def choose_parity(opponent_history):
    if not opponent_history:
        return random.choice(["even", "odd"])
    most_common = Counter(opponent_history).most_common(1)[0][0]
    return "odd" if most_common == "even" else "even"
```

**Strength**: Exploits opponents with consistent preferences  
**Weakness**: Can be exploited by adaptive opponents

---

### P03 - PatternStrategy

**Strategy Type**: Sequence Pattern Detection  
**Complexity**: O(n²) for pattern building

The Pattern strategy looks for repeating 3-choice sequences in opponent behavior:

1. Analyze opponent's choice history for 3-element patterns
2. When current pattern matches a historical pattern, predict next choice
3. Counter the predicted choice

```python
def choose_parity(opponent_history):
    if len(opponent_history) < 3:
        return random.choice(["even", "odd"])
    
    last_three = tuple(opponent_history[-3:])
    # Look for pattern matches and predict
    if last_three in pattern_predictions:
        predicted = most_likely_prediction(pattern_predictions[last_three])
        return opposite_of(predicted)
    
    return random.choice(["even", "odd"])
```

**Strength**: Detects and exploits behavioral patterns  
**Weakness**: Requires sufficient history; ineffective against random opponents

---

### P04 - RandomStrategy

**Strategy Type**: Pure Random  
**Complexity**: O(1)

Same as P01, using pure random selection for parity choice.

---

## Strategy Comparison

| Player | Strategy | Adapts to Opponent | Memory Use | Best Against |
|--------|----------|-------------------|------------|--------------|
| P01 | Random | No | None | All (baseline) |
| P02 | Frequency | Yes | Linear | Biased opponents |
| P03 | Pattern | Yes | Quadratic | Patterned opponents |
| P04 | Random | No | None | All (baseline) |

---

## Opponent Modeling

Players P02 and P03 implement basic opponent modeling:

1. **History Tracking**: Store all opponent choices per match
2. **Analysis**: Apply strategy-specific analysis
3. **Prediction**: Predict opponent's next choice
4. **Counter**: Select the opposite parity

This opponent modeling capability allows adaptive strategies to improve performance against predictable opponents while maintaining baseline performance against random opponents.

---

## Mathematical Foundation

For the Even-Odd game:

- **Random Baseline**: $P(win) = 0.5$
- **Against Biased Opponent**: If opponent chooses "even" with probability $p > 0.5$, always choosing "odd" yields $P(win) = p$
- **Pattern Exploitation**: Success depends on pattern predictability in opponent behavior

---

## Implementation Notes

1. All strategies are stateless between matches
2. Opponent history is provided via `GAME_INVITATION` message
3. Strategies must respond within 30-second timeout
4. Invalid responses result in automatic loss

---

**Document Owner**: Assignment 7 Team  
**Status**: ✅ Complete
