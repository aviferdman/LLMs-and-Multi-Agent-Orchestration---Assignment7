"""Utility functions for statistical analysis."""

from collections import defaultdict

import numpy as np
from scipy import stats


def calculate_strategy_stats(df):
    """Calculate win rates and statistics for each strategy."""
    strategy_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "draws": 0, "total_matches": 0})
    for _, row in df.iterrows():
        p1_strategy, p2_strategy = row["player1_strategy"], row["player2_strategy"]
        winner = row["winner_id"]
        # Player 1
        strategy_stats[p1_strategy]["total_matches"] += 1
        if winner == row["player1_id"]:
            strategy_stats[p1_strategy]["wins"] += 1
        elif winner == "DRAW":
            strategy_stats[p1_strategy]["draws"] += 1
        else:
            strategy_stats[p1_strategy]["losses"] += 1
        # Player 2
        strategy_stats[p2_strategy]["total_matches"] += 1
        if winner == row["player2_id"]:
            strategy_stats[p2_strategy]["wins"] += 1
        elif winner == "DRAW":
            strategy_stats[p2_strategy]["draws"] += 1
        else:
            strategy_stats[p2_strategy]["losses"] += 1
    return strategy_stats


def calculate_rates_and_points(strategy_stats):
    """Calculate win rates and points from strategy stats."""
    import pandas as pd

    results = []
    for strategy, stats_dict in strategy_stats.items():
        total = stats_dict["total_matches"]
        wins = stats_dict["wins"]
        losses = stats_dict["losses"]
        draws = stats_dict["draws"]

        win_rate = wins / total if total > 0 else 0
        draw_rate = draws / total if total > 0 else 0
        loss_rate = losses / total if total > 0 else 0

        # Points: win=3, draw=1, loss=0
        points = wins * 3 + draws * 1
        avg_points = points / total if total > 0 else 0

        results.append(
            {
                "strategy": strategy,
                "wins": wins,
                "losses": losses,
                "draws": draws,
                "total_matches": total,
                "win_rate": win_rate,
                "draw_rate": draw_rate,
                "loss_rate": loss_rate,
                "total_points": points,
                "avg_points_per_match": avg_points,
            }
        )

    return pd.DataFrame(results)


def calculate_head_to_head(df):
    """Calculate head-to-head win rates between strategies."""
    h2h = defaultdict(lambda: defaultdict(lambda: {"wins": 0, "total": 0}))

    for _, row in df.iterrows():
        p1_strat = row["player1_strategy"]
        p2_strat = row["player2_strategy"]
        winner = row["winner_id"]

        if winner != "DRAW":
            # Record for player 1's strategy
            h2h[p1_strat][p2_strat]["total"] += 1
            if winner == row["player1_id"]:
                h2h[p1_strat][p2_strat]["wins"] += 1

            # Record for player 2's strategy
            h2h[p2_strat][p1_strat]["total"] += 1
            if winner == row["player2_id"]:
                h2h[p2_strat][p1_strat]["wins"] += 1

    # Convert to win rates
    h2h_rates = {}
    for strat1 in h2h:
        h2h_rates[strat1] = {}
        for strat2 in h2h[strat1]:
            total = h2h[strat1][strat2]["total"]
            wins = h2h[strat1][strat2]["wins"]
            h2h_rates[strat1][strat2] = wins / total if total > 0 else 0.0

    return h2h_rates


def calculate_cohens_d(strategies, win_rates):
    """Calculate Cohen's d effect sizes between strategy pairs."""
    effect_sizes = {}
    for i in range(len(strategies)):
        for j in range(i + 1, len(strategies)):
            p1 = win_rates[i]
            p2 = win_rates[j]

            sd1 = np.sqrt(p1 * (1 - p1))
            sd2 = np.sqrt(p2 * (1 - p2))
            pooled_sd = np.sqrt((sd1**2 + sd2**2) / 2)

            if pooled_sd > 0:
                cohens_d = abs(p1 - p2) / pooled_sd
            else:
                cohens_d = 0.0

            effect_sizes[f"{strategies[i]}_vs_{strategies[j]}"] = cohens_d

    return effect_sizes


def calculate_confidence_intervals(strategy_df):
    """Calculate 95% confidence intervals for win rates."""
    confidence_intervals = {}
    for _, row in strategy_df.iterrows():
        strategy = row["strategy"]
        win_rate = row["win_rate"]
        n = row["total_matches"]

        # Standard error
        se = np.sqrt(win_rate * (1 - win_rate) / n)

        # 95% CI
        ci_lower = max(0, win_rate - 1.96 * se)
        ci_upper = min(1, win_rate + 1.96 * se)

        confidence_intervals[strategy] = {
            "win_rate": win_rate,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "margin_of_error": 1.96 * se,
        }

    return confidence_intervals
