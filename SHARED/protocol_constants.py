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

class Timeout:
    """Timeout values in seconds."""
    GAME_JOIN_ACK = 5
    PARITY_CHOICE = 10
    LEAGUE_REGISTER = 10
    HTTP_REQUEST = 30
    AGENT_STARTUP = 5

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
