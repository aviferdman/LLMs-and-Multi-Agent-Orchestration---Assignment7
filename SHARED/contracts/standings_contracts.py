"""League standings and completion contract builders.

Handles standings updates, league completion, and query messages.
"""

from typing import Any, Dict, List, Optional

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType
from SHARED.protocol_constants import generate_conversation_id, generate_timestamp


def build_league_completed(
    league_id: str,
    total_rounds: int,
    total_matches: int,
    champion: Dict[str, Any],
    final_standings: List[Dict[str, Any]],
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_COMPLETED message.

    Sent by league manager to all agents when league is finished.

    Args:
        league_id: League identifier
        total_rounds: Total rounds played
        total_matches: Total matches played
        champion: Champion info with:
            - player_id: Champion player ID
            - display_name: Champion display name (optional)
            - points: Champion's total points
        final_standings: List of standing entries with rank, player_id, points
        conversation_id: Optional conversation ID

    Returns:
        LEAGUE_COMPLETED message dictionary
    """
    return {
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


def build_league_standings_update(
    league_id: str,
    round_id: int,
    standings: List[Dict[str, Any]],
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_STANDINGS_UPDATE message.

    Sent by league manager to players after each round completion.

    Args:
        league_id: League identifier
        round_id: Round number after which standings are updated
        standings: List of standing entries with rank, player_id, etc.
        conversation_id: Optional conversation ID

    Returns:
        LEAGUE_STANDINGS_UPDATE message dictionary
    """
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_STANDINGS_UPDATE,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        Field.STANDINGS: standings,
    }


def build_league_error(
    error_code: str,
    error_description: str,
    original_message_type: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_ERROR message.

    Sent by league manager when a league-level error occurs.

    Args:
        error_code: Error code (e.g., 'E012')
        error_description: Error description (e.g., 'AUTH_TOKEN_INVALID')
        original_message_type: Message type that caused the error
        context: Additional error context
        conversation_id: Optional conversation ID

    Returns:
        LEAGUE_ERROR message dictionary
    """
    msg = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_ERROR,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.ERROR_CODE: error_code,
        Field.ERROR_DESCRIPTION: error_description,
    }
    if original_message_type:
        msg[Field.ORIGINAL_MESSAGE_TYPE] = original_message_type
    if context:
        msg[Field.CONTEXT] = context
    return msg


def build_league_query_response(
    query_type: str,
    success: bool,
    data: Optional[Dict[str, Any]] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_QUERY_RESPONSE message.

    Sent by league manager in response to LEAGUE_QUERY.

    Args:
        query_type: Echo of the query type requested
        success: Whether the query was successful
        data: Query result data (None if query failed)
        conversation_id: Optional conversation ID

    Returns:
        LEAGUE_QUERY_RESPONSE message dictionary
    """
    msg = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_QUERY_RESPONSE,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.QUERY_TYPE: query_type,
        "success": success,
    }
    if data is not None:
        msg[Field.DATA] = data
    return msg
