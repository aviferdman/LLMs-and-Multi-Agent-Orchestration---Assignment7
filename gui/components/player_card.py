"""Player card component."""

from typing import Dict

import streamlit as st

from gui.config import COLORS


def render_player_card(player: Dict, show_stats: bool = True):
    """Render a player card with stats."""
    player_id = player.get("player_id", "Unknown")
    wins = player.get("wins", 0)
    losses = player.get("losses", 0)
    draws = player.get("draws", 0)
    games_played = player.get("games_played", 0)
    win_rate = player.get("win_rate", 0.0)
    is_active = player.get("is_active", False)

    # Status indicator
    status_color = COLORS["success"] if is_active else COLORS["waiting"]
    status_text = "Active" if is_active else "Inactive"

    # Create player card
    st.markdown(
        f"""
        <div style="border: 2px solid {status_color};
                    border-radius: 10px;
                    padding: 1rem;
                    background: linear-gradient(135deg, rgba(31, 119, 180, 0.1), rgba(44, 160, 44, 0.1));">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0;">👤 {player_id}</h3>
                <span style="background-color: {status_color};
                             color: white;
                             padding: 0.25rem 0.5rem;
                             border-radius: 5px;
                             font-size: 0.85em;">
                    {status_text}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Display stats if requested
    if show_stats:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Games", games_played)

        with col2:
            st.metric("Wins", wins, delta=None)

        with col3:
            st.metric("Losses", losses, delta=None)

        with col4:
            st.metric("Win Rate", f"{win_rate:.1%}")

        # Win/Loss/Draw breakdown
        if games_played > 0:
            st.markdown("**Record Breakdown:**")
            record_text = f"🟢 {wins} Wins | 🔴 {losses} Losses | 🟡 {draws} Draws"
            st.markdown(record_text)
