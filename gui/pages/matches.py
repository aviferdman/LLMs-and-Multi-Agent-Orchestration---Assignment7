"""Matches page for viewing match history and details."""

import streamlit as st

from gui.api_client import get_api_client
from gui.components.header import render_header
from gui.components.match_card import render_match_card
from gui.config import PAGE_ICON, PAGE_TITLE

# Page configuration
st.set_page_config(page_title=f"{PAGE_TITLE} - Matches", page_icon=PAGE_ICON, layout="wide")

# Render header
render_header("Matches")

# Title
st.title("🎮 Match History")
st.markdown("Browse all matches with filtering and detailed views.")

# API client
api_client = get_api_client()

# Refresh button
if st.button("🔄 Refresh", type="secondary"):
    st.rerun()

# Filters
st.markdown("---")
st.subheader("🔍 Filters")

col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox(
        "Status",
        options=["All", "Scheduled", "In Progress", "Completed", "Cancelled"],
    )

with col2:
    round_filter = st.number_input("Round (0 = All)", min_value=0, value=0, step=1)

with col3:
    # Fetch players for filter
    players = api_client.list_players()
    player_options = ["All"] + [p["player_id"] for p in players] if players else ["All"]
    player_filter = st.selectbox("Player", options=player_options)

# Apply filters
status_map = {
    "All": None,
    "Scheduled": "scheduled",
    "In Progress": "in_progress",
    "Completed": "completed",
    "Cancelled": "cancelled",
}

status_param = status_map.get(status_filter)
round_param = round_filter if round_filter > 0 else None

# Fetch matches
matches = api_client.list_matches(round_number=round_param, status=status_param)

if matches:
    # Filter by player if selected
    if player_filter != "All":
        matches = [
            m
            for m in matches
            if m.get("player1_id") == player_filter or m.get("player2_id") == player_filter
        ]

    st.markdown("---")
    st.subheader(f"📋 Match List ({len(matches)} matches)")

    # Sort options
    sort_by = st.radio(
        "Sort by",
        options=["Recent First", "Round Number", "Status"],
        horizontal=True,
    )

    # Sort matches (handle None values in sorting)
    if sort_by == "Recent First":
        sorted_matches = sorted(matches, key=lambda x: x.get("started_at") or "", reverse=True)
    elif sort_by == "Round Number":
        sorted_matches = sorted(matches, key=lambda x: x.get("round_number") or 0)
    else:
        sorted_matches = sorted(matches, key=lambda x: x.get("status") or "")

    # Display matches
    for match in sorted_matches:
        render_match_card(match, show_details=True)

    # Summary statistics
    st.markdown("---")
    st.subheader("📊 Match Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Matches", len(matches))

    with col2:
        completed = sum(1 for m in matches if m.get("status") == "completed")
        st.metric("Completed", completed)

    with col3:
        in_progress = sum(1 for m in matches if m.get("status") == "in_progress")
        st.metric("In Progress", in_progress)

    with col4:
        scheduled = sum(1 for m in matches if m.get("status") == "scheduled")
        st.metric("Scheduled", scheduled)

else:
    st.info(
        "No matches found with the current filters. Try adjusting your filters or start a new league."
    )

    # Quick action
    if st.button("🚀 Launch New League", type="primary", use_container_width=True):
        st.switch_page("pages/launcher.py")

# Footer
st.markdown("---")
st.caption(
    "Use filters to narrow down your search. Click on matches to view detailed round history."
)
