"""Registration contract builders.

Handles referee and player registration messages.
"""

from typing import Any, Dict, List, Optional

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, Status
from SHARED.protocol_constants import (
    JSONRPCMethod,
    format_sender,
    generate_conversation_id,
    generate_timestamp,
)

from .jsonrpc_helpers import wrap_jsonrpc_request, wrap_jsonrpc_response


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
    params = {
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
    return wrap_jsonrpc_request(JSONRPCMethod.REGISTER_REFEREE, params, agent_id=referee_id)


def build_referee_register_response(
    referee_id: str,
    status: str = Status.ACCEPTED,
    reason: Optional[str] = None,
    conversation_id: Optional[str] = None,
    request_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Build REFEREE_REGISTER_RESPONSE message."""
    result = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.REFEREE_REGISTER_RESPONSE,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.STATUS: status,
        Field.REFEREE_ID: referee_id,
    }
    if reason:
        result[Field.REASON] = reason
    if request_id is not None:
        return wrap_jsonrpc_response(result, request_id)
    return wrap_jsonrpc_request(JSONRPCMethod.REGISTER_REFEREE_RESPONSE, result, agent_id="LM")


def build_league_register_request(
    player_id: str,
    display_name: str,
    version: str,
    contact_endpoint: str,
    game_types: Optional[List[str]] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_REGISTER_REQUEST message."""
    params = {
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
    return wrap_jsonrpc_request(JSONRPCMethod.REGISTER_PLAYER, params, agent_id=player_id)


def build_league_register_response(
    player_id: str,
    status: str = Status.ACCEPTED,
    reason: Optional[str] = None,
    conversation_id: Optional[str] = None,
    request_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_REGISTER_RESPONSE message."""
    result = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_REGISTER_RESPONSE,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.STATUS: status,
        Field.PLAYER_ID: player_id,
    }
    if reason:
        result[Field.REASON] = reason
    if request_id is not None:
        return wrap_jsonrpc_response(result, request_id)
    return wrap_jsonrpc_request(JSONRPCMethod.REGISTER_PLAYER_RESPONSE, result, agent_id="LM")
