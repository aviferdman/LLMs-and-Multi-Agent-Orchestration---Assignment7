"""Base contract for all protocol messages."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from SHARED.constants import PROTOCOL_VERSION, Field
from SHARED.protocol_constants import format_sender, generate_conversation_id, generate_timestamp


def create_base_message(
    message_type: str,
    sender_type: str,
    sender_id: str,
    conversation_id: Optional[str] = None,
    **extra_fields: Any,
) -> Dict[str, Any]:
    """Create base protocol message with required fields.

    Args:
        message_type: The message type constant
        sender_type: Entity type ('player', 'referee', 'league_manager', 'launcher')
        sender_id: Entity ID (e.g., 'P01', 'REF01')
        conversation_id: Optional conversation ID (auto-generated if not provided)
        **extra_fields: Additional fields to include in message

    Returns:
        Base message dictionary with all required fields
    """
    msg = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: message_type,
        Field.SENDER: format_sender(sender_type, sender_id),
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
    }
    msg.update(extra_fields)
    return msg


def create_game_message(
    message_type: str,
    sender_type: str,
    sender_id: str,
    league_id: str,
    round_id: int,
    match_id: str,
    conversation_id: Optional[str] = None,
    **extra_fields: Any,
) -> Dict[str, Any]:
    """Create game-context message with league/round/match identifiers.

    Args:
        message_type: The message type constant
        sender_type: Entity type ('player', 'referee', 'league_manager', 'launcher')
        sender_id: Entity ID (e.g., 'P01', 'REF01')
        league_id: League identifier
        round_id: Round number
        match_id: Match identifier
        conversation_id: Optional conversation ID (auto-generated if not provided)
        **extra_fields: Additional fields to include in message

    Returns:
        Game message dictionary with all required fields
    """
    msg = create_base_message(
        message_type=message_type,
        sender_type=sender_type,
        sender_id=sender_id,
        conversation_id=conversation_id,
    )
    msg[Field.LEAGUE_ID] = league_id
    msg[Field.ROUND_ID] = round_id
    msg[Field.MATCH_ID] = match_id
    msg.update(extra_fields)
    return msg


def validate_base_message(message: Dict[str, Any]) -> bool:
    """Validate base message structure.

    Note: This is a basic structural check. For full protocol validation,
    use the schema_validator module.
    """
    required_fields = [
        Field.PROTOCOL,
        Field.MESSAGE_TYPE,
        Field.SENDER,
        Field.TIMESTAMP,
        Field.CONVERSATION_ID,
    ]

    for field in required_fields:
        if field not in message:
            return False

    if message[Field.PROTOCOL] != PROTOCOL_VERSION:
        return False

    if not message[Field.TIMESTAMP].endswith("Z"):
        return False

    return True
