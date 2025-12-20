"""Live match viewing page with real-time updates."""

import time
import streamlit as st
from gui.api_client import get_api_client
from gui.components.header import render_header
from gui.config import PAGE_ICON, PAGE_TITLE, REFRESH_INTERVAL_LIVE

st.set_page_config(page_title=f"{PAGE_TITLE} - Live", page_icon=PAGE_ICON, layout="wide")
render_header("Live")

st.title("⚡ Live Match View")
api_client = get_api_client()

# Get available leagues
leagues_data = api_client.list_leagues()
leagues = leagues_data.get("leagues", []) if leagues_data else []
default_league = leagues_data.get("default", "") if leagues_data else ""

# League selector
if leagues:
    selected_league = st.selectbox("Select League", leagues, index=leagues.index(default_league) if default_league in leagues else 0, key="live_league")
else:
    selected_league = None
    st.warning("No leagues found. Launch a league first!")

if selected_league:
    # Fetch matches for selected league
    all_matches = api_client.list_matches(league_id=selected_league)
    active = [m for m in (all_matches or []) if m.get("status") == "in_progress"]
    recent = sorted(all_matches or [], key=lambda x: x.get("timestamp") or "", reverse=True)[:6]

    # Show league activity summary
    c1, c2, c3 = st.columns(3)
    c1.metric("🔴 Live Now", len(active))
    c2.metric("✅ Completed", sum(1 for m in (all_matches or []) if m.get("status") == "completed"))
    c3.metric("📋 Total", len(all_matches or []))

    st.markdown("---")

    if active:
        st.subheader("🎮 Live Matches")
        for match in active:
            p1, p2 = match.get("player1_id", "?"), match.get("player2_id", "?")
            rnd = match.get("round_number", 0)
            st.markdown(f"""
            <div style="border:2px solid #ff6b6b; border-radius:10px; padding:1rem; margin:0.5rem 0; background:rgba(255,107,107,0.1);">
                <div style="display:flex; justify-content:space-between;">
                    <span>🔴 <strong>LIVE</strong> - Round {rnd}</span>
                    <span style="color:#888;">{match.get('match_id', '')}</span>
                </div>
                <div style="font-size:1.5em; text-align:center; margin:1rem 0;">
                    <strong>{p1}</strong> vs <strong>{p2}</strong>
                </div>
            </div>""", unsafe_allow_html=True)
    elif not recent:
        st.info("🏁 No matches yet. Launch a league to start!")

    st.markdown("---")
    st.subheader("📜 Recent Matches")

    if recent:
        for match in recent:
            p1, p2 = match.get("player1_id", "?"), match.get("player2_id", "?")
            rnd = match.get("round_number", 0)
            status = match.get("status", "unknown")
            winner = match.get("winner_id")
            icon = {"completed": "✅", "in_progress": "🔴", "scheduled": "⏳"}.get(status, "❓")
            if status == "completed":
                win_text = f"🎉 Winner: {winner}" if winner else "🤝 Draw"
            else:
                win_text = ""
            st.markdown(f"""
            <div style="border:1px solid #444; border-radius:8px; padding:0.8rem; margin:0.3rem 0;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span>{icon} Round {rnd}: <strong>{p1}</strong> vs <strong>{p2}</strong></span>
                </div>
                <div style="font-size:0.85em; color:#888;">{win_text}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("No matches yet. Launch a league to start!")
        if st.button("🚀 Launch League", type="primary", use_container_width=True):
            st.switch_page("pages/launcher.py")

st.markdown("---")
st.caption("⟳ Auto-refreshing every 3 seconds...")
time.sleep(REFRESH_INTERVAL_LIVE)
st.rerun()
