"""Live match viewing page with real-time updates."""

import time

import streamlit as st

from gui.api_client import get_api_client
from gui.components.header import render_header
from gui.components.live_match_panel import render_live_match_panel
from gui.config import PAGE_ICON, PAGE_TITLE, REFRESH_INTERVAL_LIVE

# Page configuration
st.set_page_config(page_title=f"{PAGE_TITLE} - Live", page_icon=PAGE_ICON, layout="wide")

# Render header
render_header("Live")

# Title
st.title("⚡ Live Match View")
st.markdown("Watch matches in real-time with live player status updates.")

# API client
api_client = get_api_client()

# Auto-refresh toggle
auto_refresh = st.toggle(
    "Auto-refresh", value=True, help=f"Refresh every {REFRESH_INTERVAL_LIVE} seconds"
)

# Manual refresh button
if st.button("🔄 Refresh Now", type="secondary"):
    st.rerun()

# Fetch active matches
matches = api_client.list_matches(status="in_progress")

if not matches:
    # Also check for scheduled matches
    matches = api_client.list_matches(status="scheduled")

if matches:
    # Match selector
    st.markdown("---")
    st.subheader("🎮 Select Match")

    match_options = {
        match[
            "match_id"
        ]: f"Round {match['round_number']}: {match['player1_id']} vs {match['player2_id']}"
        for match in matches
    }

    selected_match_id = st.selectbox(
        "Match",
        options=list(match_options.keys()),
        format_func=lambda x: match_options[x],
        label_visibility="collapsed",
    )

    # Get full match details
    selected_match = api_client.get_match(selected_match_id)

    if selected_match:
        st.markdown("---")

        # Render live match panel
        render_live_match_panel(selected_match)

        # Match info
        with st.expander("ℹ️ Match Information"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"**Match ID:** `{selected_match.get('match_id', 'N/A')}`")

            with col2:
                st.markdown(f"**Round:** {selected_match.get('round_number', 'N/A')}")

            with col3:
                status = selected_match.get("status", "unknown")
                st.markdown(f"**Status:** {status.replace('_', ' ').title()}")

            if selected_match.get("referee_id"):
                st.markdown(f"**Referee:** {selected_match['referee_id']}")

            if selected_match.get("started_at"):
                st.markdown(f"**Started:** {selected_match['started_at']}")

    else:
        st.error("Failed to load match details.")

else:
    st.info("No active or scheduled matches found. Start a new league from the Launcher page.")

    # Quick action button
    if st.button("🚀 Launch New League", type="primary", use_container_width=True):
        st.switch_page("pages/launcher.py")

# Auto-refresh implementation
if auto_refresh and matches:
    with st.empty():
        st.caption(f"Auto-refreshing in {REFRESH_INTERVAL_LIVE} seconds...")
        time.sleep(REFRESH_INTERVAL_LIVE)
        st.rerun()

# Footer
st.markdown("---")
st.caption(
    "Live updates refresh automatically. Player status shows: ⏳ Waiting | 🤔 Thinking | ✅ Submitted"
)
