"""Match history display component."""

import streamlit as st


def render_match_entry(match_entry: dict) -> None:
    """Render a single match history entry."""
    match_id = match_entry.get("match_id")
    opponent_id = match_entry.get("opponent_id", "Unknown")
    result = match_entry.get("result", "unknown")
    player_score = match_entry.get("player_score", 0)
    opponent_score = match_entry.get("opponent_score", 0)
    played_at = match_entry.get("played_at", "N/A")

    result_emoji = {"win": "🎉", "loss": "😔", "draw": "🤝"}.get(result, "❓")
    result_color = {"win": "#2ca02c", "loss": "#d62728", "draw": "#ff7f0e"}.get(result, "#888888")

    st.markdown(
        f"""
        <div style="border-left: 4px solid {result_color};
                    padding: 0.5rem 1rem;
                    margin: 0.5rem 0;
                    background-color: rgba(255, 255, 255, 0.05);">
            <strong>{result_emoji} {result.upper()}</strong> vs {opponent_id}
            <br>Score: {player_score} - {opponent_score}
            <br><small>Match ID: {match_id} | Played: {played_at}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_match_history(match_history: dict, max_matches: int = 10) -> None:
    """Render match history for a player."""
    if not match_history or not match_history.get("matches"):
        st.info("No match history available for this player.")
        return

    matches = match_history.get("matches", [])
    st.markdown(f"**Total Matches:** {match_history.get('total_matches', 0)}")

    for match_entry in matches[:max_matches]:
        render_match_entry(match_entry)
