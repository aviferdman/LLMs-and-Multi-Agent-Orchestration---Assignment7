"""League orchestrator - Run complete league tournament."""

import asyncio
from SHARED.league_sdk.config_loader import load_agent_config, load_league_config
from SHARED.league_sdk.logger import LeagueLogger
from SHARED.constants import LeagueID, LogEvent, Timeout
from agents.league_manager.scheduler import get_match_schedule
from agents.league_manager.orchestration import (
    start_all_agents,
    wait_for_agents,
    register_all_agents
)

logger = LeagueLogger("ORCHESTRATOR")

async def run_league():
    """Main orchestrator function."""
    logger.log_message("LEAGUE_START", {})
    
    # Load configurations
    agents_config = load_agent_config()
    league_config = load_league_config(LeagueID.EVEN_ODD_2025)
    
    # Start all agents
    processes = await start_all_agents(agents_config, logger)
    
    # Wait for agents to initialize
    await wait_for_agents(Timeout.AGENT_STARTUP, logger)
    
    # Register all agents
    await register_all_agents(agents_config, logger)
    
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
