"""Standings table component."""

from typing import Dict, List

import pandas as pd
import streamlit as st

from gui.config import MEDALS


def render_standings_table(standings: List[Dict], show_medals: bool = True):
    """Render a standings table with rankings."""
    if not standings:
        st.info("No standings data available yet.")
        return

    # Create DataFrame
    df = pd.DataFrame(standings)

    # Add medal column for top 3
    if show_medals and "rank" in df.columns:
        df["Medal"] = df["rank"].apply(lambda x: MEDALS.get(x, ""))
        cols = ["Medal", "rank", "player_id", "wins", "losses", "draws", "points"]
    else:
        cols = ["rank", "player_id", "wins", "losses", "draws", "points"]

    # Filter to existing columns
    display_cols = [c for c in cols if c in df.columns]
    df_display = df[display_cols].copy()

    # Rename columns for display
    column_config = {
        "Medal": st.column_config.TextColumn("", width="small"),
        "rank": st.column_config.NumberColumn("Rank", width="small"),
        "player_id": st.column_config.TextColumn("Player", width="medium"),
        "wins": st.column_config.NumberColumn("Wins", width="small"),
        "losses": st.column_config.NumberColumn("Losses", width="small"),
        "draws": st.column_config.NumberColumn("Draws", width="small"),
        "points": st.column_config.NumberColumn("Points", width="small"),
        "games_played": st.column_config.NumberColumn("Games", width="small"),
    }

    # Display table
    st.dataframe(
        df_display,
        column_config=column_config,
        hide_index=True,
        use_container_width=True,
    )

    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Players", len(standings))
    with col2:
        total_matches = df["games_played"].sum() // 2 if "games_played" in df.columns else 0
        st.metric("Total Matches", int(total_matches))
    with col3:
        leader = standings[0] if standings else None
        leader_name = leader.get("player_id", "N/A") if leader else "N/A"
        st.metric("Leader", leader_name)
    with col4:
        leader_points = leader.get("points", 0) if leader else 0
        st.metric("Top Score", leader_points)
