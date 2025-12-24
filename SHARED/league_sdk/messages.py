"""Protocol message utilities.

This module re-exports from SHARED.contracts for backward compatibility.
The canonical implementations are now in SHARED.contracts.*.
"""

from SHARED.contracts.base_contract import (
    create_base_message,
    create_game_message,
    validate_base_message as validate_message,
)
from SHARED.contracts.player_contracts import (
    build_choose_parity_response,
    build_game_join_ack,
    build_parity_choice,  # deprecated alias
)
from SHARED.contracts.referee_contracts import (
    build_choose_parity_call,
    build_game_error,
    build_game_invitation,
    build_game_over,
    build_match_result_report,
)
from SHARED.protocol_constants import generate_timestamp as format_timestamp

# Re-export all for backward compatibility
__all__ = [
    "create_base_message",
    "create_game_message",
    "validate_message",
    "format_timestamp",
    "build_game_invitation",
    "build_game_join_ack",
    "build_choose_parity_call",
    "build_parity_choice",
    "build_choose_parity_response",
    "build_game_over",
    "build_match_result_report",
    "build_game_error",
]
