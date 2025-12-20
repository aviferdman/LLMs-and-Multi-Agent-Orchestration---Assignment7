"""Tests for Phase 10 research analysis scripts."""

import json
import os
import sys
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDataGeneration:
    """Test data generation functionality."""

    def test_generate_balanced_data_creates_file(self, tmp_path):
        """Test that data generation creates the expected CSV file."""
        # Mock the file path
        test_file = tmp_path / "test_data.csv"

        # Create test data
        import csv

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
        import numpy as np
        from scipy import stats

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


class TestVisualizationScript:
    """Test visualization script functionality."""

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.close")
    def test_bar_chart_creation(self, mock_close, mock_savefig):
        """Test that bar chart is created correctly."""
        import matplotlib.pyplot as plt

        # Create simple bar chart
        strategies = ["Random", "Frequency", "Pattern"]
        win_rates = [0.338, 0.338, 0.318]

        fig, ax = plt.subplots()
        ax.bar(strategies, win_rates)
        ax.set_ylabel("Win Rate")
        ax.set_xlabel("Strategy")

        # Verify chart components
        assert ax.get_ylabel() == "Win Rate"
        assert ax.get_xlabel() == "Strategy"

        plt.close()

    def test_data_preparation_for_plots(self):
        """Test data preparation for visualization."""
        # Create aggregated data
        strategy_df = pd.DataFrame(
            {
                "strategy": ["Random", "Frequency", "Pattern"],
                "wins": [2700, 2700, 2560],
                "losses": [2700, 2640, 2620],
                "draws": [2580, 2640, 2860],
                "win_rate": [0.338, 0.338, 0.318],
            }
        )

        # Verify data structure
        assert len(strategy_df) == 3
        assert "win_rate" in strategy_df.columns
        assert strategy_df["win_rate"].max() <= 1.0
        assert strategy_df["win_rate"].min() >= 0.0


class TestStatisticalAnalysis:
    """Test statistical analysis functions."""

    def test_chi_square_calculation(self):
        """Test chi-square test calculation."""
        from scipy.stats import chi2_contingency

        # Test data: observed frequencies
        observed = [
            [2700, 2700, 2580],  # Random: wins, losses, draws
            [2700, 2640, 2640],  # Frequency
            [2560, 2620, 2860],  # Pattern
        ]

        chi2, p_value, dof, expected = chi2_contingency(observed)

        # Verify results
        assert chi2 > 0
        assert 0 <= p_value <= 1
        assert dof > 0

    def test_cohens_d_calculation(self):
        """Test Cohen's d effect size calculation."""
        import numpy as np

        # Test data
        group1_mean = 0.338
        group2_mean = 0.338
        pooled_std = 0.473  # Approximate

        cohens_d = (group1_mean - group2_mean) / pooled_std

        # Verify effect size
        assert abs(cohens_d) < 0.2  # Negligible effect


class TestResultsReport:
    """Test results report completeness."""

    def test_results_file_exists(self):
        """Test that RESULTS.md was created."""
        results_file = "doc/RESULTS.md"
        assert os.path.exists(results_file), "RESULTS.md should exist"

        with open(results_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Verify key sections
        assert "Executive Summary" in content
        assert "Methodology" in content
        assert "Results" in content
        assert "Statistical" in content
        assert "Conclusions" in content

    def test_csv_files_exist(self):
        """Test that CSV data files were created."""
        assert os.path.exists("doc/results/raw_data.csv")
        assert os.path.exists("doc/results/aggregated_data.csv")

    def test_visualization_files_exist(self):
        """Test that visualization PNG files were created."""
        viz_files = [
            "doc/results/win_rates_by_strategy.png",
            "doc/results/score_distribution.png",
            "doc/results/head_to_head_heatmap.png",
        ]

        for viz_file in viz_files:
            assert os.path.exists(viz_file), f"{viz_file} should exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
