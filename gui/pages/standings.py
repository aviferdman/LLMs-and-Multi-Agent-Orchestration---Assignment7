"""Standings page with rankings and interactive charts."""

import streamlit as st

from gui.api_client import get_api_client
from gui.components.charts import render_charts
from gui.components.header import render_header
from gui.components.standings_table import render_standings_table
from gui.config import PAGE_ICON, PAGE_TITLE

# Page configuration
st.set_page_config(page_title=f"{PAGE_TITLE} - Standings", page_icon=PAGE_ICON, layout="wide")

# Render header
render_header("Standings")

# Title
st.title("🏅 League Standings")
st.markdown("Current rankings and player statistics.")

# API client
api_client = get_api_client()

# Refresh button
if st.button("🔄 Refresh", type="secondary"):
    st.rerun()

# Fetch standings
standings_data = api_client.get_standings()

if standings_data:
    standings = standings_data.get("standings", [])
    last_updated = standings_data.get("last_updated")

    if standings:
        # Last updated info
        if last_updated:
            st.caption(f"Last updated: {last_updated}")

        st.markdown("---")

        # Rankings table
        st.subheader("📊 Rankings Table")
        render_standings_table(standings, show_medals=True)

        st.markdown("---")

        # Interactive charts
        st.subheader("📈 Performance Analytics")
        render_charts(standings)

        # Detailed statistics
        st.markdown("---")
        st.subheader("📋 Detailed Statistics")

        # Sort options
        sort_options = {
            "rank": "Rank",
            "points": "Points",
            "wins": "Wins",
            "win_rate": "Win Rate",
            "games_played": "Games Played",
        }

        sort_by = st.selectbox(
            "Sort by",
            options=list(sort_options.keys()),
            format_func=lambda x: sort_options[x],
        )

        # Sort standings
        if sort_by == "rank":
            sorted_standings = sorted(standings, key=lambda x: x.get("rank", 999))
        elif sort_by == "win_rate":
            sorted_standings = sorted(
                standings,
                key=lambda x: (
                    x.get("wins", 0) / x.get("games_played", 1)
                    if x.get("games_played", 0) > 0
                    else 0
                ),
                reverse=True,
            )
        else:
            sorted_standings = sorted(standings, key=lambda x: x.get(sort_by, 0), reverse=True)

        # Display detailed stats
        for player in sorted_standings:
            with st.expander(
                f"**{player.get('player_id', 'Unknown')}** - Rank #{player.get('rank', 'N/A')}"
            ):
                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    st.metric("Points", player.get("points", 0))

                with col2:
                    st.metric("Wins", player.get("wins", 0))

                with col3:
                    st.metric("Losses", player.get("losses", 0))

                with col4:
                    st.metric("Draws", player.get("draws", 0))

                with col5:
                    games = player.get("games_played", 0)
                    wins = player.get("wins", 0)
                    win_rate = (wins / games * 100) if games > 0 else 0
                    st.metric("Win Rate", f"{win_rate:.1f}%")

    else:
        st.info("No standings data available yet. Matches need to be completed first.")

else:
    st.warning("Unable to fetch standings. Please ensure the league is running.")

    # Quick action
    if st.button("🚀 Launch New League", type="primary", use_container_width=True):
        st.switch_page("pages/launcher.py")

# Footer
st.markdown("---")
st.caption("Standings are updated after each match completion.")
