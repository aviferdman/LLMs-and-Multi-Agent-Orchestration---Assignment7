#!/usr/bin/env python3
"""Create visualizations for strategy performance analysis."""

import json

import matplotlib.pyplot as plt
import pandas as pd

from visualization_utils import create_boxplot, create_heatmap, create_win_rate_chart, setup_plot_style

setup_plot_style()

# Load data
strategy_df = pd.read_csv("doc/results/aggregated_data.csv")
with open("doc/results/analysis.json", "r") as f:
    analysis = json.load(f)

strategies = strategy_df["strategy"].tolist()
win_rates = strategy_df["win_rate"].tolist()

# Visualization 1: Win Rates by Strategy (Bar Chart)
fig, ax = plt.subplots(figsize=(10, 6))
create_win_rate_chart(ax, strategies, win_rates, analysis["confidence_intervals"])
plt.tight_layout()
plt.savefig("doc/results/win_rates_by_strategy.png", dpi=300, bbox_inches="tight")
print("Saved: doc/results/win_rates_by_strategy.png")
plt.close()

# Visualization 2: Score Distribution (Box Plot)
fig, ax = plt.subplots(figsize=(10, 6))
plot_data = []
for strategy in strategies:
    row = strategy_df[strategy_df["strategy"] == strategy].iloc[0]
    values = ([3] * row["wins"]) + ([0] * row["losses"]) + ([1] * row["draws"])
    plot_data.append(values)
create_boxplot(ax, plot_data, strategies)
plt.tight_layout()
plt.savefig("doc/results/score_distribution.png", dpi=300, bbox_inches="tight")
print("Saved: doc/results/score_distribution.png")
plt.close()

# Visualization 3: Head-to-Head Heatmap
fig, ax = plt.subplots(figsize=(8, 6))
h2h = analysis["head_to_head_win_rates"]
matrix = []
for s1 in strategies:
    row = []
    for s2 in strategies:
        if s1 == s2:
            row.append(0.5)
        elif s2 in h2h.get(s1, {}):
            row.append(h2h[s1][s2])
        else:
            row.append(0.0)
    matrix.append(row)
create_heatmap(ax, matrix, strategies)
plt.tight_layout()
plt.savefig("doc/results/head_to_head_heatmap.png", dpi=300, bbox_inches="tight")
print("Saved: doc/results/head_to_head_heatmap.png")
plt.close()

print("\nAll visualizations created successfully!")
print(f"- Win rates: Random={win_rates[strategies.index('Random')]:.1%}, "
      f"Frequency={win_rates[strategies.index('Frequency')]:.1%}, "
      f"Pattern={win_rates[strategies.index('Pattern')]:.1%}")
