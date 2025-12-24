# Running the System

**Version**: 1.0  
**Last Updated**: 2025-12-20  
**Status**: Complete

---

## Overview

This guide explains how to start, run, and monitor the AI Agent League Competition System. It covers manual agent startup, automated tournament execution, and monitoring.

---

## Quick Start

The fastest way to run a complete tournament:

```bash
python run_league.py
```

This automated script will:
1. Start the League Manager
2. Start both Referees
3. Start all 4 Players
4. Wait for registrations
5. Execute 3 rounds with 6 matches
6. Generate final standings
7. Shut down all agents

---

## Manual Startup (Step-by-Step)

For development, testing, or debugging, you may want to start agents manually in separate terminals.

### Prerequisites

Ensure you have:
- Completed installation (see INSTALLATION.md)
- Activated your virtual environment
- All configuration files in place

### Step 1: Start League Manager

Open a terminal and run:

```bash
python agents/league_manager/main.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The League Manager is now listening on **port 8000**.

**Keep this terminal open** - it will show registration and match activity.

### Step 2: Start Referees

Open **two new terminals** (one for each referee).

**Terminal 2** - Start Referee 1:
```bash
python agents/launch_referee_01.py
```

Expected output:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8001
Referee REF01 started on port 8001
```

**Terminal 3** - Start Referee 2:
```bash
python agents/launch_referee_02.py
```

Expected output:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8002
Referee REF02 started on port 8002
```

Both referees are now running and will automatically register with the League Manager.

### Step 3: Start Players

Open **four new terminals** (one for each player).

**Terminal 4** - Start Player 1 (Random Strategy):
```bash
python agents/launch_player_01.py
```

**Terminal 5** - Start Player 2 (Frequency Strategy):
```bash
python agents/launch_player_02.py
```

**Terminal 6** - Start Player 3 (Pattern Strategy):
```bash
python agents/launch_player_03.py
```

**Terminal 7** - Start Player 4 (Random Strategy):
```bash
python agents/launch_player_04.py
```

Each player outputs:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:810X
Player P0X started on port 810X with <Strategy>
```

All players will automatically register with the League Manager.

###

 Step 4: Verify All Agents Running

Check that all agents are operational:

```bash
# Check League Manager
curl http://localhost:8000/health

# Check Referees
curl http://localhost:8001/health
curl http://localhost:8002/health

# Check Players
curl http://localhost:8101/health
curl http://localhost:8102/health
curl http://localhost:8103/health
curl http://localhost:8104/health
```

Each should return `{"status": "ok"}` or similar.

### Step 5: Start Tournament

The `run_league.py` script will coordinate the tournament automatically. If you started agents manually, you can trigger rounds programmatically or wait for the scheduler.

Alternatively, monitor the League Manager terminal to see match activity as it happens.

---

## Monitoring

### Console Output

Each agent prints activity to its terminal:

**League Manager** shows:
- Agent registrations
- Round announcements
- Match results received
- Standings updates

**Referees** show:
- Match assignments
- Player invitations
- Game state changes
- Results reported

**Players** show:
- Round announcements
- Game invitations
- Parity choices made
- Match outcomes

### Log Files

All agents write structured logs in JSONL format:

```
SHARED/logs/league/league_manager.log.jsonl
SHARED/logs/agents/REF01.log.jsonl
SHARED/logs/agents/REF02.log.jsonl
SHARED/logs/agents/P01.log.jsonl
SHARED/logs/agents/P02.log.jsonl
SHARED/logs/agents/P03.log.jsonl
SHARED/logs/agents/P04.log.jsonl
```

View logs in real-time:

```bash
# On Unix/macOS:
tail -f SHARED/logs/league/league_manager.log.jsonl

# On Windows (PowerShell):
Get-Content SHARED/logs/league/league_manager.log.jsonl -Wait
```

### Data Files

Tournament data is saved in:

```
SHARED/data/leagues/league_2025_even_odd/standings.json
SHARED/data/matches/league_2025_even_odd/match_R1_M1.json
SHARED/data/matches/league_2025_even_odd/match_R1_M2.json
...
SHARED/data/players/P01/history.json
SHARED/data/players/P02/history.json
...
```

Check standings:
```bash
cat SHARED/data/leagues/league_2025_even_odd/standings.json | python -m json.tool
```

---

## Stopping the System

### Graceful Shutdown

Press `Ctrl+C` in each terminal to stop agents gracefully.

Recommended shutdown order:
1. Stop Players (terminals 4-7)
2. Stop Referees (terminals 2-3)
3. Stop League Manager (terminal 1)

### Force Kill (if needed)

