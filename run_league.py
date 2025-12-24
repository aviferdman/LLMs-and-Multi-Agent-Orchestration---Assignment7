"""League launcher - Start all agents.

Execution Flow:
1. Launcher starts all agent processes (LM, Referees, Players)
2. Agents register themselves with LM on startup:
   - Referees send REFEREE_REGISTER_REQUEST to LM
   - Players send LEAGUE_REGISTER_REQUEST to LM
3. LM auto-starts the league when all expected agents are registered
4. LM orchestrates the league:
   - LM sends ROUND_ANNOUNCEMENT to all agents
   - Referee sends GAME_INVITATION to Players
   - Players respond with GAME_JOIN_ACK
   - Referee sends CHOOSE_PARITY_CALL to Players
   - Players respond with CHOOSE_PARITY_RESPONSE
   - Referee determines winner, sends GAME_OVER to Players
   - Referee sends MATCH_RESULT_REPORT to LM
   - LM updates standings
5. LM sends LEAGUE_COMPLETED to all agents
6. All agents (Players, Referees, LM) shut down gracefully via protocol
"""

import asyncio
import signal
import sys
import time

from agents.league_manager.orchestration import start_all_agents, wait_for_agents
from SHARED.constants import LogEvent, Timeout
from SHARED.league_sdk.config_loader import (
    load_agent_config,
    load_system_config,
)
from SHARED.league_sdk.logger import LeagueLogger

# Load system config once at module level
_system_config = load_system_config()
_agents_config = load_agent_config()

logger = LeagueLogger("LAUNCHER")
_processes = []


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully - only for emergency interrupts."""
    logger.log_message(LogEvent.SHUTDOWN, {"reason": "signal", "signal": signum})
    sys.exit(0)


async def run_league():
    """Main launcher function.
    
    The launcher only starts agents - the LM auto-starts the league
    when all expected players and referees have registered.
    """
    global _processes
    logger.log_message("LAUNCHER_START", {})

    # Load configurations
    agents_config = load_agent_config()

    # Step 1: Start all agent processes
    logger.log_message("STARTING_AGENTS", {})
    _processes = await start_all_agents(agents_config, logger)

    # Step 2: Wait for agents to initialize
    await wait_for_agents(_system_config.timeouts[Timeout.AGENT_STARTUP], logger)

    # Step 3: Wait for all processes to exit naturally via protocol
    # LM auto-starts when all agents register, then sends LEAGUE_COMPLETED
    # Agents shut down gracefully after receiving LEAGUE_COMPLETED
    logger.log_message("WAITING_FOR_PROCESSES_TO_EXIT", {})

    for proc in _processes:
        proc.wait()  # Block until process exits

    logger.log_message("LAUNCHER_COMPLETE", {"all_processes_exited": True})


if __name__ == "__main__":
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        asyncio.run(run_league())
    except KeyboardInterrupt:
        logger.log_message(LogEvent.SHUTDOWN, {"reason": "user_interrupt"})
