"""Centralized constants - re-exports from split modules.

All hardcoded strings should be imported from this file.
DO NOT use string literals directly in code.
"""

# Re-export all agent and game constants
from SHARED.agent_constants import (EVEN_ODD_MAX_NUMBER, EVEN_ODD_MIN_NUMBER,
                                    AgentID, AgentType, Directory, FileName,
                                    GameID, GameStatus, LeagueID, LogEvent,
                                    ParityChoice, Points, StrategyType, Winner)
# Re-export all protocol and network constants
from SHARED.protocol_constants import (HTTP_PROTOCOL, LOCALHOST, MCP_PATH,
                                       PROTOCOL_VERSION, SERVER_HOST,
                                       STANDINGS_SCHEMA_VERSION, Endpoint,
                                       Field, MessageType, Port, Status,
                                       Timeout)

__all__ = [
    # Protocol constants
    "PROTOCOL_VERSION",
    "MCP_PATH",
    "LOCALHOST",
    "SERVER_HOST",
    "HTTP_PROTOCOL",
    "STANDINGS_SCHEMA_VERSION",
    "MessageType",
    "Port",
    "Endpoint",
    "Timeout",
    "Status",
    "Field",
    # Agent constants
    "AgentID",
    "LeagueID",
    "GameID",
    "GameStatus",
    "ParityChoice",
    "Winner",
    "EVEN_ODD_MIN_NUMBER",
    "EVEN_ODD_MAX_NUMBER",
    "StrategyType",
    "AgentType",
    "Directory",
    "FileName",
    "LogEvent",
    "Points",
]
