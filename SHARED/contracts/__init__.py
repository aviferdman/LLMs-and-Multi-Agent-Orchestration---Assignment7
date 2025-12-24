"""Protocol contracts for league.v2.

This module provides message builders and validators for all protocol messages.
All builders conform to the protocol specification in doc/protocol/v2/CONTRACTS.md.

Usage:
    from SHARED.contracts import (
        build_game_invitation,
        build_game_join_ack,
        validate_message,
        validate_or_raise,
    )
"""

from .base_contract import (
    create_base_message,
    create_game_message,
    validate_base_message,
)
from .exceptions import (
    InvalidMessageError,
    ProtocolValidationError,
    SchemaNotFoundError,
)
from .league_manager_contracts import (
    build_league_completed,
    build_league_error,
    build_league_query_response,
    build_league_register_request,
    build_league_register_response,
    build_league_standings_update,
    build_league_status,
    build_match_result_ack,
    build_referee_register_request,
    build_referee_register_response,
    build_round_announcement,
    build_round_completed,
    build_run_match,
    build_shutdown_ack,
    build_shutdown_command,
    build_start_league,
)
from .player_contracts import (
    build_choose_parity_response,
    build_game_join_ack,
    build_league_query,
    build_parity_choice,  # DEPRECATED
)
from .referee_contracts import (
    build_choose_parity_call,
    build_game_error,
    build_game_invitation,
    build_game_over,
    build_match_result_report,
    build_run_match_ack,
)
from .schema_validator import (
    clear_cache,
    get_schema,
    list_message_types,
    validate_incoming,
    validate_message,
    validate_or_raise,
    validated_builder,
)

# Protocol version constant
from SHARED.constants import PROTOCOL_VERSION

__all__ = [
    # Protocol version
    "PROTOCOL_VERSION",
    # Base contract utilities
    "create_base_message",
    "create_game_message",
    "validate_base_message",
    # Schema validation
    "validate_message",
    "validate_or_raise",
    "validate_incoming",
    "validated_builder",
    "get_schema",
    "list_message_types",
    "clear_cache",
    # Exceptions
    "ProtocolValidationError",
    "SchemaNotFoundError",
    "InvalidMessageError",
    # League Manager contracts
    "build_referee_register_request",
    "build_referee_register_response",
    "build_league_register_request",
    "build_league_register_response",
    "build_match_result_ack",
    "build_start_league",
    "build_league_status",
    "build_run_match",
    "build_shutdown_command",
    "build_shutdown_ack",
    # Round/League lifecycle
    "build_round_announcement",
    "build_round_completed",
    "build_league_completed",
    "build_league_standings_update",
    "build_league_error",
    "build_league_query_response",
    # Referee contracts
    "build_game_invitation",
    "build_choose_parity_call",
    "build_game_over",
    "build_match_result_report",
    "build_game_error",
    "build_run_match_ack",
    # Player contracts
    "build_game_join_ack",
    "build_choose_parity_response",
    "build_league_query",
    "build_parity_choice",  # DEPRECATED
]
