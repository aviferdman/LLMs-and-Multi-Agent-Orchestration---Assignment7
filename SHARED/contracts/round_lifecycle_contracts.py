"""Round lifecycle contract builders for League Manager."""

from typing import Any, Dict

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType


def build_round_announcement(
    league_id: str, round_id: int, total_rounds: int, matches: list
) -> Dict[str, Any]:
    """Build ROUND_ANNOUNCEMENT message (LM → All agents)."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.ROUND_ANNOUNCEMENT,
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        "total_rounds": total_rounds,
        "matches": matches,
    }


def build_round_completed(league_id: str, round_id: int, results: list) -> Dict[str, Any]:
    """Build ROUND_COMPLETED message (LM → All agents)."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.ROUND_COMPLETED,
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        "results": results,
    }


def build_league_completed(
    league_id: str, final_standings: list, total_matches: int
) -> Dict[str, Any]:
    """Build LEAGUE_COMPLETED message (LM → All agents)."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_COMPLETED,
        Field.LEAGUE_ID: league_id,
        "final_standings": final_standings,
        "total_matches": total_matches,
    }


def build_league_standings_update(league_id: str, round_id: int, standings: list) -> Dict[str, Any]:
    """Build LEAGUE_STANDINGS_UPDATE message (LM → All agents)."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_STANDINGS_UPDATE,
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        "standings": standings,
    }


def build_league_error(
    league_id: str, error_code: str, error_message: str, details: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Build LEAGUE_ERROR message."""
    msg = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_ERROR,
        Field.LEAGUE_ID: league_id,
        "error_code": error_code,
        "error_message": error_message,
    }
    if details:
        msg["details"] = details
    return msg