If agents don't stop with Ctrl+C:

**On Windows:**
```bash
# Find processes
netstat -ano | findstr "8000 8001 8002 8101 8102 8103 8104"

# Kill by PID
taskkill /PID <PID> /F
```

**On macOS/Linux:**
```bash
# Kill by port
lsof -ti:8000 | xargs kill -9
lsof -ti:8001 | xargs kill -9
lsof -ti:8002 | xargs kill -9
lsof -ti:8101 | xargs kill -9
lsof -ti:8102 | xargs kill -9
lsof -ti:8103 | xargs kill -9
lsof -ti:8104 | xargs kill -9
```

---

## Running Options

### Development Mode

Run with auto-reload for code changes:

```bash
uvicorn agents.league_manager.main:app --reload --port 8000
```

### Production Mode

Run with multiple workers:

```bash
uvicorn agents.league_manager.main:app --workers 4 --port 8000
```

### Custom Ports

Override default ports via environment variables:

```bash
export LEAGUE_MANAGER_PORT=9000
export REF01_PORT=9001
python agents/league_manager/main.py
```

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python agents/league_manager/main.py
```

---

## Tournament Execution Flow

### Phase 1: Registration (5-10 seconds)
- All agents start and connect
- Referees register with League Manager
- Players register with League Manager
- League Manager validates and stores registrations

### Phase 2: Scheduling (1-2 seconds)
- League Manager generates match schedule
- 6 matches distributed across 3 rounds
- Referees assigned to matches

### Phase 3: Round 1 (10-15 seconds)
- League Manager announces Round 1
- Referees invite players to matches
- Players join matches
- Referees conduct games
- Referees report results
- League Manager updates standings

### Phase 4: Round 2 (10-15 seconds)
- Same as Round 1, different pairings

### Phase 5: Round 3 (10-15 seconds)
- Same as Round 1, final pairings

### Phase 6: Completion (1-2 seconds)
- League Manager calculates final rankings
- Standings broadcast to all players
- Tournament complete

**Total Duration**: ~40-50 seconds

---

## Troubleshooting

### Issue: Port Already in Use

**Symptom**: `[Errno 48] Address already in use`

**Solution**:
1. Check if agent is already running:
   ```bash
   lsof -ti:8000  # or relevant port
   ```
2. Kill existing process or use different port

### Issue: Agent Won't Start

**Symptom**: ImportError or ModuleNotFoundError

**Solution**:
1. Verify virtual environment is activated
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

### Issue: Agents Can't Connect

**Symptom**: Connection refused or timeout errors

**Solution**:
1. Verify all agents are running
2. Check firewall settings
3. Ensure localhost resolution works:
   ```bash
   ping localhost
   ```

### Issue: Match Timeout

**Symptom**: Matches not completing

**Solution**:
1. Check timeout settings in `system.json`
2. Increase `match_timeout` if needed
3. Check player/referee logs for errors

### Issue: Standings Not Updating

**Symptom**: Standings file not changing

**Solution**:
1. Check file permissions on `SHARED/data/`
2. Verify match results being received
3. Check League Manager logs for errors

---

## Best Practices

### During Development
- Run agents in separate terminals for visibility
- Monitor logs in real-time
- Clear old data between test runs:
  ```bash
  rm -rf SHARED/data/leagues/*/
  rm -rf SHARED/data/matches/*/
  ```

### For Testing
- Use `run_league.py` for repeatable tournaments
- Capture logs for analysis
- Run multiple times to test strategies

### For Demos
- Start all agents first, then trigger tournament
- Use larger terminal windows for readability
- Consider screen/tmux for managing multiple terminals

---

## Advanced Usage

### Running Multiple Tournaments

```bash
# Tournament 1
python run_league.py

# Clear data
rm -rf SHARED/data/leagues/league_2025_even_odd/*
rm -rf SHARED/data/matches/league_2025_even_odd/*

# Tournament 2
python run_league.py
```

### Custom Player Strategies

Modify player launch scripts to use different strategies:

```python
# agents/launch_player_01.py
from agents.player_strategies import PatternStrategy  # Change this
config = load_config()
player = Player(config, strategy=PatternStrategy())  # And this
```

### Batch Testing

Run 100 tournaments for strategy analysis:

```bash
for i in {1..100}; do
  python run_league.py > results_$i.log 2>&1
  # Process results
done
```

---

## Next Steps

- **Read TESTING.md** for information on running tests
- **Read ARCHITECTURE.md** to understand system design
- **Modify strategies** in `agents/player_strategies.py`
- **Analyze results** in `SHARED/data/` directories

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-20  
**Status**: Complete ✅
