# GUI Quick Start Guide

## Getting Started in 5 Minutes

### Prerequisites
- Python 3.11+ installed
- Dependencies installed: `pip install -r requirements.txt`

### Step 1: Start the API Server
```bash
python run_api.py
```
The API will start on `http://localhost:8080`

### Step 2: Start the GUI
```bash
streamlit run gui/app.py
```
The GUI will open automatically at `http://localhost:8501`

### Step 3: Launch a League
1. Navigate to **Launcher** page in the sidebar
2. Select a game type (Connect Four or Tic-Tac-Toe)
3. Configure players and tournament settings
4. Click **Start League**

### Step 4: Watch Matches Live
1. Navigate to **Live** page
2. Select an active match from the dropdown
3. Watch the game board update in real-time
4. Enable auto-refresh for continuous updates

---

## Page Navigation

| Page | Purpose | Key Features |
|------|---------|-------------|
| **Dashboard** | Overview | League status, standings preview, recent matches |
| **Launcher** | Start leagues | Game selection, player registration, config |
| **Live** | Watch matches | Real-time game board, player status, auto-refresh |
| **Standings** | Rankings | Sortable table, interactive charts, detailed stats |
| **Matches** | History | Filtering, sorting, match details, statistics |
| **Players** | Profiles | Player stats, match history, performance metrics |

---

## Key Components

### Header Navigation
Every page includes the header with:
- Application branding
- Current page indicator
- Navigation links

### Match Cards
Display match information with:
- Status badges (✅ Completed, ⚡ In Progress, 📅 Scheduled)
- Player names
- Scores
- Round information

### Player Cards
Show player profiles with:
- Active/inactive status
- Win/loss/draw statistics
- Win rate percentage
- Games played count

### Standings Table
Rankings table featuring:
- Medal indicators for top 3 (🥇🥈🥉)
- Sortable columns
- Complete statistics
- Win rate visualization

### Charts
Interactive visualizations:
- Points distribution bar chart
- Win distribution pie chart
- Win rate comparison chart
- Zoom and pan capabilities

---

## Configuration

### API Connection
Configure in `gui/config.py`:
```python
API_BASE_URL = "http://localhost:8080"
```

Or set environment variable:
```bash
export API_BASE_URL="http://localhost:8080"
```

### Refresh Intervals
Adjust in `gui/config.py`:
```python
REFRESH_INTERVAL_DASHBOARD = 10  # seconds
REFRESH_INTERVAL_LIVE = 5        # seconds
```

### Streamlit Theme
Customize in `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
```

---

## Troubleshooting

### GUI won't start
- Check Python version: `python --version` (needs 3.11+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check port 8501 is available: `netstat -an | grep 8501`

### No data showing
- Verify API is running: `curl http://localhost:8080/health`
- Check league has been started in Launcher
- Look for errors in terminal/console

### Auto-refresh not working
- Enable toggle on Live page
- Check browser doesn't block auto-reload
- Verify REFRESH_INTERVAL_LIVE is set correctly

---

## Next Steps

### Immediate Enhancements
1. **Improve styling** - Implement design token system (see GUI_IMPLEMENTATION_GUIDE.md)
2. **Add loading states** - Show spinners during API calls
3. **Enable caching** - Reduce API load with TTL-based caching

### Advanced Features
4. **WebSocket integration** - True real-time updates instead of polling
5. **Export functionality** - Download standings/matches as CSV/JSON
6. **Settings page** - User preferences and configuration

See `doc/GUI_IMPLEMENTATION_GUIDE.md` for detailed implementation instructions.

---

## Support

For issues, questions, or contributions:
- Review full documentation in `doc/GUI_IMPLEMENTATION_GUIDE.md`
- Check API documentation in `doc/API.md`
- Review system design in `doc/DESIGN_DOCUMENT.md`

---

**Last Updated**: 2025-12-20
