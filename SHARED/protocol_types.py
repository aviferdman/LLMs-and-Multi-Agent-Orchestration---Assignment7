"""Protocol type definitions and constants.

Contains message types, status codes, and field name enumerations.
"""


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
    CHOOSE_PARITY_RESPONSE = "CHOOSE_PARITY_RESPONSE"
    GAME_OVER = "GAME_OVER"
    # Result reporting (Referee → LM)
    MATCH_RESULT_REPORT = "MATCH_RESULT_REPORT"
    MATCH_RESULT_ACK = "MATCH_RESULT_ACK"
    # Query messages
    LEAGUE_QUERY = "LEAGUE_QUERY"
    LEAGUE_QUERY_RESPONSE = "LEAGUE_QUERY_RESPONSE"
    # Shutdown messages
    SHUTDOWN_COMMAND = "SHUTDOWN_COMMAND"
    SHUTDOWN_ACK = "SHUTDOWN_ACK"
    # Error messages
    LEAGUE_ERROR = "LEAGUE_ERROR"
    GAME_ERROR = "GAME_ERROR"

    # DEPRECATED: Keep for backward compatibility
    PARITY_CHOICE = "CHOOSE_PARITY_RESPONSE"


class Status:
    """Generic status values."""

    OK = "ok"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RECORDED = "recorded"
    ACKNOWLEDGED = "acknowledged"
    ERROR = "error"
    SUCCESS = "success"
    FAILURE = "failure"

    # DEPRECATED
    REGISTERED = "ACCEPTED"


class Timeout:
    """Timeout keys for configuration lookup."""

    GAME_JOIN_ACK = "game_join_ack"
    PARITY_CHOICE = "parity_choice"
    LEAGUE_REGISTER = "league_register"
    HTTP_REQUEST = "http_request"
    AGENT_STARTUP = "agent_startup"
