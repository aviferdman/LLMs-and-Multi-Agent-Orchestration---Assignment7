"""Round management contract builders.

Handles round announcement and completion messages.
"""

from typing import Any, Dict, List, Optional

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType
from SHARED.protocol_constants import generate_conversation_id, generate_timestamp


def build_round_announcement(
    league_id: str,
    round_id: int,
    matches: List[Dict[str, Any]],
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build ROUND_ANNOUNCEMENT message.

    Sent by league manager to all agents when a new round begins.

    Args:
        league_id: League identifier
        round_id: Round number (1-based)
        matches: List of match objects with:
            - match_id: Match identifier
            - game_type: Type of game
            - player_A_id: Player A identifier
            - player_B_id: Player B identifier
            - referee_endpoint: Referee HTTP endpoint
        conversation_id: Optional conversation ID

    Returns:
        ROUND_ANNOUNCEMENT message dictionary
    """
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.ROUND_ANNOUNCEMENT,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        Field.MATCHES: matches,
    }


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

    Args:
        league_id: League identifier
        round_id: Completed round number
        matches_completed: Number of matches completed
        summary: Round summary with:
            - total_matches: Total matches in round
            - wins: Number of decisive wins
            - draws: Number of draws
            - technical_losses: Number of technical losses
        next_round_id: Next round number (None if league completed)
        conversation_id: Optional conversation ID

    Returns:
        ROUND_COMPLETED message dictionary
    """
    msg = {
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
        msg[Field.NEXT_ROUND_ID] = next_round_id
    return msg
