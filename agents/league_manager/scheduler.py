"""League Manager - Round-robin scheduler.

Uses itertools.combinations to generate all unique player pairings,
then distributes matches across rounds dynamically.
"""

from itertools import combinations
from math import ceil
from typing import Any, Dict, List, Optional

from SHARED.constants import AgentID

# Re-export RoundState for backward compatibility
from agents.league_manager.round_state import RoundState, check_round_complete, start_round


def create_all_pairings(players: List[str]) -> List[tuple]:
    """Generate all unique player pairings using combinations.

    Args:
        players: List of player IDs

    Returns:
        List of tuples, each containing two player IDs
    """
    return list(combinations(players, 2))


def generate_round_robin_schedule(
    players: List[str],
    referees: List[str],
    matches_per_round: Optional[int] = None,
) -> List[List[Dict[str, Any]]]:
    """Generate round-robin schedule for any number of players.

    Creates all unique pairings using itertools.combinations and distributes
    them across rounds. The number of matches per round defaults to half the
    number of players (allowing parallel matches without player conflicts).

    Args:
        players: List of player IDs (any number >= 2)
        referees: List of referee IDs (at least 1)
        matches_per_round: Optional override for matches per round.
                          Defaults to len(players) // 2

    Returns:
        List of rounds, each containing list of match dictionaries
    """
    if len(players) < 2:
        return []

    if not referees:
        raise ValueError("At least one referee is required")

    # Generate all unique pairings
    all_pairings = create_all_pairings(players)
    total_matches = len(all_pairings)

    # Default: half the players can play simultaneously
    if matches_per_round is None:
        matches_per_round = max(1, len(players) // 2)

    # Calculate number of rounds needed
    num_rounds = ceil(total_matches / matches_per_round)

    schedule = []
    match_idx = 0

    for round_num in range(num_rounds):
        round_matches = []

        # Assign matches to this round
        for match_in_round in range(matches_per_round):
            if match_idx >= total_matches:
                break

            player_a, player_b = all_pairings[match_idx]
            referee = referees[match_in_round % len(referees)]

            match = {
                "match_id": f"R{round_num + 1}M{match_in_round + 1}",
                "round_id": round_num + 1,
                "player_a": player_a,
                "player_b": player_b,
                "referee_id": referee,
            }
            round_matches.append(match)
            match_idx += 1

        if round_matches:
            schedule.append(round_matches)

    return schedule


def get_match_schedule(
    players: Optional[List[str]] = None,
    referees: Optional[List[str]] = None,
) -> List[List[Dict[str, Any]]]:
    """Get match schedule for the given players and referees.

    This is a convenience wrapper around generate_round_robin_schedule.
    If no players/referees provided, uses default 4 players and 2 referees
    for backward compatibility.

    Args:
        players: List of player IDs. Defaults to [P01, P02, P03, P04]
        referees: List of referee IDs. Defaults to [REF01, REF02]

    Returns:
        List of rounds, each containing list of match dictionaries
    """
    if players is None:
        players = [AgentID.PLAYER_01, AgentID.PLAYER_02, AgentID.PLAYER_03, AgentID.PLAYER_04]
    if referees is None:
        referees = [AgentID.REFEREE_01, AgentID.REFEREE_02]

    return generate_round_robin_schedule(players, referees)
