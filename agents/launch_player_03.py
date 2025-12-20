"""Launch script for Player P03 (PatternStrategy)."""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from generic_player import create_app

from SHARED.constants import SERVER_HOST
from SHARED.league_sdk.config_loader import load_agent_config

if __name__ == "__main__":
    agents_config = load_agent_config()
    player_config = agents_config["players"][2]  # P03 is third player

    player_id = player_config["player_id"]
    port = player_config["port"]
    strategy = player_config["strategy"]

    print(f"Starting {player_id} on port {port} with {strategy} strategy...")
    app = create_app(player_id, port, strategy)
    uvicorn.run(app, host=SERVER_HOST, port=port)
