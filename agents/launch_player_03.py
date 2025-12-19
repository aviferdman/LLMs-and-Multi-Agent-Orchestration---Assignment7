"""Launch script for Player P03 (PatternStrategy)."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generic_player import create_app
from SHARED.constants import AgentID, Port, StrategyType, SERVER_HOST
import uvicorn

if __name__ == "__main__":
    player_id = AgentID.PLAYER_03
    port = Port.PLAYER_03
    strategy = StrategyType.PATTERN
    
    print(f"Starting {player_id} on port {port} with {strategy} strategy...")
    app = create_app(player_id, port, strategy)
    uvicorn.run(app, host=SERVER_HOST, port=port)
