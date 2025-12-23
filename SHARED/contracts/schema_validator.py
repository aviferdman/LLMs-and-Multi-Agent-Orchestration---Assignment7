"""JSON Schema-based protocol message validator - Facade module.

This module re-exports all schema validation functions for backward
compatibility. The actual implementations are split into smaller modules.

Usage:
    # Validate a message and get list of errors
    errors = validate_message(msg)
    if errors:
        print("Validation failed:", errors)

    # Validate and raise exception on failure
    validate_or_raise(msg)

    # Decorator for builder functions
    @validated_builder
    def build_game_invitation(...):
        ...

    # Validate incoming message in handler
    errors = validate_incoming(msg)
"""

# Re-export schema loader
from .schema_loader import (
    MESSAGE_TYPE_TO_SCHEMA,
    SCHEMAS_DIR,
    clear_cache,
    get_validator,
    load_schema,
)

# Re-export message validator
from .message_validator import (
    get_schema,
    list_message_types,
    validate_incoming,
    validate_message,
    validate_or_raise,
    validated_builder,
)

# Export all for wildcard imports
__all__ = [
    # Schema loader
    "SCHEMAS_DIR",
    "MESSAGE_TYPE_TO_SCHEMA",
    "load_schema",
    "get_validator",
    "clear_cache",
    # Message validator
    "validate_message",
    "validate_or_raise",
    "validate_incoming",
    "validated_builder",
    "get_schema",
    "list_message_types",
]

# Backward compatibility aliases
_load_schema = load_schema
_get_validator = get_validator
