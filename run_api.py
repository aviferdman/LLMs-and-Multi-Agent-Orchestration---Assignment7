#!/usr/bin/env python3
"""Entry point to run the League Competition API server."""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import uvicorn


def main():
    """Run the API server."""
    parser = argparse.ArgumentParser(description="League Competition API Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to (default: 8080)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    args = parser.parse_args()

    print(
        f"""
╔══════════════════════════════════════════════════════════════╗
║           League Competition API Server                       ║
╠══════════════════════════════════════════════════════════════╣
║  Starting server at: http://{args.host}:{args.port}              ║
║  Swagger UI:         http://{args.host}:{args.port}/docs         ║
║  ReDoc:              http://{args.host}:{args.port}/redoc        ║
║  WebSocket:          ws://{args.host}:{args.port}/api/v1/ws/live ║
╚══════════════════════════════════════════════════════════════╝
    """
    )

    uvicorn.run(
        "api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
