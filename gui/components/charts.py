"""Chart components for data visualization."""

from typing import Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from gui.config import COLORS


def render_charts(standings: List[Dict]):
    """Render interactive charts for standings data."""
    if not standings:
        st.info("No data available for charts.")
        return

    df = pd.DataFrame(standings)

    # Bar chart for points
    st.subheader("Points Distribution")
    fig_bar = px.bar(
        df,
        x="player_id",
        y="points",
        color="points",
        color_continuous_scale=["#d62728", "#ff7f0e", "#2ca02c"],
        title="Player Points Comparison",
        labels={"player_id": "Player", "points": "Points"},
    )
    fig_bar.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Player",
        yaxis_title="Points",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Pie chart for win distribution
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Win Distribution")
        if "wins" in df.columns and df["wins"].sum() > 0:
            fig_pie = px.pie(
                df,
                names="player_id",
                values="wins",
                title="Wins by Player",
                color_discrete_sequence=px.colors.qualitative.Set3,
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No wins recorded yet.")

    with col2:
        st.subheader("Win Rate Comparison")
        if "win_rate" in df.columns:
            fig_winrate = go.Figure()
            fig_winrate.add_trace(
                go.Bar(
                    x=df["player_id"],
                    y=df["win_rate"] * 100,
                    marker_color=COLORS["success"],
                    text=[f"{wr:.1f}%" for wr in df["win_rate"] * 100],
                    textposition="auto",
                )
            )
            fig_winrate.update_layout(
                title="Win Rate (%)",
                xaxis_title="Player",
                yaxis_title="Win Rate (%)",
                showlegend=False,
                height=400,
            )
            st.plotly_chart(fig_winrate, use_container_width=True)
        else:
            st.info("No win rate data available.")
