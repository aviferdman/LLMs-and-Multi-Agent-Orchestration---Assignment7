"""League standings and completion contract builders.

Handles standings updates, league completion, and query messages.
"""

from typing import Any, Dict, List, Optional

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType
from SHARED.protocol_constants import JSONRPCMethod, generate_conversation_id, generate_timestamp

from .jsonrpc_helpers import wrap_jsonrpc_request, wrap_jsonrpc_response


def build_league_completed(
    league_id: str,
    total_rounds: int,
    total_matches: int,
    champion: Dict[str, Any],
    final_standings: List[Dict[str, Any]],
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_COMPLETED message. Sent by LM to all agents when league is finished."""
    params = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_COMPLETED,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.TOTAL_ROUNDS: total_rounds,
        Field.TOTAL_MATCHES: total_matches,
        Field.CHAMPION: champion,
        Field.FINAL_STANDINGS: final_standings,
    }
    return wrap_jsonrpc_request(JSONRPCMethod.LEAGUE_COMPLETED, params, agent_id="LM")


def build_league_standings_update(
    league_id: str,
    round_id: int,
    standings: List[Dict[str, Any]],
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_STANDINGS_UPDATE message. Sent by LM to players after each round."""
    params = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_STANDINGS_UPDATE,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        Field.STANDINGS: standings,
    }
    return wrap_jsonrpc_request(JSONRPCMethod.LEAGUE_STANDINGS_UPDATE, params, agent_id="LM")


def build_league_error(
    error_code: str,
    error_description: str,
    original_message_type: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_ERROR message. Sent by LM when a league-level error occurs."""
    params = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_ERROR,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.ERROR_CODE: error_code,
        Field.ERROR_DESCRIPTION: error_description,
    }
    if original_message_type:
        params[Field.ORIGINAL_MESSAGE_TYPE] = original_message_type
    if context:
        params[Field.CONTEXT] = context
    return wrap_jsonrpc_request(JSONRPCMethod.LEAGUE_ERROR, params, agent_id="LM")


def build_league_query_response(
    query_type: str,
    success: bool,
    data: Optional[Dict[str, Any]] = None,
    conversation_id: Optional[str] = None,
    request_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_QUERY_RESPONSE message. Sent by LM in response to LEAGUE_QUERY."""
    result = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_QUERY_RESPONSE,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.QUERY_TYPE: query_type,
        "success": success,
    }
    if data is not None:
        result[Field.DATA] = data
    if request_id is not None:
        return wrap_jsonrpc_response(result, request_id)
    return wrap_jsonrpc_request(JSONRPCMethod.LEAGUE_QUERY_RESPONSE, result, agent_id="LM")
