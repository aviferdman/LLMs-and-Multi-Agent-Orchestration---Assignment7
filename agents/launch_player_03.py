"""Launch script for Player P03 (PatternStrategy)."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generic_player import create_app
from SHARED.league_sdk.config_loader import load_agent_config
from SHARED.constants import SERVER_HOST
import uvicorn

if __name__ == "__main__":
    agents_config = load_agent_config()
    player_config = agents_config["players"][2]  # P03 is third player
    
    player_id = player_config["player_id"]
    port = player_config["port"]
    strategy = player_config["strategy"]
    
    print(f"Starting {player_id} on port {port} with {strategy} strategy...")
    app = create_app(player_id, port, strategy)
    uvicorn.run(app, host=SERVER_HOST, port=port)
