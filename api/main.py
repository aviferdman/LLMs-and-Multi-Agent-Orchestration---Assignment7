"""Main FastAPI application for League Competition API."""

import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from api.routes import games_router, league_router, matches_router, players_router
from api.websocket.connection_manager import manager

# Create FastAPI app with OpenAPI configuration
app = FastAPI(
    title="League Competition API",
    description="""
## League Competition REST API

A comprehensive API for managing AI agent league competitions.

### Features
- **League Management**: Start, monitor, and control leagues
- **Game Selection**: Browse available games with rules
- **Live Updates**: Real-time match progress via WebSocket
- **Player Stats**: Track player performance and history

### WebSocket
Connect to `/api/v1/ws/live` for real-time match updates.

Events:
- `player_thinking` - Player is deciding their move
- `player_move` - Player submitted their strategy
- `round_result` - Round outcome revealed
- `match_start` / `match_end` - Match lifecycle events
    """,
    version="1.0.0",
    contact={
        "name": "League Admin",
        "email": "admin@league.local",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {"name": "League", "description": "League management operations"},
        {"name": "Games", "description": "Available games and rules"},
        {"name": "Matches", "description": "Match information and live state"},
        {"name": "Players", "description": "Player statistics and history"},
        {"name": "WebSocket", "description": "Real-time live updates"},
    ],
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api/v1 prefix
API_PREFIX = "/api/v1"
app.include_router(league_router, prefix=API_PREFIX)
app.include_router(games_router, prefix=API_PREFIX)
app.include_router(matches_router, prefix=API_PREFIX)
app.include_router(players_router, prefix=API_PREFIX)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "league-api", "version": "1.0.0"}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API info."""
    return {
        "message": "League Competition API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.websocket("/api/v1/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for live match updates.

    Connect to receive real-time events:
    - player_thinking: Player is deciding
    - player_move: Player submitted move (shown immediately)
    - round_result: Round outcome
    - match_start/match_end: Match lifecycle

    Send JSON to subscribe to specific match:
    {"action": "subscribe", "match_id": "match_123"}
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                action = message.get("action")

                if action == "subscribe":
                    match_id = message.get("match_id")
                    if match_id:
                        manager.subscribe_to_match(websocket, match_id)
                        await manager.send_personal(
                            websocket,
                            {"event_type": "subscribed", "match_id": match_id},
                        )

                elif action == "unsubscribe":
                    match_id = message.get("match_id")
                    if match_id:
                        manager.unsubscribe_from_match(websocket, match_id)

                elif action == "ping":
                    await manager.send_personal(websocket, {"event_type": "pong"})

            except json.JSONDecodeError:
                await manager.send_personal(
                    websocket, {"event_type": "error", "message": "Invalid JSON"}
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
