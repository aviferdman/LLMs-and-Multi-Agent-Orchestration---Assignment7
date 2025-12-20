"""Main dashboard for the AI Agent League GUI."""

import streamlit as st

from gui.api_client import get_api_client
from gui.components.header import render_header
from gui.components.match_card import render_match_card
from gui.components.standings_table import render_standings_table
from gui.config import PAGE_ICON, PAGE_TITLE, REFRESH_INTERVAL_DASHBOARD

# Page configuration
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# Render header
render_header("Dashboard")

# Title
st.title("📊 League Dashboard")
st.markdown("Overview of the current league status and standings.")

# API client
api_client = get_api_client()

# Auto-refresh
if st.button("🔄 Refresh", type="secondary"):
    st.rerun()

# League status
st.markdown("---")
st.subheader("🏆 League Status")

league_status = api_client.get_league_status()

if league_status:
    status = league_status.get("status", "unknown")
    game_type = league_status.get("game_type", "Unknown")
    current_round = league_status.get("current_round", 0)
    total_rounds = league_status.get("total_rounds", 0)
    matches_completed = league_status.get("matches_completed", 0)
    matches_total = league_status.get("matches_total", 0)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        status_emoji = {
            "not_started": "⏸️",
            "registering": "📝",
            "in_progress": "⚡",
            "completed": "🏁",
            "paused": "⏸️",
        }.get(status, "❓")
        st.metric("Status", f"{status_emoji} {status.replace('_', ' ').title()}")

    with col2:
        st.metric("Game Type", game_type.replace("_", " ").title())

    with col3:
        st.metric("Round Progress", f"{current_round} / {total_rounds}")

    with col4:
        st.metric("Matches", f"{matches_completed} / {matches_total}")

    # Progress bar
    if matches_total > 0:
        progress = matches_completed / matches_total
        st.progress(progress, text=f"Overall Progress: {progress:.1%}")
else:
    st.warning("No league data available. Start a new league from the Launcher page.")

# Current standings
st.markdown("---")
st.subheader("🏅 Current Standings")

standings_data = api_client.get_standings()

if standings_data:
    standings = standings_data.get("standings", [])
    if standings:
        render_standings_table(standings, show_medals=True)
    else:
        st.info("No standings available yet.")
else:
    st.info("No standings data available.")

# Recent matches
st.markdown("---")
st.subheader("🎮 Recent Matches")

matches = api_client.list_matches()

if matches:
    # Show last 5 matches (handle None values)
    recent_matches = sorted(matches, key=lambda x: x.get("started_at") or "", reverse=True)[:5]

    if recent_matches:
        for match in recent_matches:
            render_match_card(match, show_details=False)
    else:
        st.info("No matches played yet.")
else:
    st.info("No match data available.")

# Quick actions
st.markdown("---")
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 Launch New League", use_container_width=True, type="primary"):
        st.switch_page("pages/launcher.py")

with col2:
    if st.button("⚡ Watch Live Matches", use_container_width=True):
        st.switch_page("pages/live.py")

with col3:
    if st.button("🏅 View Full Standings", use_container_width=True):
        st.switch_page("pages/standings.py")

# Footer
st.markdown("---")
st.caption(
    f"Auto-refresh every {REFRESH_INTERVAL_DASHBOARD} seconds. Click the Refresh button for manual updates."
)
