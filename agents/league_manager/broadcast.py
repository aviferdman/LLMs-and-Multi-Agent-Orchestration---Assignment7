"""Broadcasting utilities for League Manager."""

from typing import Dict, Any

from SHARED.league_sdk.http_client import send_message
from SHARED.constants import Field, LogEvent


async def broadcast_to_agents(
    message: Dict[str, Any],
    registered_players: Dict[str, Any],
    registered_referees: Dict[str, Any],
    logger
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
            await send_message(endpoint, message, timeout=5)
        except Exception as e:
            logger.log_error(LogEvent.ERROR, f"Broadcast failed to {endpoint}: {e}")
