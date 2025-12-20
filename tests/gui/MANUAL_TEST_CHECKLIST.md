# GUI Manual Test Checklist

**Phase 16: GUI Testing - Manual Testing Component**

This checklist is used for manual validation of the Streamlit GUI application.

---

## Prerequisites

- [ ] API server is running (`python run_api.py`)
- [ ] GUI is running (`streamlit run gui/app.py`)
- [ ] Test data exists in SHARED/data directories
- [ ] Browser opened to http://localhost:8501

---

## 1. Dashboard Page Tests

### Layout & Structure
- [ ] Dashboard page loads without errors
- [ ] Header displays "League Competition Dashboard"
- [ ] Navigation sidebar is visible
- [ ] All menu items are clickable

### Content Display
- [ ] League status card shows current status
- [ ] Quick stats display (total matches, players, etc.)
- [ ] Current standings preview table visible
- [ ] Round progress indicator shows correct data
- [ ] Active matches indicator updates

### Interactivity
- [ ] Quick Launch button navigates to Launcher
- [ ] Refresh button updates data
- [ ] All links/buttons are responsive

---

## 2. Standings Page Tests

### Data Display
- [ ] Standings table loads with player data
- [ ] Columns: Rank, Player ID, Wins, Losses, Draws, Points
- [ ] Data is sorted by rank (ascending)
- [ ] All player statistics are accurate

### Sorting & Filtering
- [ ] Can sort by Wins (ascending/descending)
- [ ] Can sort by Losses (ascending/descending)
- [ ] Can sort by Points (ascending/descending)
- [ ] Sort persists correctly

### Visualizations
- [ ] Win rate pie chart displays correctly
- [ ] Player statistics bar chart shows all players
- [ ] Charts update when data refreshes
- [ ] Chart colors are distinct and readable

### Export
- [ ] Export to CSV button works
- [ ] Downloaded file contains correct data
- [ ] File name includes timestamp

---

## 3. Matches Page Tests

### Match List
- [ ] All matches display in chronological order
- [ ] Match cards show: Match ID, Players, Status, Score
- [ ] Completed matches show winner
- [ ] In-progress matches show current state

### Filtering
- [ ] Filter by Round (dropdown works)
- [ ] Filter by Status (All, Completed, In Progress)
- [ ] Filter by Player (dropdown populated)
- [ ] Filters combine correctly

### Match Details
- [ ] Click on match card expands details
- [ ] Round-by-round breakdown visible
- [ ] Player moves shown for each round
- [ ] Timestamps are formatted correctly

---

## 4. Players Page Tests

### Player Cards
- [ ] All registered players display
- [ ] Player cards show: ID, Strategy, Stats
- [ ] Win/Loss record is accurate
- [ ] Total points displayed

### Player Details
- [ ] Click on player opens detail view
- [ ] Match history timeline displays
- [ ] Each match shows: Opponent, Result, Score, Date
- [ ] Recent matches appear first

### Head-to-Head
- [ ] Select two players for comparison
- [ ] Head-to-head stats display
- [ ] Win rate comparison chart shows
- [ ] Historical matchups listed

### Performance Charts
- [ ] Performance trend chart displays
- [ ] X-axis shows match number/date
- [ ] Y-axis shows cumulative points
- [ ] Multiple players can be compared

---

## 5. Live Match View Tests ⭐

### WebSocket Connection
- [ ] Page loads and connects to WebSocket
- [ ] Connection status indicator shows "Connected"
- [ ] Auto-reconnect works after disconnect
- [ ] No errors in browser console

### Match Selection
- [ ] Grid/list of active matches displays
- [ ] Can click to focus on specific match
- [ ] Currently viewed match is highlighted
- [ ] Mini-status shows for unfocused matches

### Player Status Indicators
- [ ] ⏳ "Waiting" status before match starts
- [ ] 🤔 "Thinking..." appears when player deciding
- [ ] Animated spinner shows during thinking
- [ ] ✅ "Submitted" shows after player move
- [ ] Status updates in real-time

### Move Display
- [ ] Player move shows immediately after submission
- [ ] Move visible even if other player still thinking
- [ ] Partial state displays correctly (one submitted, one thinking)
- [ ] Move is highlighted/emphasized

### Round Results
- [ ] Round result appears after both players submit
- [ ] Drawn number displays
- [ ] Both player choices shown
- [ ] Winner highlighted clearly
- [ ] Animation/transition effect works

### Round History
- [ ] Completed rounds listed below live view
- [ ] Table shows: Round #, P1 Move, P2 Move, Winner
- [ ] Running score updates after each round
- [ ] New rounds animate in

