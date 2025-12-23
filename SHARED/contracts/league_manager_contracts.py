"""League Manager contract definitions - Facade module.

This module re-exports all League Manager contracts for backward compatibility.
The actual implementations are split into smaller modules.

League Manager-sourced messages (responses and control):
- REFEREE_REGISTER_RESPONSE: LM → Referee
- LEAGUE_REGISTER_RESPONSE: LM → Player
- MATCH_RESULT_ACK: LM → Referee
- LEAGUE_STATUS: LM → Launcher
- RUN_MATCH: LM → Referee
- SHUTDOWN_COMMAND: LM → All Agents

Registration requests (Referee/Player → LM):
- REFEREE_REGISTER_REQUEST
- LEAGUE_REGISTER_REQUEST

Launcher messages:
- START_LEAGUE: Launcher → LM
"""

from typing import Any, Dict

from SHARED.constants import Status

# Re-export registration contracts
from .registration_contracts import (
    build_league_register_request,
    build_league_register_response,
    build_referee_register_request,
    build_referee_register_response,
)

# Re-export match control contracts
from .match_control_contracts import (
    build_league_status,
    build_match_result_ack,
    build_run_match,
    build_shutdown_ack,
    build_shutdown_command,
    build_start_league,
)

# Re-export round lifecycle contracts for backward compatibility
from .round_lifecycle_contracts import (
    build_league_completed,
    build_league_error,
    build_league_query_response,
    build_league_standings_update,
    build_round_announcement,
    build_round_completed,
)

# Export all for wildcard imports
__all__ = [
    # Registration
    "build_referee_register_request",
    "build_referee_register_response",
    "build_league_register_request",
    "build_league_register_response",
    # Match control
    "build_match_result_ack",
    "build_start_league",
    "build_league_status",
    "build_run_match",
    "build_shutdown_command",
    "build_shutdown_ack",
    # Round lifecycle
    "build_round_announcement",
    "build_round_completed",
    "build_league_standings_update",
    "build_league_completed",
    "build_league_error",
    "build_league_query_response",
    # Deprecated
    "build_run_match_ack",
]


# DEPRECATED: Old function signatures for backward compatibility
def build_run_match_ack(
    match_id: str, status: str = Status.ACKNOWLEDGED
) -> Dict[str, Any]:
    """DEPRECATED: Use referee_contracts.build_run_match_ack instead."""
    import warnings

    from .referee_contracts import build_run_match_ack as _build_run_match_ack

    warnings.warn(
        "build_run_match_ack in league_manager_contracts is deprecated",
        DeprecationWarning,
        stacklevel=2,
    )
    return _build_run_match_ack(match_id=match_id, referee_id="UNKNOWN", status=status)
