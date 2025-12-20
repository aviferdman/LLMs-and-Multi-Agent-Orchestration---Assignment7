"""Launch script for Referee REF01."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generic_referee import create_app
from SHARED.league_sdk.config_loader import load_agent_config
from SHARED.constants import SERVER_HOST
import uvicorn

if __name__ == "__main__":
    agents_config = load_agent_config()
    referee_config = agents_config["referees"][0]  # REF01 is first referee
    
    referee_id = referee_config["referee_id"]
    port = referee_config["port"]
    
    print(f"Starting {referee_id} on port {port}...")
    app = create_app(referee_id, port)
    uvicorn.run(app, host=SERVER_HOST, port=port)
