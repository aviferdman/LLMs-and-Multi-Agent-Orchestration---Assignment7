"""League orchestration helper functions."""

import subprocess
import asyncio
from SHARED.league_sdk.logger import LeagueLogger
from SHARED.league_sdk.http_client import send_message
from SHARED.league_sdk.config_loader import load_agent_config
from SHARED.constants import LogEvent, Field, AgentType

# Load config once at module level
_agents_config = load_agent_config()
_lm_endpoint = _agents_config["league_manager"]["endpoint"]

async def start_agent(agent_type: str, agent_id: str, port: int, logger: LeagueLogger):
    """Start an agent process."""
    if agent_type == AgentType.LEAGUE_MANAGER:
        script = "agents/league_manager/main.py"
    elif agent_type == AgentType.REFEREE:
        script = f"agents/launch_referee_{agent_id[-2:]}.py"
    else:  # player
        script = f"agents/launch_player_{agent_id[-2:]}.py"
    
    # Use CREATE_NEW_PROCESS_GROUP to prevent signals from propagating
    proc = subprocess.Popen(
        ["python", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    
    logger.log_message(LogEvent.STARTUP, {"agent_id": agent_id, "port": port})
    return proc

async def wait_for_agents(timeout: int, logger: LeagueLogger):
    """Wait for all agents to be ready."""
    logger.log_message(LogEvent.STARTUP, {"timeout": timeout, "status": "waiting"})
    await asyncio.sleep(timeout)

async def register_referee(referee_id: str, endpoint: str, logger: LeagueLogger):
    """Register referee with league manager."""
    from SHARED.contracts import build_referee_register_request
    
    message = build_referee_register_request(referee_id, endpoint)
    response = await send_message(_lm_endpoint, message)
    logger.log_message(LogEvent.REFEREE_REGISTERED, {Field.REFEREE_ID: referee_id, "response": str(response)})

async def register_player(player_id: str, endpoint: str, logger: LeagueLogger):
    """Register player with league manager."""
    from SHARED.contracts import build_league_register_request
    
    message = build_league_register_request(player_id, endpoint)
    response = await send_message(_lm_endpoint, message)
    logger.log_message(LogEvent.PLAYER_REGISTERED, {Field.PLAYER_ID: player_id, "response": str(response)})

async def start_all_agents(agents_config: dict, logger: LeagueLogger):
    """Start all agents (league manager, referees, players)."""
    processes = []
    
    # Start League Manager using config port
    lm_config = agents_config["league_manager"]
    lm_proc = await start_agent(AgentType.LEAGUE_MANAGER, lm_config["agent_id"], lm_config["port"], logger)
    processes.append(lm_proc)
    
    # Start Referees
    for referee in agents_config["referees"]:
        ref_proc = await start_agent(AgentType.REFEREE, referee["referee_id"], referee["port"], logger)
        processes.append(ref_proc)
    
    # Start Players
    for player in agents_config["players"]:
        player_proc = await start_agent(AgentType.PLAYER, player["player_id"], player["port"], logger)
        processes.append(player_proc)
    
    return processes

async def register_all_agents(agents_config: dict, logger: LeagueLogger):
    """Register all referees and players with league manager."""
    # Register referees
    for referee in agents_config["referees"]:
        await register_referee(referee["referee_id"], referee["endpoint"], logger)
    
    # Register players
    for player in agents_config["players"]:
        await register_player(player["player_id"], player["endpoint"], logger)
