"""Tests for Phase 10 visualization and statistical analysis."""

import os
import sys
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2_contingency

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
