"""League orchestrator - Run complete league tournament."""

import asyncio
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any

from SHARED.league_sdk.config_loader import (
    load_agents_config,
    load_league_config
)
from SHARED.league_sdk.http_client import send_message
from SHARED.league_sdk.logger import LeagueLogger
from SHARED.constants import (
    MessageType,
    Field,
    AgentID,
    Port,
    Endpoint,
    LeagueID,
    LogEvent,
    Timeout,
    MCP_PATH
)
from agents.league_manager.scheduler import get_match_schedule

logger = LeagueLogger("ORCHESTRATOR")

async def start_agent(agent_type: str, agent_id: str, port: int):
    """Start an agent process."""
    if agent_type == LogEvent.LEAGUE_MANAGER:
        script = "agents/league_manager/main.py"
    elif agent_type == "referee":
        script = f"agents/referee_{agent_id}/main.py"
    else:  # player
        script = f"agents/player_{agent_id}/main.py"
    
    proc = subprocess.Popen(
        ["python", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    logger.log_message(LogEvent.STARTUP, {
        "agent_id": agent_id,
        "port": port
    })
    
    return proc

async def wait_for_agents(timeout: int = Timeout.LEAGUE_REGISTER):
    """Wait for all agents to be ready."""
    logger.log_message("WAITING_FOR_AGENTS", {"timeout": timeout})
    await asyncio.sleep(timeout)

async def register_referee(referee_id: str, endpoint: str):
    """Register referee with league manager."""
    from SHARED.contracts import build_referee_register_request
    
    message = build_referee_register_request(referee_id, endpoint)
    
    response = await send_message(Endpoint.LEAGUE_MANAGER, message)
    
    logger.log_message(LogEvent.REFEREE_REGISTERED, {
        Field.REFEREE_ID: referee_id,
        "response": response
    })

async def register_player(player_id: str, endpoint: str):
    """Register player with league manager."""
    from SHARED.contracts import build_league_register_request
    
    message = build_league_register_request(player_id, endpoint)
    
    response = await send_message(Endpoint.LEAGUE_MANAGER, message)
    
    logger.log_message(LogEvent.PLAYER_REGISTERED, {
        Field.PLAYER_ID: player_id,
        "response": response
    })

async def run_league():
    """Main orchestrator function."""
    logger.log_message("LEAGUE_START", {})
    
    # Load configurations
    agents_config = load_agents_config()
    league_config = load_league_config(LeagueID.EVEN_ODD_2025)
    
    processes = []
    
    # Start League Manager
    lm_proc = await start_agent(
        "league_manager",
        AgentID.LEAGUE_MANAGER,
        Port.LEAGUE_MANAGER
    )
    processes.append(lm_proc)
    
    # Start Referees
    for referee in agents_config["referees"]:
        ref_proc = await start_agent(
            "referee",
            referee["referee_id"],
            referee["port"]
        )
        processes.append(ref_proc)
    
    # Start Players
    for player in agents_config["players"]:
        player_proc = await start_agent(
            "player",
            player["player_id"],
            player["port"]
        )
        processes.append(player_proc)
    
    # Wait for agents to initialize
    await wait_for_agents(Timeout.AGENT_STARTUP)
    
    # Register referees
    for referee in agents_config["referees"]:
        await register_referee(
            referee["referee_id"],
            referee["endpoint"]
        )
    
    # Register players
    for player in agents_config["players"]:
        await register_player(
            player["player_id"],
            player["endpoint"]
        )
    
    await asyncio.sleep(5)
    
    # Get match schedule
    schedule = get_match_schedule()
    
    logger.log_message("SCHEDULE_LOADED", {
        "total_rounds": len(schedule),
        "total_matches": sum(len(r) for r in schedule)
    })
    
    # Execute matches
    # Note: Actual match execution would be triggered here
    # For now, this is a placeholder for the orchestration logic
    
    logger.log_message("LEAGUE_COMPLETE", {})
    
    # Keep processes running
    try:
        while True:
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        logger.log_message(LogEvent.SHUTDOWN, {})
        for proc in processes:
            proc.terminate()

if __name__ == "__main__":
    asyncio.run(run_league())
