"""Round management contract builders.

Handles round announcement and completion messages.
"""

from typing import Any, Dict, List, Optional

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType
from SHARED.protocol_constants import JSONRPCMethod, generate_conversation_id, generate_timestamp

from .jsonrpc_helpers import wrap_jsonrpc_request


def build_round_announcement(
    league_id: str,
    round_id: int,
    matches: List[Dict[str, Any]],
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build ROUND_ANNOUNCEMENT message.

    Sent by league manager to all agents when a new round begins.
    """
    params = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.ROUND_ANNOUNCEMENT,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        Field.MATCHES: matches,
    }
    return wrap_jsonrpc_request(JSONRPCMethod.ROUND_ANNOUNCEMENT, params, agent_id="LM")


def build_round_completed(
    league_id: str,
    round_id: int,
    matches_completed: int,
    summary: Dict[str, int],
    next_round_id: Optional[int] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build ROUND_COMPLETED message.

    Sent by league manager to players when all matches in round are complete.
    """
    params = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.ROUND_COMPLETED,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        Field.MATCHES_COMPLETED: matches_completed,
        Field.SUMMARY: summary,
    }
    if next_round_id is not None:
        params[Field.NEXT_ROUND_ID] = next_round_id
    return wrap_jsonrpc_request(JSONRPCMethod.ROUND_COMPLETED, params, agent_id="LM")
