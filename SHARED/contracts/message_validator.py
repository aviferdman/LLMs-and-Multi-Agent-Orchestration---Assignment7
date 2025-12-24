"""Message validation functions.

Provides validation for protocol messages against JSON schemas.
"""

import functools
import json
import logging
from typing import Any, Callable, Dict, List, Optional

from SHARED.contracts.exceptions import (
    InvalidMessageError,
    ProtocolValidationError,
    SchemaNotFoundError,
)
from SHARED.contracts.schema_loader import MESSAGE_TYPE_TO_SCHEMA, get_validator, load_schema

logger = logging.getLogger(__name__)


def validate_message(message: Dict[str, Any]) -> List[str]:
    """Validate a message against its JSON schema.

    Args:
        message: The message dictionary to validate

    Returns:
        List of validation error descriptions (empty if valid)
    """
    if not isinstance(message, dict):
        return ["Message must be a dictionary"]

    message_type = message.get("message_type")
    if not message_type:
        return ["Missing required field: message_type"]

    try:
        validator = get_validator(message_type)
    except SchemaNotFoundError:
        logger.warning(f"No schema found for message type: {message_type}")
        return [f"No schema found for message type: {message_type}"]

    errors = []
    for error in validator.iter_errors(message):
        path = ".".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
        errors.append(f"{path}: {error.message}")

    return errors


def validate_or_raise(message: Dict[str, Any]) -> None:
    """Validate a message and raise an exception if invalid."""
    if not isinstance(message, dict):
        raise InvalidMessageError("Message must be a dictionary", message)

    message_type = message.get("message_type")
    if not message_type:
        raise InvalidMessageError("Missing required field: message_type", message)

    errors = validate_message(message)
    if errors:
        raise ProtocolValidationError(message_type, errors, message)


def validate_incoming(
    message: Dict[str, Any], log_errors: bool = True, raise_on_error: bool = False
) -> List[str]:
    """Validate an incoming message (handler-side validation)."""
    errors = validate_message(message)
    if errors:
        message_type = message.get("message_type", "UNKNOWN")
        if log_errors:
            error_summary = "; ".join(errors[:3])
            extra = f" (and {len(errors) - 3} more)" if len(errors) > 3 else ""
            logger.warning(f"Validation failed for {message_type}: {error_summary}{extra}")
        if raise_on_error:
            raise ProtocolValidationError(message_type, errors, message)
    return errors


def validated_builder(func: Callable[..., Dict[str, Any]]) -> Callable[..., Dict[str, Any]]:
    """Decorator that validates builder function output against schema."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        message = func(*args, **kwargs)
        validate_or_raise(message)
        return message

    return wrapper


def get_schema(message_type: str) -> Optional[dict]:
    """Get the JSON schema for a message type."""
    schema_file = MESSAGE_TYPE_TO_SCHEMA.get(message_type)
    if not schema_file:
        return None
    try:
        return load_schema(schema_file)
    except (SchemaNotFoundError, json.JSONDecodeError):
        return None


def list_message_types() -> List[str]:
    """Get list of all message types with defined schemas."""
    return list(MESSAGE_TYPE_TO_SCHEMA.keys())
