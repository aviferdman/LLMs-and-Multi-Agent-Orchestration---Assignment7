"""League launcher - Start all agents and trigger league execution.

Execution Flow:
1. Launcher starts all agent processes (LM, Referees, Players)
2. Agents register themselves with LM on startup:
   - Referees send REFEREE_REGISTER_REQUEST to LM
   - Players send LEAGUE_REGISTER_REQUEST to LM
3. Launcher sends START_LEAGUE to LM
4. LM orchestrates the league:
   - LM sends RUN_MATCH to Referees for each match
   - Referee sends GAME_INVITATION to Players
   - Players respond with GAME_JOIN_ACK
   - Referee sends CHOOSE_PARITY_CALL to Players
   - Players respond with PARITY_CHOICE
   - Referee determines winner, sends GAME_OVER to Players
   - Referee sends MATCH_RESULT_REPORT to LM
   - LM updates standings
5. LM completes all rounds and finalizes standings
"""

import asyncio
import time
import signal
import sys
from SHARED.league_sdk.config_loader import load_agent_config, load_league_config, load_system_config
from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.agent_comm import send
from SHARED.constants import LeagueID, LogEvent, Timeout
from SHARED.contracts import build_start_league
from agents.league_manager.orchestration import (
    start_all_agents,
    wait_for_agents
)

# Load system config once at module level
_system_config = load_system_config()
_agents_config = load_agent_config()
_lm_endpoint = _agents_config["league_manager"]["endpoint"]

logger = LeagueLogger("LAUNCHER")
_processes = []

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.log_message(LogEvent.SHUTDOWN, {"reason": "signal", "signal": signum})
    for proc in _processes:
        try:
            proc.terminate()
        except Exception:
            pass
    sys.exit(0)

async def run_league():
    """Main launcher function."""
    global _processes
    logger.log_message("LAUNCHER_START", {})
    
    # Load configurations
    agents_config = load_agent_config()
    league_config = load_league_config(LeagueID.EVEN_ODD_2025)
    
    # Step 1: Start all agent processes
    logger.log_message("STARTING_AGENTS", {})
    _processes = await start_all_agents(agents_config, logger)
    
    # Step 2: Wait for agents to initialize and self-register
    # Agents register themselves with LM on startup
    await wait_for_agents(_system_config.timeouts[Timeout.AGENT_STARTUP], logger)
    
    # Additional wait for self-registration to complete
    # Agents wait 2s after startup, so we need at least 5-7s for all registrations
    logger.log_message("WAITING_FOR_REGISTRATIONS", {})
    time.sleep(10)  # Synchronous sleep to avoid asyncio cancellation
    
    # Step 3: Send START_LEAGUE to LM
    logger.log_message("TRIGGERING_LEAGUE_START", {
        "league_id": league_config.league_id
    })
    
    start_msg = build_start_league(league_config.league_id, "LAUNCHER")
    response = await send(_lm_endpoint, start_msg)
    
    logger.log_message("LEAGUE_STARTED", {"response": response})
    
    # Step 4: Keep processes running until league completes
    logger.log_message("WAITING_FOR_LEAGUE_COMPLETION", {})
    
    # Synchronous sleep to avoid asyncio cancellation issues
    # 3 rounds × (broadcast + 2 matches × ~5s + standings) + buffer = ~90s
    time.sleep(90)  # Wait for matches to complete
    
    logger.log_message("LAUNCHER_COMPLETE", {})
    
    # Terminate all processes
    for proc in _processes:
        try:
            proc.terminate()
        except Exception:
            pass

if __name__ == "__main__":
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(run_league())
    except KeyboardInterrupt:
        logger.log_message(LogEvent.SHUTDOWN, {"reason": "user_interrupt"})
        for proc in _processes:
            try:
                proc.terminate()
            except Exception:
                pass
