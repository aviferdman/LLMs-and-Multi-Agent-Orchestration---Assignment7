"""Visualization helper functions for strategy analysis charts."""

import matplotlib.pyplot as plt
import seaborn as sns


def setup_plot_style():
    """Configure matplotlib style for consistent charts."""
    sns.set_style("whitegrid")
    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["font.size"] = 10


def create_win_rate_chart(ax, strategies, win_rates, ci_data):
    """Create bar chart with confidence intervals."""
    colors = ["#3498db", "#e74c3c", "#2ecc71"]
    bars = ax.bar(strategies, win_rates, color=colors, alpha=0.8, edgecolor="black", linewidth=1.5)
    errors = [
        [ci_data[s]["win_rate"] - ci_data[s]["ci_lower"] for s in strategies],
        [ci_data[s]["ci_upper"] - ci_data[s]["win_rate"] for s in strategies],
    ]
    ax.errorbar(strategies, win_rates, yerr=errors, fmt="none", ecolor="black", capsize=5, capthick=2, linewidth=2)
    for bar, rate in zip(bars, win_rates):
        ax.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height() + 0.01, f"{rate:.1%}", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_ylabel("Win Rate", fontsize=12, fontweight="bold")
    ax.set_xlabel("Strategy", fontsize=12, fontweight="bold")
    ax.set_title("Strategy Performance Comparison (100 Tournaments)\nWith 95% Confidence Intervals", fontsize=14, fontweight="bold", pad=20)
    ax.set_ylim(0, 0.5)
    ax.axhline(y=0.333, color="red", linestyle="--", linewidth=2, alpha=0.7, label="Random Baseline (33.3%)")
    ax.legend(fontsize=10)


def create_boxplot(ax, plot_data, strategies):
    """Create box plot for score distribution."""
    ax.boxplot(
        plot_data, labels=strategies, patch_artist=True,
        medianprops=dict(color="red", linewidth=2),
        boxprops=dict(facecolor="lightblue", alpha=0.7, edgecolor="black", linewidth=1.5),
        whiskerprops=dict(color="black", linewidth=1.5),
        capprops=dict(color="black", linewidth=1.5),
    )
    ax.set_ylabel("Points per Match", fontsize=12, fontweight="bold")
    ax.set_xlabel("Strategy", fontsize=12, fontweight="bold")
    ax.set_title("Score Distribution by Strategy (100 Tournaments)", fontsize=14, fontweight="bold", pad=20)
    ax.grid(True, alpha=0.3)


def create_heatmap(ax, matrix, strategies):
    """Create head-to-head heatmap."""
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(len(strategies)))
    ax.set_yticks(range(len(strategies)))
    ax.set_xticklabels(strategies, fontsize=11)
    ax.set_yticklabels(strategies, fontsize=11)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Win Rate", fontsize=11, fontweight="bold")
    for i in range(len(strategies)):
        for j in range(len(strategies)):
            if i != j:
                ax.text(j, i, f"{matrix[i][j]:.2f}", ha="center", va="center", color="black", fontweight="bold", fontsize=10)
    ax.set_title("Head-to-Head Win Rates\n(Row vs Column)", fontsize=14, fontweight="bold", pad=20)
    ax.set_xlabel("Opponent Strategy", fontsize=12, fontweight="bold")
    ax.set_ylabel("Strategy", fontsize=12, fontweight="bold")
    return im
