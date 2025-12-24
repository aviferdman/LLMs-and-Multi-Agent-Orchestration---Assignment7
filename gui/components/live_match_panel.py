"""Live match panel component for real-time match display."""

from typing import Dict, Optional

import streamlit as st

from gui.config import COLORS, STATUS_ICONS


def render_live_match_panel(match: Dict):
    """Render a live match panel with two-player display."""
    player1_id = match.get("player1_id", "Player 1")
    player2_id = match.get("player2_id", "Player 2")
    player1_score = match.get("player1_score", 0)
    player2_score = match.get("player2_score", 0)
    current_round = match.get("current_round", 1)
    total_rounds = match.get("total_rounds", 5)
    status = match.get("status", "unknown")

    # Player statuses (if live state available)
    player1_status = match.get("player1_status", "waiting")
    player2_status = match.get("player2_status", "waiting")
    player1_move = match.get("player1_move")
    player2_move = match.get("player2_move")

    # Match header
    st.markdown(f"### Round {current_round} of {total_rounds}")

    # Progress bar
    progress = (current_round - 1) / total_rounds if total_rounds > 0 else 0
    st.progress(progress)

    # Two-column layout for players
    col1, col2 = st.columns(2)

    with col1:
        _render_player_panel(player1_id, player1_score, player1_status, player1_move, "left")

    with col2:
        _render_player_panel(player2_id, player2_score, player2_status, player2_move, "right")

    # Round history
    if "rounds_played" in match and match["rounds_played"]:
        st.markdown("---")
        st.markdown("### Round History")
        _render_round_history(match["rounds_played"])


def _render_player_panel(
    player_id: str,
    score: int,
    status: str,
    move: Optional[str],
    side: str,
):
    """Render individual player panel."""
    status_icon = STATUS_ICONS.get(status, "❓")
    status_text = status.replace("_", " ").title()

    # Status color
    status_color_map = {
        "waiting": COLORS["waiting"],
        "thinking": COLORS["thinking"],
        "submitted": COLORS["submitted"],
    }
    status_color = status_color_map.get(status, COLORS["light"])

    # Player panel
    st.markdown(
        f"""
        <div style="border: 3px solid {status_color};
                    border-radius: 15px;
                    padding: 1.5rem;
                    text-align: center;
                    background: linear-gradient(135deg, rgba(31, 119, 180, 0.1), rgba(255, 127, 14, 0.1));">
            <h2 style="margin: 0;">👤 {player_id}</h2>
            <h1 style="color: {status_color}; margin: 0.5rem 0;">
                {status_icon} {status_text}
            </h1>
            <div style="font-size: 3em; font-weight: bold; margin: 1rem 0;">
                {score}
            </div>
            <div style="font-size: 0.9em; color: #888;">
                Score
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Show move if submitted
    if move and status == "submitted":
        st.markdown(f"**Move:** `{move}`")
    elif status == "thinking":
        st.markdown("*Thinking...*")


def _render_round_history(rounds: list):
    """Render round history table."""
    if not rounds:
        st.info("No rounds completed yet.")
        return

    for i, round_data in enumerate(reversed(rounds[-5:]), 1):
        round_num = round_data.get("round_number", "?")
        p1_move = round_data.get("player1_move", "?")
        p2_move = round_data.get("player2_move", "?")
        winner = round_data.get("winner", "Draw")

        col1, col2, col3, col4 = st.columns([1, 2, 2, 2])

        with col1:
            st.markdown(f"**R{round_num}**")
        with col2:
            st.markdown(f"`{p1_move}`")
        with col3:
            st.markdown(f"`{p2_move}`")
        with col4:
            winner_icon = STATUS_ICONS.get("win", "🏆")
            st.markdown(f"{winner_icon} {winner}")
