"""Referee contract definitions - Facade module.

This module re-exports all Referee contracts for backward compatibility.
The actual implementations are split into smaller modules.

Referee-sourced messages:
- REFEREE_REGISTER_REQUEST: Referee → League Manager
- GAME_INVITATION: Referee → Player
- CHOOSE_PARITY_CALL: Referee → Player
- GAME_OVER: Referee → Both Players
- MATCH_RESULT_REPORT: Referee → League Manager
- GAME_ERROR: Referee → Player
- RUN_MATCH_ACK: Referee → League Manager
"""

# Re-export game flow contracts
from .game_flow_contracts import (
    build_choose_parity_call,
    build_game_invitation,
)

# Re-export game result contracts
from .game_result_contracts import (
    build_game_error,
    build_game_over,
    build_match_result_report,
    build_run_match_ack,
)

# Export all for wildcard imports
__all__ = [
    # Game flow
    "build_game_invitation",
    "build_choose_parity_call",
    # Game results
    "build_game_over",
    "build_match_result_report",
    "build_game_error",
    "build_run_match_ack",
]
