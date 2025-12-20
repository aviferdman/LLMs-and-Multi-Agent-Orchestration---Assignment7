"""Launch script for Player P05 (TimeoutStrategy) - for testing timeout edge cases.

This player deliberately times out on every move, testing:
1. Referee timeout handling
2. Automatic loss assignment for timed-out player
3. Match continuation when one player fails

Usage:
    python agents/launch_player_timeout.py

The player will register with the league manager and participate in matches,
but will always lose due to exceeding the parity_choice timeout.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from generic_player import create_app

from SHARED.constants import SERVER_HOST, StrategyType

# Timeout player configuration (not in agents_config.json, used for testing only)
TIMEOUT_PLAYER_ID = "P05"
TIMEOUT_PLAYER_PORT = 8105
TIMEOUT_PLAYER_STRATEGY = StrategyType.TIMEOUT

if __name__ == "__main__":
    print(f"Starting {TIMEOUT_PLAYER_ID} on port {TIMEOUT_PLAYER_PORT} with {TIMEOUT_PLAYER_STRATEGY} strategy...")
    print("WARNING: This player will timeout on every move and always lose!")
    app = create_app(TIMEOUT_PLAYER_ID, TIMEOUT_PLAYER_PORT, TIMEOUT_PLAYER_STRATEGY)
    uvicorn.run(app, host=SERVER_HOST, port=TIMEOUT_PLAYER_PORT)
