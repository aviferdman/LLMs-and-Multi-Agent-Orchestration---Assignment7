"""Configuration settings for the GUI application."""

from pathlib import Path

# API Configuration
API_BASE_URL = "http://127.0.0.1:8080"
API_VERSION = "v1"
API_ENDPOINTS = {
    "league_status": f"{API_BASE_URL}/api/{API_VERSION}/league/status",
    "league_standings": f"{API_BASE_URL}/api/{API_VERSION}/league/standings",
    "league_start": f"{API_BASE_URL}/api/{API_VERSION}/league/start",
    "league_agents": f"{API_BASE_URL}/api/{API_VERSION}/league/agents",
    "games": f"{API_BASE_URL}/api/{API_VERSION}/games",
    "matches": f"{API_BASE_URL}/api/{API_VERSION}/matches",
    "players": f"{API_BASE_URL}/api/{API_VERSION}/players",
}
WEBSOCKET_URL = f"ws://127.0.0.1:8080/api/{API_VERSION}/ws/live"

# Refresh Intervals (seconds)
REFRESH_INTERVAL_DASHBOARD = 5
REFRESH_INTERVAL_LIVE = 2
REFRESH_INTERVAL_STANDINGS = 10

# UI Configuration
PAGE_TITLE = "AI Agent League"
PAGE_ICON = "🏆"
LAYOUT = "wide"

# Color Scheme
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "warning": "#ffc107",
    "danger": "#d62728",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40",
    "waiting": "#6c757d",
    "thinking": "#ffc107",
    "submitted": "#2ca02c",
    "completed": "#17a2b8",
}

# Status Icons
STATUS_ICONS = {
    "waiting": "⏳",
    "thinking": "🤔",
    "submitted": "✅",
    "scheduled": "📅",
    "in_progress": "⚡",
    "completed": "🏁",
    "cancelled": "❌",
    "win": "🎉",
    "loss": "😔",
    "draw": "🤝",
}

# Medals for Top Players
MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}

# File Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "SHARED" / "data"
