"""Match card component."""

from typing import Dict

import streamlit as st

from gui.config import COLORS, STATUS_ICONS


def render_match_card(match: Dict, show_details: bool = False):
    """Render a match card."""
    match_id = match.get("match_id", "Unknown")
    status = match.get("status", "unknown")
    player1_id = match.get("player1_id", "Player 1")
    player2_id = match.get("player2_id", "Player 2")
    player1_score = match.get("player1_score", 0)
    player2_score = match.get("player2_score", 0)
    round_number = match.get("round_number", 0)
    winner_id = match.get("winner_id")

    # Determine status color
    status_color_map = {
        "scheduled": COLORS["waiting"],
        "in_progress": COLORS["warning"],
        "completed": COLORS["completed"],
        "cancelled": COLORS["danger"],
    }
    status_color = status_color_map.get(status, COLORS["light"])

    # Status badge
    status_icon = STATUS_ICONS.get(status, "❓")
    status_text = status.replace("_", " ").title()

    # Create card
    st.markdown(
        f"""
        <div style="border: 2px solid {status_color};
                    border-radius: 10px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                    background-color: rgba(255, 255, 255, 0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>Round {round_number}</strong> | {status_icon} {status_text}
                </div>
                <div style="font-size: 0.9em; color: #888;">
                    {match_id}
                </div>
            </div>
            <div style="margin-top: 1rem; font-size: 1.2em;">
                <strong>{player1_id}</strong> {player1_score} - {player2_score} <strong>{player2_id}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Show details if requested
    if show_details and winner_id:
        winner_icon = STATUS_ICONS.get("win", "🏆")
        st.markdown(f"**Winner:** {winner_icon} {winner_id}")

    # Show rounds played if available
    if show_details and "rounds_played" in match and match["rounds_played"]:
        with st.expander("View Round History"):
            for round_data in match["rounds_played"]:
                round_num = round_data.get("round_number", "?")
                p1_move = round_data.get("player1_move", "?")
                p2_move = round_data.get("player2_move", "?")
                round_winner = round_data.get("winner", "Draw")
                st.markdown(
                    f"**Round {round_num}:** {p1_move} vs {p2_move} → Winner: {round_winner}"
                )
