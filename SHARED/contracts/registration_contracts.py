"""Registration contract builders.

Handles referee and player registration messages.
"""

from typing import Any, Dict, List, Optional

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, Status
from SHARED.protocol_constants import (
    format_sender,
    generate_conversation_id,
    generate_timestamp,
)


def build_referee_register_request(
    referee_id: str,
    display_name: str,
    version: str,
    contact_endpoint: str,
    game_types: Optional[List[str]] = None,
    max_concurrent_matches: int = 1,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build REFEREE_REGISTER_REQUEST message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.REFEREE_REGISTER_REQUEST,
        Field.SENDER: format_sender("referee", referee_id),
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.REFEREE_META: {
            Field.DISPLAY_NAME: display_name,
            Field.VERSION: version,
            Field.GAME_TYPES: game_types or ["even_odd"],
            Field.CONTACT_ENDPOINT: contact_endpoint,
            Field.MAX_CONCURRENT_MATCHES: max_concurrent_matches,
        },
    }


def build_referee_register_response(
    referee_id: str,
    status: str = Status.ACCEPTED,
    reason: Optional[str] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build REFEREE_REGISTER_RESPONSE message."""
    msg = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.REFEREE_REGISTER_RESPONSE,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.STATUS: status,
        Field.REFEREE_ID: referee_id,
    }
    if reason:
        msg[Field.REASON] = reason
    return msg


def build_league_register_request(
    player_id: str,
    display_name: str,
    version: str,
    contact_endpoint: str,
    game_types: Optional[List[str]] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_REGISTER_REQUEST message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_REGISTER_REQUEST,
        Field.SENDER: format_sender("player", player_id),
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.PLAYER_META: {
            Field.DISPLAY_NAME: display_name,
            Field.VERSION: version,
            Field.GAME_TYPES: game_types or ["even_odd"],
            Field.CONTACT_ENDPOINT: contact_endpoint,
        },
    }


def build_league_register_response(
    player_id: str,
    status: str = Status.ACCEPTED,
    reason: Optional[str] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_REGISTER_RESPONSE message."""
    msg = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_REGISTER_RESPONSE,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.STATUS: status,
        Field.PLAYER_ID: player_id,
    }
    if reason:
        msg[Field.REASON] = reason
    return msg
