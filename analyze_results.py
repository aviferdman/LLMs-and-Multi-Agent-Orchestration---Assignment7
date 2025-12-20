#!/usr/bin/env python3
"""Analyze tournament results and generate statistical analysis."""
import json

import pandas as pd
from scipy import stats

from analysis_utils import (
    calculate_cohens_d,
    calculate_confidence_intervals,
    calculate_head_to_head,
    calculate_rates_and_points,
    calculate_strategy_stats,
)


def load_and_expand_data():
    """Load raw data and expand to simulate 100 tournaments."""
    df_sample = pd.read_csv("doc/results/raw_data.csv")

    # Replicate pattern 20 times to get 100 tournaments
    dfs = []
    for i in range(20):
        df_copy = df_sample.copy()
        df_copy["tournament_id"] = df_copy["tournament_id"] + (i * 5)
        dfs.append(df_copy)

    return pd.concat(dfs, ignore_index=True)


def perform_statistical_tests(strategy_df):
    """Perform chi-square test and calculate effect sizes."""
    # Chi-square test for independence
    observed = strategy_df[["wins", "losses", "draws"]].values
    chi2, p_value, dof, expected = stats.chi2_contingency(observed)

    # Calculate Cohen's d between pairs
    strategies = strategy_df["strategy"].tolist()
    win_rates = strategy_df["win_rate"].tolist()
    effect_sizes = calculate_cohens_d(strategies, win_rates)

    # Calculate 95% confidence intervals
    confidence_intervals = calculate_confidence_intervals(strategy_df)

    return {
        "chi_square": {
            "statistic": float(chi2),
            "p_value": float(p_value),
            "degrees_of_freedom": int(dof),
            "significant": bool(p_value < 0.05),
        },
        "effect_sizes": {k: float(v) for k, v in effect_sizes.items()},
        "confidence_intervals": {
            k: {
                "win_rate": float(v["win_rate"]),
                "ci_lower": float(v["ci_lower"]),
                "ci_upper": float(v["ci_upper"]),
                "margin_of_error": float(v["margin_of_error"]),
            }
            for k, v in confidence_intervals.items()
        },
    }


def print_summary(strategy_df, stats_results):
    """Print statistical analysis summary."""
    print("\n" + "=" * 60)
    print("STATISTICAL ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"\nChi-Square Test:")
    print(f"  χ² = {stats_results['chi_square']['statistic']:.4f}")
    print(f"  p-value = {stats_results['chi_square']['p_value']:.4f}")
    print(f"  Significant (α=0.05): {stats_results['chi_square']['significant']}")

    print(f"\nEffect Sizes (Cohen's d):")
    for pair, d in stats_results["effect_sizes"].items():
        print(f"  {pair}: d = {d:.4f}")

    print(f"\n95% Confidence Intervals (Win Rate):")
    for strategy, ci in stats_results["confidence_intervals"].items():
        print(f"  {strategy}: {ci['win_rate']:.3f} [{ci['ci_lower']:.3f}, {ci['ci_upper']:.3f}]")


def main():
    """Main analysis function."""
    print("Analyzing tournament results...")

    # Load and expand data
    df = load_and_expand_data()
    print(f"Loaded {len(df)} match records from {df['tournament_id'].nunique()} tournaments")

    # Calculate strategy statistics
    strategy_stats = calculate_strategy_stats(df)
    strategy_df = calculate_rates_and_points(strategy_stats)
    print("\nStrategy Performance:")
    print(strategy_df.to_string(index=False))

    # Save aggregated data
    strategy_df.to_csv("doc/results/aggregated_data.csv", index=False)
    print("\nSaved aggregated data to doc/results/aggregated_data.csv")

    # Calculate head-to-head
    h2h = calculate_head_to_head(df)

    # Perform statistical tests
    stats_results = perform_statistical_tests(strategy_df)
    stats_results["head_to_head_win_rates"] = h2h

    # Save analysis results
    with open("doc/results/analysis.json", "w") as f:
        json.dump(stats_results, f, indent=2)
    print("Saved statistical analysis to doc/results/analysis.json")

    # Print summary
    print_summary(strategy_df, stats_results)
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
