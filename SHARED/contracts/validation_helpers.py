"""Validation helper functions for message processing.

This module provides utility functions for validating incoming messages.
"""

import functools
import logging
from typing import Any, Callable, Dict, List

from SHARED.contracts.exceptions import ProtocolValidationError

logger = logging.getLogger(__name__)


def validate_incoming(
    message: Dict[str, Any],
    validator_func: Callable[[Dict[str, Any]], List[str]],
    log_errors: bool = True,
    raise_on_error: bool = False,
) -> List[str]:
    """Validate an incoming message (handler-side validation).

    This is a gentler validation that logs warnings but allows
    processing to continue by default.

    Args:
        message: The incoming message to validate
        validator_func: Function that returns list of validation errors
        log_errors: Whether to log validation errors as warnings
        raise_on_error: Whether to raise exception on validation failure

    Returns:
        List of validation errors (empty if valid)

    Raises:
        ProtocolValidationError: If raise_on_error=True and validation fails
    """
    errors = validator_func(message)

    if errors:
        message_type = message.get("message_type", "UNKNOWN")
        if log_errors:
            logger.warning(
                f"Incoming message validation failed for {message_type}: "
                f"{'; '.join(errors[:3])}"
                + (f" (and {len(errors) - 3} more)" if len(errors) > 3 else "")
            )
        if raise_on_error:
            raise ProtocolValidationError(message_type, errors, message)

    return errors


def validated_builder(
    validator_func: Callable[[Dict[str, Any]], None]
) -> Callable[[Callable[..., Dict[str, Any]]], Callable[..., Dict[str, Any]]]:
    """Decorator factory that validates builder function output.

    Use this decorator on message builder functions to ensure all
    outgoing messages conform to the protocol schema.

    Args:
        validator_func: Function that validates and raises on error

    Returns:
        Decorator function
    """

    def decorator(func: Callable[..., Dict[str, Any]]) -> Callable[..., Dict[str, Any]]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Dict[str, Any]:
            message = func(*args, **kwargs)
            validator_func(message)
            return message

        return wrapper

    return decorator
