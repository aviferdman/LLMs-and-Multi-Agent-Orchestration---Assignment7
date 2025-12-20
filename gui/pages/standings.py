"""Results page with standings, matches, and player statistics."""

import streamlit as st

from gui.api_client import get_api_client
from gui.components.charts import render_charts
from gui.components.header import render_header
from gui.components.match_card import render_match_card
from gui.components.standings_table import render_standings_table
from gui.config import PAGE_ICON, PAGE_TITLE

st.set_page_config(page_title=f"{PAGE_TITLE} - Results", page_icon=PAGE_ICON, layout="wide")
render_header("Results")

st.title("🏅 League Results")
api_client = get_api_client()

# League selector
leagues_data = api_client.list_leagues()
leagues = leagues_data.get("leagues", []) if leagues_data else []
default_league = leagues_data.get("default", "") if leagues_data else ""

if leagues:
    selected_league = st.selectbox("Select League", leagues, index=leagues.index(default_league) if default_league in leagues else 0)
else:
    selected_league = None
    st.warning("No leagues found. Launch a league first!")

if st.button("🔄 Refresh", type="secondary"):
    st.rerun()

if selected_league:
    tab_standings, tab_matches, tab_analytics = st.tabs(["📊 Standings", "🎮 Matches", "📈 Analytics"])

    with tab_standings:
        standings_data = api_client.get_standings(league_id=selected_league)
        if standings_data and (standings := standings_data.get("standings", [])):
            if last_upd := standings_data.get("last_updated"):
                st.caption(f"Last updated: {last_upd}")
            render_standings_table(standings, show_medals=True)
            st.markdown("---")
            st.subheader("👥 Player Details")
            for player in standings:
                pid, rank = player.get("player_id", "?"), player.get("rank", "?")
                pts, w, l, d = player.get("points", 0), player.get("wins", 0), player.get("losses", 0), player.get("draws", 0)
                games = player.get("games_played", 0)
                wr = (w / games * 100) if games > 0 else 0
                medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "")
                with st.expander(f"{medal} **{pid}** - Rank #{rank} ({pts} pts)"):
                    c1, c2, c3, c4, c5 = st.columns(5)
                    c1.metric("Games", games); c2.metric("Wins", w); c3.metric("Losses", l); c4.metric("Draws", d); c5.metric("Win Rate", f"{wr:.1f}%")
        else:
            st.warning("No standings data for this league.")

    with tab_matches:
        c1, c2 = st.columns(2)
        status_filter = c1.selectbox("Status", ["All", "Completed", "In Progress", "Scheduled"], key="sf")
        round_filter = c2.number_input("Round (0=All)", min_value=0, value=0, step=1, key="rf")
        status_map = {"All": None, "Scheduled": "scheduled", "In Progress": "in_progress", "Completed": "completed"}
        matches = api_client.list_matches(league_id=selected_league, round_number=round_filter or None, status=status_map.get(status_filter))
        if matches:
            st.markdown(f"**{len(matches)} match(es)**")
            for m in sorted(matches, key=lambda x: x.get("timestamp") or "", reverse=True):
                render_match_card(m, show_details=True)
        else:
            st.info("No matches found for this league.")

    with tab_analytics:
        data = api_client.get_standings(league_id=selected_league)
        if data and (s := data.get("standings", [])):
            render_charts(s)
        else:
            st.info("No analytics data. Complete matches first.")

st.markdown("---")
st.caption("Data updates after each match. Click Refresh for latest results.")
