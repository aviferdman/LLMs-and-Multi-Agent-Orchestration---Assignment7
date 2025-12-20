"""Base contract for all protocol messages."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from SHARED.constants import PROTOCOL_VERSION, Field


def create_base_message(
    message_type: str,
    league_id: str,
    round_id: int,
    match_id: str,
    sender: str,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create base protocol message with required fields."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: message_type,
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        Field.MATCH_ID: match_id,
        Field.CONVERSATION_ID: conversation_id or str(uuid.uuid4()),
        Field.SENDER: sender,
        Field.TIMESTAMP: datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
    }


def validate_base_message(message: Dict[str, Any]) -> bool:
    """Validate base message structure."""
    required_fields = [
        Field.PROTOCOL,
        Field.MESSAGE_TYPE,
        Field.LEAGUE_ID,
        Field.ROUND_ID,
        Field.MATCH_ID,
        Field.CONVERSATION_ID,
        Field.SENDER,
        Field.TIMESTAMP,
    ]

    for field in required_fields:
        if field not in message:
            return False

    if message[Field.PROTOCOL] != PROTOCOL_VERSION:
        return False

    if not message[Field.TIMESTAMP].endswith("Z"):
        return False

    return True