### Match Timer
- [ ] Elapsed time since match start displays
- [ ] Time since last move shown
- [ ] Timer updates every second
- [ ] Format: MM:SS or HH:MM:SS

### Match Completion
- [ ] Match end event triggers completion view
- [ ] Final score displayed prominently
- [ ] Overall winner announced
- [ ] Match summary statistics shown
- [ ] Option to view next match appears

### Event Log
- [ ] Real-time event stream visible
- [ ] Events color-coded by type
- [ ] Can filter by match/player
- [ ] Scrollable log with timestamps
- [ ] Most recent events at top

---

## 6. Launcher Page Tests ⭐

### Game Selection
- [ ] Game dropdown populated with available games
- [ ] "Even-Odd" game appears in list
- [ ] Game description displays on selection
- [ ] Game rules tooltip/modal accessible

### Player Configuration
- [ ] Number of players selector works (dropdown/slider)
- [ ] Min: 2 players, Max: based on game
- [ ] Currently shows 4 players for Even-Odd
- [ ] Player list preview updates

### League Settings
- [ ] League name input field works
- [ ] Number of rounds calculated automatically
- [ ] Round-robin: (n × (n-1)) / 2 matches
- [ ] Timeout settings (optional advanced section)

### Validation
- [ ] Cannot launch without game selected
- [ ] Cannot launch with too few players
- [ ] Cannot launch with too many players
- [ ] Validation errors display clearly

### Launch Button
- [ ] Button enabled when valid configuration
- [ ] Button disabled when invalid
- [ ] Shows loading/progress indicator on click
- [ ] Auto-navigates to Live View on success

### Status Indicators
- [ ] Shows if agents are registered/ready
- [ ] Shows referee availability
- [ ] Warning if prerequisites not met
- [ ] Green checkmarks for ready components

---

## 7. Responsive Design Tests

### Desktop (1920x1080)
- [ ] All elements display properly
- [ ] No horizontal scrolling
- [ ] Charts render at appropriate size
- [ ] Text is readable

### Laptop (1366x768)
- [ ] Layout adjusts appropriately
- [ ] Sidebar collapses to hamburger menu
- [ ] Content fits without scrolling
- [ ] Charts scale down

### Tablet (768x1024)
- [ ] Touch-friendly button sizes
- [ ] Single column layout
- [ ] Tables become scrollable
- [ ] Charts stack vertically

### Mobile (375x667)
- [ ] Readable on small screen
- [ ] Navigation accessible
- [ ] No content cut off
- [ ] Pinch-to-zoom works on charts

---

## 8. Error Handling Tests

### API Unavailable
- [ ] Graceful error message displays
- [ ] Retry button appears
- [ ] App doesn't crash
- [ ] User can navigate to other pages

### WebSocket Disconnect
- [ ] "Disconnected" status shows
- [ ] Auto-reconnect attempts
- [ ] Success message on reconnect
- [ ] Missed events handled

### Invalid Data
- [ ] Missing data shows placeholder
- [ ] Corrupt data doesn't crash app
- [ ] Error logged to console
- [ ] User-friendly error message

### Network Issues
- [ ] Loading spinners appear
- [ ] Timeout handled gracefully
- [ ] Can retry failed requests
- [ ] Offline mode message

---

## 9. Performance Tests

### Load Times
- [ ] Dashboard loads in <2 seconds
- [ ] Standings page <1 second
- [ ] Matches page <2 seconds
- [ ] Players page <2 seconds
- [ ] Live view connects <1 second

### Refresh Performance
- [ ] Manual refresh completes quickly
- [ ] Auto-refresh doesn't cause lag
- [ ] Large datasets (100+ matches) handled
- [ ] Memory usage stays stable

### Chart Rendering
- [ ] Charts render smoothly
- [ ] No flickering on update
- [ ] Animations are smooth
- [ ] Interactions are responsive

---

## 10. Accessibility Tests

### Keyboard Navigation
- [ ] Can tab through all controls
- [ ] Enter/Space activates buttons
- [ ] Arrow keys work in dropdowns
- [ ] Esc closes modals

### Screen Reader
- [ ] Page titles announced
- [ ] Button purposes clear
- [ ] Alt text on images/icons
- [ ] Tables have proper headers

### Color Contrast
- [ ] Text readable on backgrounds
- [ ] Status indicators distinguishable
- [ ] Links visually distinct
- [ ] Focus indicators visible

---

## Test Summary

**Date**: ________________  
**Tester**: ________________  
**Version**: ________________  

**Total Tests**: 150+  
**Passed**: ______  
**Failed**: ______  
**Skipped**: ______  

**Critical Issues Found**: ________________

**Notes**:
_______________________________________________
_______________________________________________
_______________________________________________

**Sign-off**: ________________
