"""Launch script for Referee REF02."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generic_referee import create_app
from SHARED.constants import AgentID, Port, SERVER_HOST
import uvicorn

if __name__ == "__main__":
    referee_id = AgentID.REFEREE_02
    port = Port.REFEREE_02
    
    print(f"Starting {referee_id} on port {port}...")
    app = create_app(referee_id, port)
    uvicorn.run(app, host=SERVER_HOST, port=port)
