"""Centralized constants for the entire system.

All hardcoded strings should be imported from this file.
DO NOT use string literals directly in code.
"""

# ============================================================================
# PROTOCOL CONSTANTS
# ============================================================================

PROTOCOL_VERSION = "league.v2"

# Message Types
class MessageType:
    """All protocol message types."""
    REFEREE_REGISTER_REQUEST = "REFEREE_REGISTER_REQUEST"
    REFEREE_REGISTER_RESPONSE = "REFEREE_REGISTER_RESPONSE"
    LEAGUE_REGISTER_REQUEST = "LEAGUE_REGISTER_REQUEST"
    LEAGUE_REGISTER_RESPONSE = "LEAGUE_REGISTER_RESPONSE"
    GAME_INVITATION = "GAME_INVITATION"
    GAME_JOIN_ACK = "GAME_JOIN_ACK"
    CHOOSE_PARITY_CALL = "CHOOSE_PARITY_CALL"
    PARITY_CHOICE = "PARITY_CHOICE"
    GAME_OVER = "GAME_OVER"
    MATCH_RESULT_REPORT = "MATCH_RESULT_REPORT"
    MATCH_RESULT_ACK = "MATCH_RESULT_ACK"

# ============================================================================
# AGENT IDS
# ============================================================================

class AgentID:
    """All agent identifiers."""
    LEAGUE_MANAGER = "LM01"
    REFEREE_01 = "REF01"
    REFEREE_02 = "REF02"
    PLAYER_01 = "P01"
    PLAYER_02 = "P02"
    PLAYER_03 = "P03"
    PLAYER_04 = "P04"

# ============================================================================
# NETWORK CONSTANTS
# ============================================================================

class Port:
    """Default port assignments."""
    LEAGUE_MANAGER = 8000
    REFEREE_01 = 8001
    REFEREE_02 = 8002
    PLAYER_01 = 8101
    PLAYER_02 = 8102
    PLAYER_03 = 8103
    PLAYER_04 = 8104

class Endpoint:
    """Default endpoint URLs."""
    LEAGUE_MANAGER = "http://localhost:8000/mcp"
    REFEREE_01 = "http://localhost:8001/mcp"
    REFEREE_02 = "http://localhost:8002/mcp"
    PLAYER_01 = "http://localhost:8101/mcp"
    PLAYER_02 = "http://localhost:8102/mcp"
    PLAYER_03 = "http://localhost:8103/mcp"
    PLAYER_04 = "http://localhost:8104/mcp"

MCP_PATH = "/mcp"
LOCALHOST = "localhost"
HTTP_PROTOCOL = "http"

# ============================================================================
# LEAGUE & GAME CONSTANTS
# ============================================================================

class LeagueID:
    """League identifiers."""
    EVEN_ODD_2025 = "league_2025_even_odd"

class GameID:
    """Game type identifiers."""
    EVEN_ODD = "even_odd"

class GameStatus:
    """Game/Match status values."""
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    COLLECTING_CHOICES = "COLLECTING_CHOICES"
    DRAWING_NUMBER = "DRAWING_NUMBER"
    FINISHED = "FINISHED"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# ============================================================================
# GAME RULES CONSTANTS
# ============================================================================

class ParityChoice:
    """Parity choices in Even-Odd game."""
    EVEN = "EVEN"
    ODD = "ODD"

class Winner:
    """Winner designation values."""
    PLAYER_A = "PLAYER_A"
    PLAYER_B = "PLAYER_B"
    DRAW = "DRAW"

# Game parameters
EVEN_ODD_MIN_NUMBER = 1
EVEN_ODD_MAX_NUMBER = 10

# ============================================================================
# STRATEGY CONSTANTS
# ============================================================================

class StrategyType:
    """Player strategy types."""
    RANDOM = "random"
    FREQUENCY = "frequency"
    PATTERN = "pattern"

# ============================================================================
# TIMEOUT CONSTANTS
# ============================================================================

class Timeout:
    """Timeout values in seconds."""
    GAME_JOIN_ACK = 5
    PARITY_CHOICE = 30
    LEAGUE_REGISTER = 10
    HTTP_REQUEST = 30
    AGENT_STARTUP = 15

# ============================================================================
# STATUS CONSTANTS
# ============================================================================

class Status:
    """Generic status values."""
    OK = "ok"
    REGISTERED = "registered"
    RECORDED = "recorded"
    ACKNOWLEDGED = "acknowledged"
    ERROR = "error"
    SUCCESS = "success"
    FAILURE = "failure"

# ============================================================================
# DIRECTORY PATHS
# ============================================================================

class Directory:
    """Standard directory names."""
    CONFIG = "config"
    DATA = "data"
    LOGS = "logs"
    AGENTS = "agents"
    LEAGUES = "leagues"
    GAMES = "games"
    MATCHES = "matches"
    PLAYERS = "players"
    SHARED = "SHARED"
    TESTS = "tests"
    DOC = "doc"

# ============================================================================
# FILE NAMES
# ============================================================================

class FileName:
    """Standard file names."""
    SYSTEM_CONFIG = "system.json"
    AGENTS_CONFIG = "agents_config.json"
    GAMES_REGISTRY = "games_registry.json"
    STANDINGS = "standings.json"

# ============================================================================
# LOG EVENT TYPES
# ============================================================================

class LogEvent:
    """Logging event types."""
    STARTUP = "STARTUP"
    SHUTDOWN = "SHUTDOWN"
    RECEIVED = "RECEIVED"
    SENT = "SENT"
    ERROR = "ERROR"
    MATCH_START = "MATCH_START"
    MATCH_COMPLETE = "MATCH_COMPLETE"
    GAME_INVITATION_RECEIVED = "GAME_INVITATION_RECEIVED"
    PARITY_CHOICE_MADE = "PARITY_CHOICE_MADE"
    GAME_OVER_RECEIVED = "GAME_OVER_RECEIVED"
    REFEREE_REGISTERED = "REFEREE_REGISTERED"
    PLAYER_REGISTERED = "PLAYER_REGISTERED"
    MATCH_RESULT = "MATCH_RESULT"
    TIMEOUT = "TIMEOUT"
    REQUEST_ERROR = "REQUEST_ERROR"
    DUPLICATE_REGISTRATION = "DUPLICATE_REGISTRATION"

# ============================================================================
# SCORING CONSTANTS
# ============================================================================

class Points:
    """Point values for match outcomes."""
    WIN = 3
    DRAW = 1
    LOSS = 0

# ============================================================================
# FIELD NAMES
# ============================================================================

class Field:
    """JSON field names for protocol messages."""
    PROTOCOL = "protocol"
    MESSAGE_TYPE = "message_type"
    LEAGUE_ID = "league_id"
    ROUND_ID = "round_id"
    MATCH_ID = "match_id"
    CONVERSATION_ID = "conversation_id"
    SENDER = "sender"
    TIMESTAMP = "timestamp"
    PLAYER_ID = "player_id"
    REFEREE_ID = "referee_id"
    OPPONENT_ID = "opponent_id"
    ENDPOINT = "endpoint"
    AUTH_TOKEN = "auth_token"
    STATUS = "status"
    CHOICE = "choice"
    WINNER = "winner"
    DRAWN_NUMBER = "drawn_number"
    PLAYER_A = "player_a"
    PLAYER_B = "player_b"
    PLAYER_A_CHOICE = "player_a_choice"
    PLAYER_B_CHOICE = "player_b_choice"
