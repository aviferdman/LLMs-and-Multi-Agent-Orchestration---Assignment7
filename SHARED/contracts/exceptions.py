"""Custom exceptions for protocol validation.

This module defines exceptions used by the schema validator
to report protocol contract violations.
"""

from typing import List, Optional


class ProtocolValidationError(Exception):
    """Raised when a message fails protocol schema validation.

    Attributes:
        message_type: The message type that failed validation
        errors: List of validation error descriptions
        message_data: The original message that failed validation (optional)
    """

    def __init__(
        self,
        message_type: str,
        errors: List[str],
        message_data: Optional[dict] = None,
    ):
        self.message_type = message_type
        self.errors = errors
        self.message_data = message_data

        # Build user-friendly error message
        error_summary = "; ".join(errors[:5])  # Show first 5 errors
        if len(errors) > 5:
            error_summary += f" (and {len(errors) - 5} more)"

        super().__init__(
            f"Protocol validation failed for {message_type}: {error_summary}"
        )

    def __repr__(self) -> str:
        return (
            f"ProtocolValidationError(message_type={self.message_type!r}, "
            f"errors={self.errors!r})"
        )


class SchemaNotFoundError(Exception):
    """Raised when a schema file cannot be found for a message type."""

    def __init__(self, message_type: str):
        self.message_type = message_type
        super().__init__(f"No schema found for message type: {message_type}")


class InvalidMessageError(Exception):
    """Raised when a message is structurally invalid (missing message_type, etc.)."""

    def __init__(self, reason: str, message_data: Optional[dict] = None):
        self.reason = reason
        self.message_data = message_data
        super().__init__(f"Invalid message: {reason}")
