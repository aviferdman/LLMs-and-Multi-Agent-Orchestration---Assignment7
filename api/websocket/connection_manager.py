"""WebSocket connection manager for live updates."""

import json
from datetime import datetime
from typing import Dict, List, Set

from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections for live match updates."""

    def __init__(self):
        """Initialize connection manager."""
        # All active connections
        self.active_connections: List[WebSocket] = []
        # Connections subscribed to specific matches
        self.match_subscriptions: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        # Remove from all match subscriptions
        for subscribers in self.match_subscriptions.values():
            subscribers.discard(websocket)

    def subscribe_to_match(self, websocket: WebSocket, match_id: str):
        """Subscribe a connection to a specific match."""
        if match_id not in self.match_subscriptions:
            self.match_subscriptions[match_id] = set()
        self.match_subscriptions[match_id].add(websocket)

    def unsubscribe_from_match(self, websocket: WebSocket, match_id: str):
        """Unsubscribe a connection from a specific match."""
        if match_id in self.match_subscriptions:
            self.match_subscriptions[match_id].discard(websocket)

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        message["timestamp"] = datetime.utcnow().isoformat() + "Z"
        json_message = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(json_message)
            except Exception:
                pass  # Connection may have closed

    async def broadcast_to_match(self, match_id: str, message: dict):
        """Broadcast a message to clients subscribed to a specific match."""
        message["timestamp"] = datetime.utcnow().isoformat() + "Z"
        message["match_id"] = match_id
        json_message = json.dumps(message)

        subscribers = self.match_subscriptions.get(match_id, set())
        for connection in subscribers:
            try:
                await connection.send_text(json_message)
            except Exception:
                pass

        # Also broadcast to all connections (for dashboard views)
        for connection in self.active_connections:
            if connection not in subscribers:
                try:
                    await connection.send_text(json_message)
                except Exception:
                    pass

    async def send_personal(self, websocket: WebSocket, message: dict):
        """Send a message to a specific client."""
        message["timestamp"] = datetime.utcnow().isoformat() + "Z"
        try:
            await websocket.send_text(json.dumps(message))
        except Exception:
            pass


# Global connection manager instance
manager = ConnectionManager()
