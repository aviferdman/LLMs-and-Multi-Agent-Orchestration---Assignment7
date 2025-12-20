"""League Launcher page for starting new leagues."""

import time
import streamlit as st

from gui.api_client import get_api_client
from gui.components.header import render_header
from gui.config import PAGE_ICON, PAGE_TITLE

# Page configuration
st.set_page_config(page_title=f"{PAGE_TITLE} - Launcher", page_icon=PAGE_ICON, layout="wide")

# Render header
render_header("Launcher")

# Title
st.title("🚀 League Launcher")
st.markdown("Configure and launch a new AI agent league competition.")

# API client
api_client = get_api_client()

# Initialize session state
if "league_launched" not in st.session_state:
    st.session_state.league_launched = False

# Redirect to Live page if league was just launched
if st.session_state.league_launched:
    st.session_state.league_launched = False
    st.switch_page("pages/live.py")

# Check agent status
with st.expander("🤖 Agent Status", expanded=False):
    agents_status = api_client.get_agents_status()
    if agents_status:
        all_ready = agents_status.get("all_ready", False)
        message = agents_status.get("message", "")

        if all_ready:
            st.success(f"✅ {message}")
        else:
            st.warning(f"⚠️ {message}")

        # Player agents
        st.markdown("**Players:**")
        players = agents_status.get("players", [])
        if players:
            for player in players:
                status_icon = "✅" if player.get("is_ready") else "❌"
                st.markdown(f"- {status_icon} {player.get('agent_id', 'Unknown')}")
        else:
            st.info("No players registered yet.")

        # Referee agents
        st.markdown("**Referees:**")
        referees = agents_status.get("referees", [])
        if referees:
            for referee in referees:
                status_icon = "✅" if referee.get("is_ready") else "❌"
                st.markdown(f"- {status_icon} {referee.get('agent_id', 'Unknown')}")
        else:
            st.info("No referees registered yet.")

# Configuration form
st.markdown("---")
st.subheader("⚙️ League Configuration")

# Fetch available games
games = api_client.list_games()

if not games:
    st.error("No games available. Please check the API connection.")
    st.stop()

# Game selection
game_options = {game["game_id"]: game["name"] for game in games}
selected_game_id = st.selectbox(
    "Select Game",
    options=list(game_options.keys()),
    format_func=lambda x: game_options[x],
    help="Choose the game type for this league",
)

# Get game details
game_details = api_client.get_game(selected_game_id)

if game_details:
    st.info(f"**{game_details['name']}**: {game_details['description']}")

    # Show game rules
    with st.expander("📖 Game Rules"):
        rules = game_details.get("rules", "No rules available.")
        st.markdown(rules)

# Player count - currently only 4 players is supported
st.markdown("**Number of Players:** 4 (fixed)")
st.caption("⚠️ Currently only 4-player leagues are supported.")
num_players = 4

# League name - Get existing leagues for validation
existing_leagues_data = api_client.list_leagues()
existing_leagues = existing_leagues_data.get("leagues", []) if existing_leagues_data else []

league_name = st.text_input(
    "League Name *",
    placeholder="e.g., 'Spring Championship 2025'",
    help="Custom name for your league (must be unique)",
    key="league_name_input",
)

# Validation messages
if league_name:
    # Generate the league ID that will be created
    league_id = league_name.lower().replace(" ", "_")
    if league_id in existing_leagues:
        st.error(f"❌ League name '{league_name}' already exists. Please choose a unique name.")
    else:
        st.success(f"✅ League name is unique")
else:
    st.warning("⚠️ League name is required")

# Launch button
if st.button("🚀 Launch League", type="primary", use_container_width=True):
    # Validate league name
    if not league_name or not league_name.strip():
        st.error("❌ Please provide a league name")
    else:
        league_id = league_name.lower().replace(" ", "_")
        if league_id in existing_leagues:
            st.error(f"❌ League name '{league_name}' already exists. Please choose a unique name.")
        else:
            with st.spinner("Launching league..."):
                result = api_client.start_league(
                    game_id=selected_game_id,
                    num_players=num_players,
                    league_name=league_name,
                )

                if result and result.get("success"):
                    st.success(f"🎉 {result.get('message', 'League started successfully!')}")
                    st.balloons()
                    st.info("Redirecting to Live page...")
                    time.sleep(2)
                    st.session_state.league_launched = True
                    st.rerun()
                else:
                    error_msg = result.get("message", "Unknown error") if result else "No response from API"
                    st.error(f"Failed to start league: {error_msg}")
