# GUI Implementation Guide - Phase 15 Complete

## Executive Summary

This document provides a comprehensive guide to the AI Agent League GUI implementation completed in Phase 15. The GUI has been developed using **Streamlit** as the frontend framework with a **FastAPI** backend, providing a professional, user-friendly interface for managing and monitoring AI agent competitions.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Current Implementation Status](#current-implementation-status)
3. [Component Library](#component-library)
4. [Page Descriptions](#page-descriptions)
5. [Design System](#design-system)
6. [API Integration](#api-integration)
7. [Running the GUI](#running-the-gui)
8. [Enhancement Recommendations](#enhancement-recommendations)
9. [Testing Guide](#testing-guide)
10. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### Technology Stack

- **Frontend**: Streamlit 1.40.2
- **Backend**: FastAPI (with Uvicorn)
- **Data Visualization**: Plotly Express
- **Real-time Updates**: Planned WebSocket integration
- **Communication Protocol**: league.v2 protocol

### Directory Structure

```
gui/
├── app.py                    # Main dashboard entry point
├── config.py                 # Configuration and design tokens
├── api_client.py             # API communication layer
├── components/               # Reusable UI components
│   ├── __init__.py
│   ├── header.py            # Navigation header
│   ├── match_card.py        # Match display cards
│   ├── player_card.py       # Player profile cards
│   ├── live_match_panel.py  # Live match viewer
│   ├── standings_table.py   # Rankings table
│   └── charts.py            # Data visualizations
└── pages/                    # Multi-page app structure
    ├── launcher.py          # League launcher
    ├── live.py              # Live match viewer
    ├── matches.py           # Match history
    ├── players.py           # Player profiles
    └── standings.py         # League standings

api/
├── main.py                   # FastAPI server
├── routes/                   # API endpoints
│   ├── games.py
│   ├── league.py
│   ├── matches.py
│   └── players.py
└── models/                   # Data models

.streamlit/
└── config.toml              # Streamlit configuration
```

---

## Current Implementation Status

### ✅ Completed Features

#### Core Pages (6 Total)

1. **Dashboard (app.py)** - Main overview page
   - League status metrics
   - Current standings preview
   - Recent match history
   - Quick action buttons
   - Auto-refresh capability

2. **Launcher (launcher.py)** - League configuration and startup
   - Game type selection (Connect Four, Tic-Tac-Toe)
   - Player registration interface
   - Tournament format configuration
   - League initialization controls

3. **Live Viewer (live.py)** - Real-time match monitoring
   - Active match selection
   - Live game state visualization
   - Player status indicators
   - Auto-refresh toggle (configurable interval)

4. **Standings (standings.py)** - Rankings and analytics
   - Sortable rankings table
   - Interactive charts (Plotly)
   - Detailed player statistics
   - Performance breakdowns

5. **Matches (matches.py)** - Match history browser
   - Multi-criteria filtering (status, round, player)
   - Sorting options
   - Match detail cards
   - Summary statistics

6. **Players (players.py)** - Player profiles
   - Player listing with stats
   - Detailed player view
   - Match history by player
   - Win/loss records

#### Components Library

All components are located in `gui/components/`:

- **header.py** - Consistent navigation header with active page highlighting
- **match_card.py** - Displays match information with status badges
- **player_card.py** - Player profile cards with stats and status indicators
- **live_match_panel.py** - Real-time match visualization with game board
- **standings_table.py** - Rankings table with medals and statistics
- **charts.py** - Interactive data visualizations using Plotly

#### API Client (api_client.py)

Comprehensive API wrapper providing:
- `get_league_status()` - Fetch league state
- `list_games()` - Available game types
- `get_game(game_id)` - Game details
- `list_players()` - All registered players
- `get_player(player_id)` - Player details
- `get_player_history(player_id)` - Match history
- `get_standings()` - Current rankings
- `list_matches(round_number, status)` - Match listing with filters
- `get_match(match_id)` - Detailed match information
- Error handling with user-friendly messages

#### Configuration (config.py)

Centralized configuration including:
- Page metadata (title, icon)
- Color scheme constants
- Refresh intervals
- Status icons mapping
- API endpoint configuration

### 🔨 Enhancement Recommendations from Sub-Agents

The UI-Designer and Fullstack-Developer agents completed comprehensive analysis and created enhancement proposals. Below are key recommendations that could be implemented:

#### Design System Enhancements

**Proposed Design Tokens** (from UI-Designer agent analysis):

```python
# WCAG AA Compliant Color Palette
COLORS = {
    "primary": "#1976D2",        # Blue 700 - Contrast: 5.2:1
    "primary_light": "#42A5F5",  # Blue 400
    "primary_dark": "#0D47A1",   # Blue 900
    "success": "#66BB6A",        # Green 400 - Contrast: 6.2:1
    "warning": "#FFB74D",        # Orange 300 - Contrast: 8.1:1
    "danger": "#EF5350",         # Red 400 - Contrast: 4.9:1
    "info": "#29B6F6",           # Light Blue 400
    # ... extended palette
}

# Typography Scale (1.250 Major Third)
TYPOGRAPHY = {
    "display": "3.052rem",
    "h1": "2.441rem",
    "h2": "1.953rem",
    "h3": "1.563rem",
    "body": "1rem",
    "small": "0.8rem",
}

# Spacing System (8px base unit)
SPACING = {
    "xs": "0.25rem",   # 4px
    "sm": "0.5rem",    # 8px
    "md": "1rem",      # 16px
    "lg": "1.5rem",    # 24px
    "xl": "2rem",      # 32px
}
```

#### Component Enhancements

**Enhanced Header with Gradients**:
```python
def render_header(current_page: str = "Dashboard"):
    """Render enhanced header with gradient background."""
    gradient = "linear-gradient(90deg, #1976D2 0%, #1565C0 50%, #0D47A1 100%)"
    st.markdown(f"""
        <div style="background: {gradient};
                    padding: 1.5rem;
                    border-radius: 10px;
                    margin-bottom: 2rem;">
            <h1 style="color: white; margin: 0;">🏆 AI Agent League</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0;">
                Multi-Agent Competition Platform
            </p>
        </div>
    """, unsafe_allow_html=True)
```

**Standings Table with Progress Bars**:
```python
def render_standings_table(standings: List[Dict], show_medals: bool = True):
    """Enhanced standings with win rate progress bars."""
    for idx, player in enumerate(standings):
        rank = idx + 1
        win_rate = player.get("win_rate", 0.0)

        # Gradient backgrounds for top 3
        bg_color = {
            1: "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)",  # Gold
            2: "linear-gradient(135deg, #C0C0C0 0%, #808080 100%)",  # Silver
            3: "linear-gradient(135deg, #CD7F32 0%, #8B4513 100%)",  # Bronze
        }.get(rank, "#f8f9fa")

        # Win rate progress bar
        st.progress(win_rate, text=f"{win_rate:.1%}")
```

#### Fullstack Integration Enhancements

**API Client with Caching**:
```python
from functools import wraps
import time

def cached_api_call(ttl: int = 60):
    """Cache API responses with TTL."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = f"{func.__name__}_{args}_{kwargs}"
            if cache_key in self._cache:
                cached_data, timestamp = self._cache[cache_key]
                if time.time() - timestamp < ttl:
                    return cached_data
            result = func(self, *args, **kwargs)
            if result is not None:
                self._cache[cache_key] = (result, time.time())
            return result
        return wrapper
    return decorator
```

**WebSocket Client for Real-time Updates** (Proposed):
```python
class WebSocketClient:
    """WebSocket client for live match updates."""

    async def connect(self, url: str):
        """Connect to WebSocket server."""
        self.ws = await websockets.connect(url)

    async def subscribe_to_match(self, match_id: str):
        """Subscribe to match updates."""
        await self.ws.send(json.dumps({
            "action": "subscribe",
            "match_id": match_id
        }))
```

**Enhanced Error Handling** (Proposed):
```python
class APIException(Exception):
    """Base exception for API errors."""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}

def handle_api_errors(func):
    """Decorator for consistent error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return None
    return wrapper
```

---

## Component Library

### Header Component
**File**: `gui/components/header.py`

**Usage**:
```python
from gui.components.header import render_header

render_header("Dashboard")  # Highlights "Dashboard" as active page
```

**Features**:
- Consistent branding across all pages
- Active page highlighting
- Responsive navigation menu

---

### Match Card Component
**File**: `gui/components/match_card.py`

**Usage**:
```python
from gui.components.match_card import render_match_card

match_data = {
    "match_id": "match_001",
    "round_number": 1,
    "player1_id": "agent_alpha",
    "player2_id": "agent_beta",
    "status": "completed",
    "winner_id": "agent_alpha",
    "final_score": {"agent_alpha": 1, "agent_beta": 0}
}

render_match_card(match_data, show_details=True)
```

**Features**:
- Status badge with icon (✅ Completed, ⚡ In Progress, 📅 Scheduled)
- Player vs player display
- Score visualization
- Optional detailed view with round history

---

### Player Card Component
**File**: `gui/components/player_card.py`

**Usage**:
```python
from gui.components.player_card import render_player_card

player_data = {
    "player_id": "agent_alpha",
    "wins": 5,
    "losses": 2,
    "draws": 1,
    "games_played": 8,
    "win_rate": 0.625,
    "is_active": True
}

render_player_card(player_data, show_stats=True)
```

**Features**:
- Active/inactive status indicator
- Win/loss/draw statistics
- Win rate percentage
- Gradient background styling

---

### Live Match Panel
**File**: `gui/components/live_match_panel.py`

**Usage**:
```python
from gui.components.live_match_panel import render_live_match_panel

match_data = {
    "match_id": "match_001",
    "player1_id": "agent_alpha",
    "player2_id": "agent_beta",
    "current_round": 3,
    "game_state": {...},  # Game-specific state
    "player_states": {
        "agent_alpha": "submitted",
        "agent_beta": "thinking"
    }
}

render_live_match_panel(match_data)
```

**Features**:
- Real-time game board visualization
- Player status indicators (⏳ Waiting, 🤔 Thinking, ✅ Submitted)
- Current round information
- Round history display

---

### Standings Table
**File**: `gui/components/standings_table.py`

**Usage**:
```python
from gui.components.standings_table import render_standings_table

standings = [
    {
        "rank": 1,
        "player_id": "agent_alpha",
        "points": 15,
        "wins": 5,
        "losses": 0,
        "draws": 0,
        "games_played": 5,
        "win_rate": 1.0
    },
    # ... more players
]

render_standings_table(standings, show_medals=True)
```

**Features**:
- Rank-ordered display
- Medal icons for top 3 (🥇🥈🥉)
- Sortable columns
- Win/loss/draw breakdown

---

### Charts Component
**File**: `gui/components/charts.py`

**Usage**:
```python
from gui.components.charts import render_charts

standings = [...]  # Same format as standings table

render_charts(standings)
```

**Features**:
- **Points Distribution**: Bar chart comparing player points
- **Win Distribution**: Pie chart showing win percentages
- **Win Rate Comparison**: Bar chart with win rate percentages
- Interactive Plotly charts with zoom and pan

---

## Page Descriptions

### Dashboard (app.py)

**Route**: `/` (main page)

**Purpose**: Provides a high-level overview of the league status, current standings, and recent activity.

**Sections**:
1. **League Status Metrics**
   - Status indicator (⏸️ Not Started, 📝 Registering, ⚡ In Progress, 🏁 Completed)
   - Game type display
   - Round progress tracker
   - Match completion counter
   - Progress bar

2. **Current Standings**
   - Top players rankings table
   - Medals for top 3 positions
   - Quick stats summary

3. **Recent Matches**
   - Last 5 matches
   - Match cards with results
   - Quick access to match details

4. **Quick Actions**
   - Launch New League button
   - Watch Live Matches button
   - View Full Standings button

**Auto-refresh**: Manual refresh button available

---

### Launcher (launcher.py)

**Route**: `/pages/launcher`

**Purpose**: Configure and start new league competitions.

**Sections**:
1. **Game Selection**
   - Dropdown to select game type (Connect Four, Tic-Tac-Toe)
   - Game rules display
   - Game preview

2. **Player Registration**
   - List of available agents
   - Player selection interface
   - Registration status

3. **Tournament Configuration**
   - Format selection (Round Robin, Elimination, Swiss)
   - Number of rounds
   - Match settings

4. **Launch Controls**
   - Start League button
   - Configuration validation
   - Status feedback

---

### Live Viewer (live.py)

**Route**: `/pages/live`

**Purpose**: Watch matches in real-time with live updates.

**Sections**:
1. **Match Selector**
   - Dropdown of active/scheduled matches
   - Match preview info

2. **Live Match Panel**
   - Game board visualization
   - Player status indicators
   - Current round display
   - Score tracking

3. **Match Information Expander**
   - Match ID
   - Round number
   - Referee ID
   - Start time

4. **Auto-refresh Toggle**
   - Enable/disable auto-refresh
   - Manual refresh button
   - Configurable interval (default: 5 seconds)

**Note**: Auto-refresh uses `time.sleep()` and `st.rerun()` - consider WebSocket upgrade for true real-time updates.

---

### Standings (standings.py)

**Route**: `/pages/standings`

**Purpose**: Display comprehensive league rankings and analytics.

**Sections**:
1. **Rankings Table**
   - Sortable by rank, points, wins, win rate, games played
   - Medal indicators for top 3
   - Complete statistics

2. **Performance Analytics**
   - Points distribution chart
   - Win distribution pie chart
   - Win rate comparison

3. **Detailed Statistics Expanders**
   - Per-player expandable sections
   - Points, wins, losses, draws
   - Win rate percentage
   - Games played count

**Features**:
- Manual refresh button
- Last updated timestamp
- Multiple sort options

---

### Matches (matches.py)

**Route**: `/pages/matches`

**Purpose**: Browse and filter match history.

**Sections**:
1. **Filters**
   - Status filter (All, Scheduled, In Progress, Completed, Cancelled)
   - Round number filter
   - Player filter

2. **Sort Options**
   - Recent first
   - By round number
   - By status

3. **Match List**
   - Match cards with details
   - Expandable for round history
   - Winner highlighting

4. **Match Statistics**
   - Total matches count
   - Completed count
   - In progress count
   - Scheduled count

---

### Players (players.py)

**Route**: `/pages/players`

**Purpose**: View player profiles and individual statistics.

**Sections**:
1. **Player Grid**
   - All players displayed in 3-column grid
   - Player cards with basic stats

2. **Player Selector**
   - Dropdown to select player for details
   - Profile information

3. **Player Details**
   - Status badges (Active/Inactive, Registered/Not Registered)
   - Games played metric
   - Win rate metric

4. **Match History**
   - Last 10 matches
   - Result cards (🎉 Win, 😔 Loss, 🤝 Draw)
   - Score display
   - Opponent information
   - Match ID and timestamp

---

## Design System

### Color Scheme

Current colors defined in `gui/config.py`:

```python
COLORS = {
    "primary": "#1f77b4",    # Blue
    "success": "#2ca02c",    # Green
    "warning": "#ff7f0e",    # Orange
    "danger": "#d62728",     # Red
    "info": "#17becf",       # Cyan
    "waiting": "#bcbd22",    # Yellow-green
}
```

**Recommended Enhancement**: Implement WCAG AA compliant palette with 4.5:1 minimum contrast ratio.

---

### Status Icons

Defined in `gui/config.py`:

```python
STATUS_ICONS = {
    "scheduled": "📅",
    "in_progress": "⚡",
    "completed": "✅",
    "cancelled": "❌",
    "not_started": "⏸️",
    "registering": "📝",
    "paused": "⏸️",
}
```

---

### Refresh Intervals

```python
REFRESH_INTERVAL_DASHBOARD = 10  # seconds
REFRESH_INTERVAL_LIVE = 5        # seconds
```

---

## API Integration

### API Client Architecture

The `APIClient` class in `gui/api_client.py` provides a clean interface to the FastAPI backend.

**Initialization**:
```python
from gui.api_client import get_api_client

api_client = get_api_client()  # Uses default base URL from config
```

**Configuration**:
```python
# In gui/config.py
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
```

---

### Available Endpoints

#### League Management

**Get League Status**:
```python
status = api_client.get_league_status()
# Returns: {
#     "status": "in_progress",
#     "game_type": "connect_four",
#     "current_round": 2,
#     "total_rounds": 5,
#     "matches_completed": 3,
#     "matches_total": 10
# }
```

---

#### Game Information

**List Games**:
```python
games = api_client.list_games()
# Returns: [
#     {"game_id": "connect_four", "name": "Connect Four", ...},
#     {"game_id": "tic_tac_toe", "name": "Tic Tac Toe", ...}
# ]
```

**Get Game Details**:
```python
game = api_client.get_game("connect_four")
# Returns: {
#     "game_id": "connect_four",
#     "name": "Connect Four",
#     "description": "...",
#     "rules": {...}
# }
```

---

#### Player Management

**List Players**:
```python
players = api_client.list_players()
# Returns: [
#     {
#         "player_id": "agent_alpha",
#         "is_active": True,
#         "is_registered": True,
#         "wins": 5,
#         "losses": 2,
#         "draws": 1,
#         "games_played": 8,
#         "win_rate": 0.625
#     },
#     ...
# ]
```

**Get Player Details**:
```python
player = api_client.get_player("agent_alpha")
# Returns detailed player info
```

**Get Player History**:
```python
history = api_client.get_player_history("agent_alpha")
# Returns: {
#     "player_id": "agent_alpha",
#     "total_matches": 8,
#     "matches": [
#         {
#             "match_id": "match_001",
#             "opponent_id": "agent_beta",
#             "result": "win",
#             "player_score": 1,
#             "opponent_score": 0,
#             "played_at": "2025-12-20T10:30:00"
#         },
#         ...
#     ]
# }
```

---

#### Standings

**Get Standings**:
```python
standings_data = api_client.get_standings()
# Returns: {
#     "standings": [
#         {
#             "rank": 1,
#             "player_id": "agent_alpha",
#             "points": 15,
#             "wins": 5,
#             "losses": 0,
#             "draws": 0,
#             "games_played": 5,
#             "win_rate": 1.0
#         },
#         ...
#     ],
#     "last_updated": "2025-12-20T10:30:00"
# }
```

---

#### Match Management

**List Matches**:
```python
# All matches
matches = api_client.list_matches()

# Filter by round
matches = api_client.list_matches(round_number=2)

# Filter by status
matches = api_client.list_matches(status="in_progress")

# Both filters
matches = api_client.list_matches(round_number=2, status="completed")
```

**Get Match Details**:
```python
match = api_client.get_match("match_001")
# Returns: {
#     "match_id": "match_001",
#     "round_number": 1,
#     "player1_id": "agent_alpha",
#     "player2_id": "agent_beta",
#     "status": "completed",
#     "winner_id": "agent_alpha",
#     "final_score": {"agent_alpha": 1, "agent_beta": 0},
#     "started_at": "2025-12-20T10:00:00",
#     "completed_at": "2025-12-20T10:15:00",
#     "game_state": {...},
#     "round_history": [...]
# }
```

---

### Error Handling

Current implementation in `api_client.py`:

```python
def _make_request(self, method: str, endpoint: str, **kwargs):
    """Make HTTP request with error handling."""
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None
```

**Recommended Enhancement**: Implement custom exception classes for more granular error handling.

---

## Running the GUI

### Prerequisites

1. **Python 3.11+** installed
2. **Dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **API Server** running on port 8080:
   ```bash
   python run_api.py
   ```

---

### Start the GUI

**Method 1: Using Streamlit CLI**
```bash
streamlit run gui/app.py --server.port 8501
```

**Method 2: Using proposed run_gui.py script**
```bash
# (If implemented from fullstack-developer agent recommendations)
python run_gui.py --port 8501
```

---

### Configuration

**Streamlit Config** (`.streamlit/config.toml`):
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
font = "sans serif"

[server]
port = 8501
address = "localhost"
```

**Environment Variables**:
```bash
# Set API base URL (optional, defaults to http://localhost:8080)
export API_BASE_URL="http://localhost:8080"
```

---

### Accessing the GUI

Once running:
- Open browser to: `http://localhost:8501`
- Main dashboard will be displayed
- Navigation in sidebar or header

---

## Enhancement Recommendations

Based on the comprehensive analysis by the UI-Designer and Fullstack-Developer agents, here are prioritized enhancement recommendations:

### High Priority (Immediate Impact)

#### 1. Implement Design Token System
**Impact**: Consistency, maintainability, accessibility

**Implementation**:
- Create `gui/styles/design_tokens.py` with comprehensive design system
- Update all components to use design tokens
- Ensure WCAG AA compliance (4.5:1 contrast minimum)

**Example**:
```python
# gui/styles/design_tokens.py
COLORS = {
    "primary": "#1976D2",        # WCAG AA: 5.2:1
    "success": "#66BB6A",        # WCAG AA: 6.2:1
    "warning": "#FFB74D",        # WCAG AA: 8.1:1
    "danger": "#EF5350",         # WCAG AA: 4.9:1
}

TYPOGRAPHY = {
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "scale_ratio": 1.250,  # Major Third
}

SPACING = {
    "base": "8px",
    "scale": [4, 8, 16, 24, 32, 48, 64]
}
```

---

#### 2. Add Loading States and Skeletons
**Impact**: Better UX, perceived performance

**Implementation**:
- Create `gui/utils/loading.py` with skeleton screens
- Add loading spinners to API calls
- Implement progress indicators

**Example**:
```python
# gui/utils/loading.py
def render_skeleton_card(num_cards: int = 1, height: str = "150px"):
    """Render skeleton loading placeholders."""
    shimmer = """
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    """
    # ... skeleton implementation
```

**Usage**:
```python
with st.spinner("Loading matches..."):
    matches = api_client.list_matches()
```

---

#### 3. Implement Caching with TTL
**Impact**: Performance, reduced API load

**Implementation**:
- Add caching decorator to `api_client.py`
- Configure appropriate TTL for different data types
- Add cache clear functionality

**Example**:
```python
@cached_api_call(ttl=60)  # Cache for 60 seconds
def get_standings(self):
    return self._make_request("GET", "/league/standings")
```

---

#### 4. Enhanced Component Styling
**Impact**: Professional appearance, user engagement

**Implementation**:
- Add gradient backgrounds to key components
- Implement hover effects on interactive elements
- Add animations for state transitions

**Example** (Enhanced Match Card):
```python
def render_match_card(match: Dict, show_details: bool = False):
    """Enhanced match card with hover effects."""
    st.markdown(f"""
        <div class="match-card" style="
            background: linear-gradient(135deg, rgba(31,119,180,0.1), rgba(44,160,44,0.1));
            border-radius: 10px;
            padding: 1rem;
            transition: transform 0.2s;
            &:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
        ">
            <!-- Card content -->
        </div>
    """, unsafe_allow_html=True)
```

---

### Medium Priority (Quality of Life)

#### 5. WebSocket Integration for Real-time Updates
**Impact**: True real-time updates, better live experience

**Implementation**:
- Create `gui/websocket_client.py`
- Connect to FastAPI WebSocket endpoints
- Update live.py to use WebSocket instead of polling

**Example**:
```python
# gui/websocket_client.py
import asyncio
import websockets
import json

class WebSocketClient:
    async def connect(self, url: str = "ws://localhost:8080/ws"):
        self.ws = await websockets.connect(url)

    async def subscribe_to_match(self, match_id: str):
        await self.ws.send(json.dumps({
            "action": "subscribe",
            "match_id": match_id
        }))

    async def listen(self, callback):
        async for message in self.ws:
            data = json.loads(message)
            await callback(data)
```

---

#### 6. Export Functionality
**Impact**: Data portability, analysis capabilities

**Implementation**:
- Create `gui/utils/export.py`
- Add export buttons to key pages
- Support CSV and JSON formats

**Example**:
```python
# gui/utils/export.py
import pandas as pd

def export_to_csv(data: List[Dict], filename: str):
    """Export data to CSV file."""
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')

# Usage in standings.py
if st.button("Export Standings to CSV"):
    csv_data = export_to_csv(standings, "standings.csv")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="standings.csv",
        mime="text/csv"
    )
```

---

#### 7. Settings Page
**Impact**: User customization, configuration management

**Implementation**:
- Create `gui/pages/settings.py`
- Add theme selection
- API configuration
- Refresh interval settings
- Cache management

---

#### 8. Enhanced Error Handling
**Impact**: Better debugging, user feedback

**Implementation**:
- Create `api/middleware/error_handler.py`
- Implement custom exception classes
- Add error boundary components

**Example**:
```python
# api/middleware/error_handler.py
class APIException(Exception):
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class NotFoundException(APIException):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource} '{resource_id}' not found",
            status_code=404
        )
```

---

### Low Priority (Nice to Have)

#### 9. Advanced Filtering and Search
- Full-text search for players/matches
- Date range filters
- Advanced sorting options

#### 10. Notifications System
- Toast notifications for events
- Match completion alerts
- Player registration notifications

#### 11. Responsive Design Improvements
- Mobile-optimized layouts
- Tablet breakpoints
- Touch-friendly interactions

#### 12. Performance Monitoring
- Page load time tracking
- API response time metrics
- User interaction analytics

---

## Testing Guide

### Manual Testing Checklist

#### Dashboard Page
- [ ] League status displays correctly
- [ ] Standings table renders with correct data
- [ ] Recent matches show last 5 matches
- [ ] Quick action buttons navigate correctly
- [ ] Refresh button updates data
- [ ] Progress bar shows accurate percentage

#### Launcher Page
- [ ] Game selection dropdown works
- [ ] Player list loads correctly
- [ ] Tournament configuration options available
- [ ] Start button initiates league
- [ ] Error messages display for invalid configurations

#### Live Page
- [ ] Match selector shows active matches
- [ ] Game board visualizes correctly
- [ ] Player status updates in real-time
- [ ] Auto-refresh toggle works
- [ ] Manual refresh button functions
- [ ] Match information expander contains correct data

#### Standings Page
- [ ] Rankings table displays all players
- [ ] Sort options work correctly
- [ ] Charts render without errors
- [ ] Detailed statistics expand correctly
- [ ] Win rate calculations are accurate

#### Matches Page
- [ ] Filters apply correctly (status, round, player)
- [ ] Sort options work as expected
- [ ] Match cards display complete information
- [ ] Statistics summary is accurate
- [ ] No matches state displays correctly

#### Players Page
- [ ] Player grid displays all players
- [ ] Player selector dropdown works
- [ ] Player details load correctly
- [ ] Status badges show accurate state
- [ ] Match history displays last 10 matches
- [ ] Result cards styled correctly (win/loss/draw)

---

### API Integration Testing

**Test API Connectivity**:
```python
# Test script
from gui.api_client import get_api_client

def test_api_connectivity():
    client = get_api_client()

    # Test league status
    status = client.get_league_status()
    assert status is not None, "Failed to get league status"

    # Test players list
    players = client.list_players()
    assert isinstance(players, list), "Failed to get players list"

    # Test matches list
    matches = client.list_matches()
    assert isinstance(matches, list), "Failed to get matches list"

    print("✅ All API tests passed!")

if __name__ == "__main__":
    test_api_connectivity()
```

---

### Performance Testing

**Metrics to Monitor**:
- Page load time (target: < 2 seconds)
- API response time (target: < 500ms)
- Component render time
- Memory usage
- Browser console errors

**Tools**:
- Chrome DevTools Performance tab
- Streamlit built-in profiling
- Network tab for API calls

---

## Troubleshooting

### Common Issues

#### Issue: "Connection Error" when accessing GUI

**Symptoms**: Error message about unable to connect to API

**Solutions**:
1. Verify API server is running:
   ```bash
   curl http://localhost:8080/health
   ```
2. Check `API_BASE_URL` in config
3. Ensure ports 8080 and 8501 are not blocked
4. Check firewall settings

---

#### Issue: GUI appears but no data shows

**Symptoms**: Empty tables, "No data available" messages

**Solutions**:
1. Check API server logs for errors
2. Verify league has been started
3. Check that players are registered
4. Inspect browser console for JavaScript errors
5. Use browser Network tab to check API responses

---

#### Issue: Auto-refresh not working on Live page

**Symptoms**: Page doesn't update automatically

**Solutions**:
1. Verify auto-refresh toggle is enabled
2. Check `REFRESH_INTERVAL_LIVE` in config
3. Ensure no browser extensions blocking reloads
4. Check Streamlit server logs for errors

---

#### Issue: Charts not rendering

**Symptoms**: Blank space where charts should be

**Solutions**:
1. Verify Plotly is installed: `pip show plotly`
2. Check browser console for JavaScript errors
3. Ensure data format is correct (pandas DataFrame)
4. Try clearing browser cache
5. Check for conflicting CSS

---

#### Issue: Slow page loads

**Symptoms**: Long wait times when navigating

**Solutions**:
1. Implement caching (see enhancement #3)
2. Reduce API call frequency
3. Optimize data queries on backend
4. Enable Streamlit caching decorators:
   ```python
   @st.cache_data(ttl=60)
   def load_standings():
       return api_client.get_standings()
   ```

---

#### Issue: Match cards display incorrect data

**Symptoms**: Wrong scores, players, or statuses

**Solutions**:
1. Check API response format matches expected schema
2. Verify data mapping in component code
3. Add logging to track data transformation
4. Validate API endpoint returns correct data:
   ```bash
   curl http://localhost:8080/matches/{match_id}
   ```

---

## Development Workflow

### Adding a New Page

1. **Create page file**: `gui/pages/new_page.py`
2. **Set page config**:
   ```python
   import streamlit as st
   from gui.config import PAGE_TITLE, PAGE_ICON

   st.set_page_config(
       page_title=f"{PAGE_TITLE} - New Page",
       page_icon=PAGE_ICON,
       layout="wide"
   )
   ```
3. **Add header**: `render_header("New Page")`
4. **Implement page logic**
5. **Add navigation link** to header component
6. **Test thoroughly**

---

### Adding a New Component

1. **Create component file**: `gui/components/new_component.py`
2. **Define render function**:
   ```python
   from typing import Dict
   import streamlit as st

   def render_new_component(data: Dict):
       """Render new component."""
       # Implementation
   ```
3. **Import in `gui/components/__init__.py`**:
   ```python
   from .new_component import render_new_component
   ```
4. **Use in pages**:
   ```python
   from gui.components.new_component import render_new_component
   render_new_component(data)
   ```

---

### Adding a New API Endpoint Integration

1. **Add method to APIClient**:
   ```python
   def get_new_resource(self, resource_id: str):
       """Get new resource by ID."""
       endpoint = f"/new-resource/{resource_id}"
       return self._make_request("GET", endpoint)
   ```
2. **Add error handling**
3. **Test with actual API**
4. **Use in components/pages**

---

## Accessibility Considerations

### Current Status

The GUI has basic accessibility but needs improvements:

**✅ Current Strengths**:
- Semantic HTML structure
- Alt text on icons (emojis)
- Keyboard navigation (Streamlit default)
- Color-coded status indicators

**❌ Areas for Improvement**:
- Contrast ratios not verified (WCAG AA requires 4.5:1 minimum)
- No ARIA labels on custom components
- Screen reader support not tested
- Focus indicators could be more visible
- No skip navigation links

---

### Recommended Accessibility Enhancements

#### 1. Ensure WCAG AA Compliance
- Use color contrast checker on all text
- Implement design token system with verified colors
- Add patterns/icons in addition to color for state

#### 2. Add ARIA Labels
```python
st.markdown("""
    <button aria-label="Refresh league standings">
        🔄 Refresh
    </button>
""", unsafe_allow_html=True)
```

#### 3. Keyboard Navigation
- Ensure all interactive elements are keyboard accessible
- Add visible focus indicators
- Implement skip links for long pages

#### 4. Screen Reader Support
- Test with NVDA/JAWS
- Add descriptive labels to all interactive elements
- Use semantic HTML5 elements

---

## Best Practices

### Code Organization

**DO**:
- Keep components small and focused
- Use type hints for function parameters
- Document functions with docstrings
- Extract reusable logic into utilities
- Follow consistent naming conventions

**DON'T**:
- Put business logic in components
- Hardcode values that should be in config
- Create deeply nested components
- Ignore error cases

---

### Performance

**DO**:
- Use `@st.cache_data` for expensive computations
- Minimize API calls with caching
- Lazy load data when possible
- Optimize images and assets

**DON'T**:
- Make API calls in loops
- Load all data upfront
- Use large unoptimized images
- Forget to clear caches when needed

---

### User Experience

**DO**:
- Provide loading indicators
- Show helpful error messages
- Use consistent terminology
- Give visual feedback for actions
- Implement auto-refresh for live data

**DON'T**:
- Leave users waiting without feedback
- Show technical error messages
- Use inconsistent icons/colors
- Auto-refresh too frequently

---

## Future Roadmap

### Short Term (Next Sprint)

1. **Implement design token system** from UI-Designer recommendations
2. **Add loading states** with skeleton screens
3. **Enable API caching** with TTL
4. **Enhance component styling** with gradients and hover effects

### Medium Term (Next Month)

5. **WebSocket integration** for true real-time updates
6. **Export functionality** (CSV/JSON)
7. **Settings page** for user preferences
8. **Enhanced error handling** with custom exceptions

### Long Term (Future Phases)

9. **Advanced analytics** with more chart types
10. **Notification system** for events
11. **Mobile responsive design**
12. **Performance monitoring dashboard**
13. **Internationalization** (i18n) support
14. **Theme customization** (light/dark mode)
15. **Plugin system** for custom games

---

## Conclusion

The AI Agent League GUI provides a solid foundation for managing and monitoring agent competitions. The current implementation covers all core functionality with a clean, component-based architecture.

Key achievements:
- ✅ 6 functional pages covering all user needs
- ✅ Reusable component library
- ✅ Clean API integration layer
- ✅ Interactive visualizations with Plotly
- ✅ Real-time monitoring capabilities
- ✅ Professional UI with Streamlit

Next steps should focus on:
1. Implementing the design token system for consistency and accessibility
2. Adding loading states for better UX
3. Enabling caching for performance
4. Enhancing component styling for a more polished look

With the enhancement recommendations from the UI-Designer and Fullstack-Developer agents, the GUI is well-positioned to become a professional, production-ready application.

---

## References

- **Streamlit Documentation**: https://docs.streamlit.io
- **Plotly Python**: https://plotly.com/python/
- **WCAG 2.1 AA Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Design Tokens**: https://designtokens.org

---

**Document Version**: 1.0
**Last Updated**: 2025-12-20
**Author**: Generated by Claude Code (Sonnet 4.5)
**Status**: Complete - Phase 15 Implementation Guide
