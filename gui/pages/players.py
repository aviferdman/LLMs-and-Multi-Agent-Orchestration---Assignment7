"""Players page for viewing player profiles and statistics."""

import streamlit as st

from gui.api_client import get_api_client
from gui.components.header import render_header
from gui.components.match_history import render_match_history
from gui.components.player_card import render_player_card
from gui.config import PAGE_ICON, PAGE_TITLE

st.set_page_config(page_title=f"{PAGE_TITLE} - Players", page_icon=PAGE_ICON, layout="wide")
render_header("Players")

st.title("👥 Player Profiles")
st.markdown("View detailed player statistics and match history.")

api_client = get_api_client()

if st.button("🔄 Refresh", type="secondary"):
    st.rerun()

players = api_client.list_players()

if players:
    st.markdown("---")
    st.subheader(f"📋 All Players ({len(players)} total)")

    cols = st.columns(min(3, len(players)))
    for idx, player in enumerate(players):
        with cols[idx % 3]:
            render_player_card(player, show_stats=True)

    st.markdown("---")
    st.subheader("🔍 Player Details")

    player_options = {p["player_id"]: p["player_id"] for p in players}
    selected_player_id = st.selectbox(
        "Select a player to view details",
        options=list(player_options.keys()),
        format_func=lambda x: player_options[x],
    )

    player_details = api_client.get_player(selected_player_id)

    if player_details:
        st.markdown("---")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### 👤 {player_details.get('player_id', 'Unknown')}")

            is_active = player_details.get("is_active", False)
            is_registered = player_details.get("is_registered", False)

            badge_col1, badge_col2 = st.columns(2)
            with badge_col1:
                st.success("✅ Active") if is_active else st.warning("⏸️ Inactive")
            with badge_col2:
                st.success("✅ Registered") if is_registered else st.error("❌ Not Registered")

        with col2:
            games = player_details.get("games_played", 0)
            win_rate = player_details.get("win_rate", 0.0)

            st.metric("Games Played", games)
            st.metric("Win Rate", f"{win_rate:.1%}")

        st.markdown("---")
        st.subheader("📜 Match History")

        match_history = api_client.get_player_history(selected_player_id)
        render_match_history(match_history, max_matches=10)
    else:
        st.error("Failed to load player details.")
else:
    st.info("No players found. Players will appear here once the league is running.")
    if st.button("🚀 Launch New League", type="primary", use_container_width=True):
        st.switch_page("pages/launcher.py")

st.markdown("---")
st.caption("Player statistics update after each match completion.")
