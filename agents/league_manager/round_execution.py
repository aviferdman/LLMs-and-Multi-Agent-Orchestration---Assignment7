"""Round execution logic for League Manager."""

import asyncio
from typing import Any, Dict, List

from agents.league_manager.broadcast import broadcast_to_agents
from agents.league_manager.round_tracker import get_round_tracker
from agents.league_manager.scheduler import get_match_schedule

from SHARED.constants import Field, GameID, Winner
from SHARED.contracts import (
    build_round_announcement,
    build_round_completed,
    build_league_standings_update,
)
from SHARED.league_sdk.repositories import StandingsRepository


async def execute_round(
    round_num: int,
    total_rounds: int,
    round_matches: list,
    league_config,
    registered_players,
    registered_referees,
    logger,
    state,
) -> List[Dict[str, Any]]:
    """Execute a single round of matches.

    New flow (per CONTRACTS.md):
    1. Send ROUND_ANNOUNCEMENT to all agents (referees identify their matches)
    2. Referees self-start matches based on referee_endpoint
    3. Wait for MATCH_RESULT_REPORT from referees (tracked via round_tracker)
    4. Send ROUND_COMPLETED when all matches done
    """
    # Assign matches to referees (round-robin)
    referee_list = list(registered_referees.items())
    matches_with_referees = []
    for i, match in enumerate(round_matches):
        ref_id, ref_info = referee_list[i % len(referee_list)]
        referee_endpoint = ref_info.get("endpoint", "")
        matches_with_referees.append({
            "match_id": match["match_id"],
            "player_A_id": match["player_a"],
            "player_B_id": match["player_b"],
            "game_type": GameID.EVEN_ODD,
            "referee_endpoint": referee_endpoint,
        })

    # Register expected matches with round tracker
    tracker = get_round_tracker()
    match_ids = [m["match_id"] for m in matches_with_referees]
    await tracker.start_round(round_num, match_ids)

    # Build and send ROUND_ANNOUNCEMENT
    announcement = build_round_announcement(
        league_id=league_config.league_id,
        round_id=round_num,
        matches=matches_with_referees,
    )
    await broadcast_to_agents(
        announcement, registered_players, registered_referees, logger
    )
    logger.log_message("ROUND_ANNOUNCEMENT_SENT", {"round": round_num, "matches": len(match_ids)})

    # Wait for all match results (referees send MATCH_RESULT_REPORT)
    # Timeout set to 60 seconds per match to be safe
    timeout = 60.0 * len(match_ids)
    current_round_results = await tracker.wait_for_round_complete(round_num, timeout=timeout)

    logger.log_message(
        "ROUND_MATCHES_COMPLETED",
        {"round": round_num, "results_received": len(current_round_results)},
    )

    # Update state
    state["matches_completed"] += len(current_round_results)

    # Clean up tracker
    await tracker.cleanup_round(round_num)

    # Send ROUND_COMPLETED and STANDINGS_UPDATE
    await send_round_completed(
        round_num,
        total_rounds,
        current_round_results,
        league_config,
        registered_players,
        registered_referees,
        logger,
    )
    return current_round_results


async def send_round_completed(
    round_num: int,
    total_rounds: int,
    results: list,
    league_config,
    registered_players,
    registered_referees,
    logger,
):
    """Send ROUND_COMPLETED and STANDINGS_UPDATE messages."""
    try:
        # Compute summary
        summary = {
            "total_matches": len(results),
            "completed_matches": len([r for r in results if r.get("winner")]),
            "draws": len([r for r in results if r.get("winner") == Winner.DRAW]),
        }
        # Determine next round id
        next_round_id = round_num + 1 if round_num < total_rounds else None
        completed_msg = build_round_completed(
            league_id=league_config.league_id,
            round_id=round_num,
            matches_completed=len(results),
            summary=summary,
            next_round_id=next_round_id,
        )
        await broadcast_to_agents(
            completed_msg, registered_players, registered_referees, logger
        )
        logger.log_message("ROUND_COMPLETED_SENT", {"round": round_num})
        standings_repo = StandingsRepository(league_config.league_id)
        standings_data = standings_repo.load()
        standings_list = standings_data.get("standings", [])
        standings_list.sort(key=lambda x: (-x.get("points", 0), -x.get("wins", 0)))
        standings_update = build_league_standings_update(
            league_id=league_config.league_id,
            round_id=round_num,
            standings=standings_list,
        )
        await broadcast_to_agents(
            standings_update, registered_players, registered_referees, logger
        )
        logger.log_message("STANDINGS_UPDATE_SENT", {"round": round_num})
    except Exception as e:
        logger.log_error("SEND_ROUND_COMPLETED_ERROR", f"{type(e).__name__}: {e}")
