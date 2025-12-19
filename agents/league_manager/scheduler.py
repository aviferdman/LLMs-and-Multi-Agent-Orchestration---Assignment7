"""League Manager - Round-robin scheduler."""

from itertools import combinations
from typing import List, Tuple, Dict, Any

def generate_round_robin_schedule(
    players: List[str],
    referees: List[str]
) -> List[List[Dict[str, Any]]]:
    """Generate round-robin schedule for players.
    
    Args:
        players: List of player IDs (4 players)
        referees: List of referee IDs (2 referees)
    
    Returns:
        List of rounds, each containing list of matches
    """
    all_pairings = list(combinations(players, 2))
    schedule = []
    
    # Distribute 6 matches across 3 rounds (2 matches per round)
    for round_num in range(3):
        round_matches = []
        
        # Get 2 matches for this round
        for match_idx in range(2):
            pairing_idx = round_num * 2 + match_idx
            if pairing_idx < len(all_pairings):
                player_a, player_b = all_pairings[pairing_idx]
                referee = referees[match_idx % len(referees)]
                
                match = {
                    "match_id": f"R{round_num + 1}M{match_idx + 1}",
                    "round_id": round_num + 1,
                    "player_a": player_a,
                    "player_b": player_b,
                    "referee_id": referee
                }
                round_matches.append(match)
        
        schedule.append(round_matches)
    
    return schedule

def get_match_schedule() -> List[List[Dict[str, Any]]]:
    """Get predefined match schedule for 4 players."""
    return [
        # Round 1
        [
            {"match_id": "R1M1", "round_id": 1, 
             "player_a": "P01", "player_b": "P02", "referee_id": "REF01"},
            {"match_id": "R1M2", "round_id": 1,
             "player_a": "P03", "player_b": "P04", "referee_id": "REF02"}
        ],
        # Round 2
        [
            {"match_id": "R2M1", "round_id": 2,
             "player_a": "P03", "player_b": "P01", "referee_id": "REF01"},
            {"match_id": "R2M2", "round_id": 2,
             "player_a": "P04", "player_b": "P02", "referee_id": "REF02"}
        ],
        # Round 3
        [
            {"match_id": "R3M1", "round_id": 3,
             "player_a": "P04", "player_b": "P01", "referee_id": "REF01"},
            {"match_id": "R3M2", "round_id": 3,
             "player_a": "P03", "player_b": "P02", "referee_id": "REF02"}
        ]
    ]
