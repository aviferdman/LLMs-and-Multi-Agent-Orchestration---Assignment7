"""League Launcher page for starting new leagues."""

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

with st.form("league_config_form"):
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

        # Player count configuration
        min_players = game_details.get("min_players", 2)
        max_players = game_details.get("max_players", 8)

        num_players = st.slider(
            "Number of Players",
            min_value=min_players,
            max_value=max_players,
            value=min_players,
            help=f"Select between {min_players} and {max_players} players",
        )

    # League name
    league_name = st.text_input(
        "League Name (Optional)",
        placeholder="e.g., 'Spring Championship 2025'",
        help="Custom name for your league",
    )

    # Submit button
    submit = st.form_submit_button("🚀 Launch League", type="primary", use_container_width=True)

    if submit:
        with st.spinner("Launching league..."):
            result = api_client.start_league(
                game_id=selected_game_id,
                num_players=num_players,
                league_name=league_name if league_name else None,
            )

            if result and result.get("success"):
                st.success(f"🎉 {result.get('message', 'League started successfully!')}")
                st.balloons()
                st.info("Navigate to the **Live** page to watch matches in real-time!")

                # Auto-navigate to live page after 2 seconds
                st.markdown("Redirecting to Live page in 2 seconds...")
            else:
                st.error("Failed to start league. Please check the logs and try again.")
