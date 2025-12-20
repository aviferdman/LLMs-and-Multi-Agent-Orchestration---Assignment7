"""Match card component."""

from typing import Dict

import streamlit as st

from gui.config import COLORS, STATUS_ICONS


def render_match_card(match: Dict, show_details: bool = False):
    """Render a match card for even/odd game."""
    match_id = match.get("match_id", "Unknown")
    status = match.get("status", "unknown")
    player1_id = match.get("player1_id", "Player 1")
    player2_id = match.get("player2_id", "Player 2")
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
    status_icon = STATUS_ICONS.get(status, "❓")
    status_text = status.replace("_", " ").title()

    # Determine result display
    if status == "completed":
        if winner_id:
            result = f"<div style='color:#4CAF50;font-weight:bold;margin-top:0.5rem;'>🎉 Winner: {winner_id}</div>"
        else:
            result = "<div style='color:#FFC107;font-weight:bold;margin-top:0.5rem;'>🤝 Draw</div>"
    else:
        result = ""

    st.markdown(
        f"""
        <div style="border: 2px solid {status_color}; border-radius: 10px; padding: 1rem;
                    margin: 0.5rem 0; background-color: rgba(255, 255, 255, 0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div><strong>Round {round_number}</strong> | {status_icon} {status_text}</div>
                <div style="font-size: 0.9em; color: #888;">{match_id}</div>
            </div>
            <div style="margin-top: 1rem; font-size: 1.2em; text-align:center;">
                <strong>{player1_id}</strong> vs <strong>{player2_id}</strong>
            </div>
            {result}
        </div>
        """,
        unsafe_allow_html=True,
    )
