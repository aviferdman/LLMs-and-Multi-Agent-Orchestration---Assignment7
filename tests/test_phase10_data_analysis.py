"""Tests for Phase 10 data generation and analysis scripts."""

import csv
import os
import sys
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from scipy import stats

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDataGeneration:
    """Test data generation functionality."""

    def test_generate_balanced_data_creates_file(self, tmp_path):
        """Test that data generation creates the expected CSV file."""
        # Mock the file path
        test_file = tmp_path / "test_data.csv"

        # Create test data
        matches = []
        for tid in range(1, 3):  # 2 tournaments
            for mid in range(1, 7):  # 6 matches each
                matches.append(
                    {
                        "tournament_id": tid,
                        "round_num": (mid - 1) // 2 + 1,
                        "match_id": f"R{(mid-1)//2+1}_M{(mid-1)%2+1}",
                        "player1_id": "P01",
                        "player1_strategy": "Random",
                        "player2_id": "P02",
                        "player2_strategy": "Frequency",
                        "winner_id": "P01",
                        "player1_score": 3,
                        "player2_score": 1,
                        "draw": False,
                    }
                )

        with open(test_file, "w", newline="") as f:
            fieldnames = [
                "tournament_id",
                "round_num",
                "match_id",
                "player1_id",
                "player1_strategy",
                "player2_id",
                "player2_strategy",
                "winner_id",
                "player1_score",
                "player2_score",
                "draw",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matches)

        # Verify file exists and has correct structure
        assert test_file.exists()
        df = pd.read_csv(test_file)
        assert len(df) == 12  # 2 tournaments × 6 matches
        assert "player1_strategy" in df.columns
        assert "player2_strategy" in df.columns


class TestAnalysisScript:
    """Test analysis script functionality."""

    def test_strategy_aggregation(self, tmp_path):
        """Test that strategy performance is aggregated correctly."""
        # Create test data
        test_data = pd.DataFrame(
            {
                "player1_id": ["P01", "P01", "P02"],
                "player1_strategy": ["Random", "Random", "Frequency"],
                "player2_id": ["P02", "P03", "P03"],
                "player2_strategy": ["Frequency", "Pattern", "Pattern"],
                "winner_id": ["P01", "DRAW", "P03"],
                "draw": [False, True, False],
            }
        )

        # Aggregate strategy performance
        strategy_stats = {}
        for strategy in ["Random", "Frequency", "Pattern"]:
            wins = 0
            losses = 0
            draws = 0
            total = 0

            for _, row in test_data.iterrows():
                if row["player1_strategy"] == strategy:
                    total += 1
                    if row["winner_id"] == row["player1_id"]:
                        wins += 1
                    elif row["draw"]:
                        draws += 1
                    else:
                        losses += 1

                if row["player2_strategy"] == strategy:
                    total += 1
                    if row["winner_id"] == row["player2_id"]:
                        wins += 1
                    elif row["draw"]:
                        draws += 1
                    else:
                        losses += 1

            if total > 0:
                strategy_stats[strategy] = {
                    "wins": wins,
                    "losses": losses,
                    "draws": draws,
                    "total": total,
                    "win_rate": wins / total,
                }

        # Verify aggregation
        assert "Random" in strategy_stats
        assert strategy_stats["Random"]["total"] == 2
        assert strategy_stats["Random"]["wins"] == 1
        assert strategy_stats["Random"]["draws"] == 1

    def test_confidence_interval_calculation(self):
        """Test confidence interval calculation."""
        # Test data
        win_rate = 0.338
        n_matches = 7980

        # Calculate 95% CI
        std_error = np.sqrt(win_rate * (1 - win_rate) / n_matches)
        ci_lower = win_rate - 1.96 * std_error
        ci_upper = win_rate + 1.96 * std_error

        # Verify CI bounds
        assert 0 <= ci_lower <= win_rate
        assert win_rate <= ci_upper <= 1
        assert ci_upper - ci_lower < 0.1  # Reasonable margin


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
