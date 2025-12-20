"""Protocol and network-related constants."""

# Protocol
PROTOCOL_VERSION = "league.v2"
MCP_PATH = "/mcp"
LOCALHOST = "localhost"
SERVER_HOST = "0.0.0.0"
HTTP_PROTOCOL = "http"


class MessageType:
    """All protocol message types."""

    # Registration messages
    REFEREE_REGISTER_REQUEST = "REFEREE_REGISTER_REQUEST"
    REFEREE_REGISTER_RESPONSE = "REFEREE_REGISTER_RESPONSE"
    LEAGUE_REGISTER_REQUEST = "LEAGUE_REGISTER_REQUEST"
    LEAGUE_REGISTER_RESPONSE = "LEAGUE_REGISTER_RESPONSE"
    # League control messages (Launcher → LM)
    START_LEAGUE = "START_LEAGUE"
    LEAGUE_STATUS = "LEAGUE_STATUS"
    # Round lifecycle messages (LM → All)
    ROUND_ANNOUNCEMENT = "ROUND_ANNOUNCEMENT"
    ROUND_COMPLETED = "ROUND_COMPLETED"
    LEAGUE_COMPLETED = "LEAGUE_COMPLETED"
    LEAGUE_STANDINGS_UPDATE = "LEAGUE_STANDINGS_UPDATE"
    # Match assignment messages (LM → Referee)
    RUN_MATCH = "RUN_MATCH"
    RUN_MATCH_ACK = "RUN_MATCH_ACK"
    # Game flow messages (Referee ↔ Player)
    GAME_INVITATION = "GAME_INVITATION"
    GAME_JOIN_ACK = "GAME_JOIN_ACK"
    CHOOSE_PARITY_CALL = "CHOOSE_PARITY_CALL"
    PARITY_CHOICE = "PARITY_CHOICE"
    GAME_OVER = "GAME_OVER"
    # Result reporting (Referee → LM)
    MATCH_RESULT_REPORT = "MATCH_RESULT_REPORT"
    MATCH_RESULT_ACK = "MATCH_RESULT_ACK"
    # Shutdown messages
    SHUTDOWN_COMMAND = "SHUTDOWN_COMMAND"
    SHUTDOWN_ACK = "SHUTDOWN_ACK"
    # Error messages
    LEAGUE_ERROR = "LEAGUE_ERROR"
    GAME_ERROR = "GAME_ERROR"


class Port:
    """Default port assignments.

    DEPRECATED: Use agents_config.json for port configuration.
    These values are kept for backward compatibility and testing only.
    """

    LEAGUE_MANAGER = 8000
    REFEREE_01 = 8001
    REFEREE_02 = 8002
    PLAYER_01 = 8101
    PLAYER_02 = 8102
    PLAYER_03 = 8103
    PLAYER_04 = 8104


class Endpoint:
    """Default endpoint URLs.

    DEPRECATED: Use agents_config.json for endpoint configuration.
    These values are kept for backward compatibility and testing only.
    """

    LEAGUE_MANAGER = "http://localhost:8000/mcp"
    REFEREE_01 = "http://localhost:8001/mcp"
    REFEREE_02 = "http://localhost:8002/mcp"
    PLAYER_01 = "http://localhost:8101/mcp"
    PLAYER_02 = "http://localhost:8102/mcp"
    PLAYER_03 = "http://localhost:8103/mcp"
    PLAYER_04 = "http://localhost:8104/mcp"


class Timeout:
    """Timeout keys for configuration lookup.

    NOTE: These are now KEY NAMES to be used with system_config.timeouts[key].
    Actual values are defined in SHARED/config/system.json.
    """

    GAME_JOIN_ACK = "game_join_ack"
    PARITY_CHOICE = "parity_choice"
    LEAGUE_REGISTER = "league_register"
    HTTP_REQUEST = "http_request"
    AGENT_STARTUP = "agent_startup"


class Status:
    """Generic status values."""

    OK = "ok"
    REGISTERED = "registered"
    RECORDED = "recorded"
    ACKNOWLEDGED = "acknowledged"
    ERROR = "error"
    SUCCESS = "success"
    FAILURE = "failure"


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
    # Data structure fields
    VERSION = "version"
    MATCHES = "matches"
    STANDINGS = "standings"
    LAST_UPDATED = "last_updated"
    OPPONENT_CHOICES = "opponent_choices"


# Schema versions for data structures
STANDINGS_SCHEMA_VERSION = 1
