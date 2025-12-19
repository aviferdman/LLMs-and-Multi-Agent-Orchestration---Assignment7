"""Protocol contracts for league.v2."""

from .base_contract import (
    PROTOCOL_VERSION,
    create_base_message,
    validate_base_message
)
from .league_manager_contracts import (
    build_referee_register_request,
    build_referee_register_response,
    build_league_register_request,
    build_league_register_response,
    build_match_result_ack,
    build_start_league,
    build_league_status,
    build_run_match,
    build_run_match_ack
)
from .referee_contracts import (
    build_game_invitation,
    build_choose_parity_call,
    build_game_over,
    build_match_result_report
)
from .player_contracts import (
    build_game_join_ack,
    build_parity_choice
)

__all__ = [
    "PROTOCOL_VERSION",
    "create_base_message",
    "validate_base_message",
    "build_referee_register_request",
    "build_referee_register_response",
    "build_league_register_request",
    "build_league_register_response",
    "build_match_result_ack",
    "build_start_league",
    "build_league_status",
    "build_run_match",
    "build_run_match_ack",
    "build_game_invitation",
    "build_choose_parity_call",
    "build_game_over",
    "build_match_result_report",
    "build_game_join_ack",
    "build_parity_choice"
]
