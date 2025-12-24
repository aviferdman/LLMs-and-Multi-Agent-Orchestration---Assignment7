"""Broadcasting utilities for League Manager."""

from typing import Any, Dict

from SHARED.constants import Field, LogEvent
from SHARED.league_sdk.agent_comm import send


async def broadcast_to_agents(
    message: Dict[str, Any],
    registered_players: Dict[str, Any],
    registered_referees: Dict[str, Any],
    logger,
):
    """Broadcast a message to all registered agents."""
    endpoints = []
    for player_info in registered_players.values():
        endpoints.append(player_info[Field.ENDPOINT])
    for referee_info in registered_referees.values():
        endpoints.append(referee_info[Field.ENDPOINT])

    # Send to all endpoints (fire and forget - don't wait for responses)
    for endpoint in endpoints:
        try:
            await send(endpoint, message)
        except Exception as e:
            logger.log_error(LogEvent.ERROR, f"Broadcast failed to {endpoint}: {e}")
