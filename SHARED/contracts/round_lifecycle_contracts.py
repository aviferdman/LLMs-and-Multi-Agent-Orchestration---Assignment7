"""Round lifecycle contract builders - Facade module.

This module re-exports all round lifecycle contracts for backward compatibility.
The actual implementations are split into smaller modules.

League Manager-sourced messages:
- ROUND_ANNOUNCEMENT: LM → All Agents
- ROUND_COMPLETED: LM → Players
- LEAGUE_COMPLETED: LM → All Agents
- LEAGUE_STANDINGS_UPDATE: LM → Players
- LEAGUE_ERROR: LM → Agent
- LEAGUE_QUERY_RESPONSE: LM → Player/Referee
"""

# Re-export round contracts
from .round_contracts import (
    build_round_announcement,
    build_round_completed,
)

# Re-export standings contracts
from .standings_contracts import (
    build_league_completed,
    build_league_error,
    build_league_query_response,
    build_league_standings_update,
)

# Export all for wildcard imports
__all__ = [
    # Round management
    "build_round_announcement",
    "build_round_completed",
    # Standings and completion
    "build_league_completed",
    "build_league_standings_update",
    "build_league_error",
    "build_league_query_response",
]
