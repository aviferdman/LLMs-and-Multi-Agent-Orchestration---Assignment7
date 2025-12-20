#!/usr/bin/env python3
"""Create visualizations for strategy performance analysis."""

import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["font.size"] = 10

# Load aggregated data
strategy_df = pd.read_csv("doc/results/aggregated_data.csv")

# Load analysis results
with open("doc/results/analysis.json", "r") as f:
    analysis = json.load(f)

# Visualization 1: Win Rates by Strategy (Bar Chart)
fig, ax = plt.subplots(figsize=(10, 6))

strategies = strategy_df["strategy"].tolist()
win_rates = strategy_df["win_rate"].tolist()
colors = ["#3498db", "#e74c3c", "#2ecc71"]

bars = ax.bar(strategies, win_rates, color=colors, alpha=0.8, edgecolor="black", linewidth=1.5)

# Add confidence intervals as error bars
ci_data = analysis["confidence_intervals"]
errors = [
    [ci_data[s]["win_rate"] - ci_data[s]["ci_lower"] for s in strategies],
    [ci_data[s]["ci_upper"] - ci_data[s]["win_rate"] for s in strategies],
]

ax.errorbar(
    strategies,
    win_rates,
    yerr=errors,
    fmt="none",
    ecolor="black",
    capsize=5,
    capthick=2,
    linewidth=2,
)

# Add value labels on bars
for bar, rate in zip(bars, win_rates):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.0,
        height + 0.01,
        f"{rate:.1%}",
        ha="center",
        va="bottom",
        fontweight="bold",
        fontsize=11,
    )

ax.set_ylabel("Win Rate", fontsize=12, fontweight="bold")
ax.set_xlabel("Strategy", fontsize=12, fontweight="bold")
ax.set_title(
    "Strategy Performance Comparison (100 Tournaments)\nWith 95% Confidence Intervals",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
ax.set_ylim(0, 0.5)
ax.axhline(
    y=0.333, color="red", linestyle="--", linewidth=2, alpha=0.7, label="Random Baseline (33.3%)"
)
ax.legend(fontsize=10)

plt.tight_layout()
plt.savefig("doc/results/win_rates_by_strategy.png", dpi=300, bbox_inches="tight")
print("Saved: doc/results/win_rates_by_strategy.png")
plt.close()

# Visualization 2: Score Distribution (Box Plot)
fig, ax = plt.subplots(figsize=(10, 6))

# Prepare data for box plot
plot_data = []
for strategy in strategies:
    wins = strategy_df[strategy_df["strategy"] == strategy]["wins"].values[0]
    losses = strategy_df[strategy_df["strategy"] == strategy]["losses"].values[0]
    draws = strategy_df[strategy_df["strategy"] == strategy]["draws"].values[0]

    # Create distribution (approximate)
    values = ([3] * wins) + ([0] * losses) + ([1] * draws)
    plot_data.append(values)

bp = ax.boxplot(
    plot_data,
    labels=strategies,
    patch_artist=True,
    medianprops=dict(color="red", linewidth=2),
    boxprops=dict(facecolor="lightblue", alpha=0.7, edgecolor="black", linewidth=1.5),
    whiskerprops=dict(color="black", linewidth=1.5),
    capprops=dict(color="black", linewidth=1.5),
)

ax.set_ylabel("Points per Match", fontsize=12, fontweight="bold")
ax.set_xlabel("Strategy", fontsize=12, fontweight="bold")
ax.set_title(
    "Score Distribution by Strategy (100 Tournaments)", fontsize=14, fontweight="bold", pad=20
)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("doc/results/score_distribution.png", dpi=300, bbox_inches="tight")
print("Saved: doc/results/score_distribution.png")
plt.close()

# Visualization 3: Head-to-Head Heatmap
fig, ax = plt.subplots(figsize=(8, 6))

h2h = analysis["head_to_head_win_rates"]

# Create matrix
matrix = []
for s1 in strategies:
    row = []
    for s2 in strategies:
        if s1 == s2:
            row.append(0.5)  # Same strategy
        elif s2 in h2h.get(s1, {}):
            row.append(h2h[s1][s2])
        else:
            row.append(0.0)
    matrix.append(row)

# Create heatmap
im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)

# Set ticks and labels
ax.set_xticks(range(len(strategies)))
ax.set_yticks(range(len(strategies)))
ax.set_xticklabels(strategies, fontsize=11)
ax.set_yticklabels(strategies, fontsize=11)

# Rotate x labels
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Win Rate", fontsize=11, fontweight="bold")

# Add text annotations
for i in range(len(strategies)):
    for j in range(len(strategies)):
        if i != j:
            text = ax.text(
                j,
                i,
                f"{matrix[i][j]:.2f}",
                ha="center",
                va="center",
                color="black",
                fontweight="bold",
                fontsize=10,
            )

ax.set_title("Head-to-Head Win Rates\n(Row vs Column)", fontsize=14, fontweight="bold", pad=20)
ax.set_xlabel("Opponent Strategy", fontsize=12, fontweight="bold")
ax.set_ylabel("Strategy", fontsize=12, fontweight="bold")

plt.tight_layout()
plt.savefig("doc/results/head_to_head_heatmap.png", dpi=300, bbox_inches="tight")
print("Saved: doc/results/head_to_head_heatmap.png")
plt.close()

print("\nAll visualizations created successfully!")
print(
    f"- Win rates: Random={win_rates[strategies.index('Random')]:.1%}, "
    f"Frequency={win_rates[strategies.index('Frequency')]:.1%}, "
    f"Pattern={win_rates[strategies.index('Pattern')]:.1%}"
)
