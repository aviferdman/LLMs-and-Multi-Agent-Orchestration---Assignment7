"""Header component with navigation."""

import streamlit as st


def render_header(current_page: str = "Dashboard"):
    """Render the application header with navigation."""
    st.markdown(
        """
        <style>
        .header-container {
            background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .header-title {
            color: white;
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
        }
        .header-subtitle {
            color: #f0f0f0;
            font-size: 1.1rem;
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">🏆 AI Agent League</h1>
            <p class="header-subtitle">Competition Management System</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation menu
    cols = st.columns([1, 1, 1, 1, 1, 1, 2])

    with cols[0]:
        if st.button(
            "📊 Dashboard",
            use_container_width=True,
            type="primary" if current_page == "Dashboard" else "secondary",
        ):
            st.switch_page("app.py")

    with cols[1]:
        if st.button(
            "🚀 Launcher",
            use_container_width=True,
            type="primary" if current_page == "Launcher" else "secondary",
        ):
            st.switch_page("pages/launcher.py")

    with cols[2]:
        if st.button(
            "⚡ Live",
            use_container_width=True,
            type="primary" if current_page == "Live" else "secondary",
        ):
            st.switch_page("pages/live.py")

    with cols[3]:
        if st.button(
            "🏅 Standings",
            use_container_width=True,
            type="primary" if current_page == "Standings" else "secondary",
        ):
            st.switch_page("pages/standings.py")

    with cols[4]:
        if st.button(
            "🎮 Matches",
            use_container_width=True,
            type="primary" if current_page == "Matches" else "secondary",
        ):
            st.switch_page("pages/matches.py")

    with cols[5]:
        if st.button(
            "👥 Players",
            use_container_width=True,
            type="primary" if current_page == "Players" else "secondary",
        ):
            st.switch_page("pages/players.py")

    st.markdown("---")
