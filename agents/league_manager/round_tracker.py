"""Round completion tracker for League Manager.

This module tracks match results for each round and provides a way to
wait for all matches in a round to complete.
"""

import asyncio
from typing import Any, Dict, List, Optional


class RoundTracker:
    """Tracks match completion for rounds.

    This class allows the round execution to wait for all matches to complete
    before proceeding to ROUND_COMPLETED message.
    """

    def __init__(self):
        self._pending_matches: Dict[int, set] = {}  # round_id -> set of match_ids
        self._results: Dict[int, Dict[str, Any]] = {}  # round_id -> {match_id -> result}
        self._events: Dict[int, asyncio.Event] = {}  # round_id -> completion event
        self._lock = asyncio.Lock()

    async def start_round(self, round_id: int, match_ids: List[str]) -> None:
        """Register matches for a round that we're waiting to complete.

        Args:
            round_id: The round number
            match_ids: List of match IDs expected for this round
        """
        async with self._lock:
            self._pending_matches[round_id] = set(match_ids)
            self._results[round_id] = {}
            self._events[round_id] = asyncio.Event()

    async def record_result(
        self, round_id: int, match_id: str, result: Dict[str, Any]
    ) -> None:
        """Record a match result and check if round is complete.

        Args:
            round_id: The round number
            match_id: The match ID
            result: The match result data
        """
        async with self._lock:
            if round_id not in self._pending_matches:
                return

            self._results[round_id][match_id] = result
            self._pending_matches[round_id].discard(match_id)

            # If all matches done, signal completion
            if not self._pending_matches[round_id]:
                self._events[round_id].set()

    async def wait_for_round_complete(
        self, round_id: int, timeout: float = 120.0
    ) -> List[Dict[str, Any]]:
        """Wait for all matches in a round to complete.

        Args:
            round_id: The round number to wait for
            timeout: Maximum seconds to wait

        Returns:
            List of match results for the round
        """
        if round_id not in self._events:
            return []

        try:
            await asyncio.wait_for(self._events[round_id].wait(), timeout=timeout)
        except asyncio.TimeoutError:
            pass  # Return whatever we have

        async with self._lock:
            return list(self._results.get(round_id, {}).values())

    async def get_pending_count(self, round_id: int) -> int:
        """Get count of pending matches for a round."""
        async with self._lock:
            return len(self._pending_matches.get(round_id, set()))

    async def cleanup_round(self, round_id: int) -> None:
        """Clean up tracking data for a completed round."""
        async with self._lock:
            self._pending_matches.pop(round_id, None)
            self._results.pop(round_id, None)
            self._events.pop(round_id, None)


# Module-level singleton
_round_tracker: Optional[RoundTracker] = None


def get_round_tracker() -> RoundTracker:
    """Get the round tracker singleton."""
    global _round_tracker
    if _round_tracker is None:
        _round_tracker = RoundTracker()
    return _round_tracker
