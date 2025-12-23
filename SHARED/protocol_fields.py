"""Protocol field name definitions.

Contains JSON field names for protocol messages.
"""


class Field:
    """JSON field names for protocol messages."""

    # Base message fields
    PROTOCOL = "protocol"
    MESSAGE_TYPE = "message_type"
    SENDER = "sender"
    TIMESTAMP = "timestamp"
    CONVERSATION_ID = "conversation_id"

    # Identifiers
    LEAGUE_ID = "league_id"
    ROUND_ID = "round_id"
    MATCH_ID = "match_id"
    PLAYER_ID = "player_id"
    REFEREE_ID = "referee_id"
    OPPONENT_ID = "opponent_id"

    # Game fields
    GAME_TYPE = "game_type"
    ROLE_IN_MATCH = "role_in_match"
    PARITY_CHOICE = "parity_choice"
    DEADLINE = "deadline"
    CONTEXT = "context"
    GAME_RESULT = "game_result"

    # Player fields
    ARRIVAL_TIMESTAMP = "arrival_timestamp"
    ACCEPT = "accept"
    PLAYER_META = "player_meta"

    # Referee fields
    REFEREE_META = "referee_meta"

    # Result fields
    WINNER = "winner"
    WINNER_PLAYER_ID = "winner_player_id"
    DRAWN_NUMBER = "drawn_number"
    NUMBER_PARITY = "number_parity"
    CHOICES = "choices"
    REASON = "reason"
    RESULT = "result"
    SCORE = "score"
    DETAILS = "details"

    # Match fields
    PLAYER_A_ID = "player_A_id"
    PLAYER_B_ID = "player_B_id"
    PLAYER_A_ENDPOINT = "player_A_endpoint"
    PLAYER_B_ENDPOINT = "player_B_endpoint"
    REFEREE_ENDPOINT = "referee_endpoint"

    # Round/League lifecycle
    MATCHES = "matches"
    STANDINGS = "standings"
    MATCHES_COMPLETED = "matches_completed"
    NEXT_ROUND_ID = "next_round_id"
    SUMMARY = "summary"
    TOTAL_ROUNDS = "total_rounds"
    TOTAL_MATCHES = "total_matches"
    CHAMPION = "champion"
    FINAL_STANDINGS = "final_standings"

    # Error fields
    ERROR_CODE = "error_code"
    ERROR_DESCRIPTION = "error_description"
    AFFECTED_PLAYER = "affected_player"
    ACTION_REQUIRED = "action_required"
    RETRY_INFO = "retry_info"
    CONSEQUENCE = "consequence"
    ORIGINAL_MESSAGE_TYPE = "original_message_type"

    # Query fields
    QUERY_TYPE = "query_type"
    QUERY_PARAMS = "query_params"
    DATA = "data"

    # Misc
    ENDPOINT = "endpoint"
    AUTH_TOKEN = "auth_token"
    STATUS = "status"
    VERSION = "version"
    LAST_UPDATED = "last_updated"
    DISPLAY_NAME = "display_name"
    GAME_TYPES = "game_types"
    CONTACT_ENDPOINT = "contact_endpoint"
    MAX_CONCURRENT_MATCHES = "max_concurrent_matches"

    # DEPRECATED aliases
    CHOICE = "parity_choice"
    PLAYER_A = "player_A_id"
    PLAYER_B = "player_B_id"
    PLAYER_A_CHOICE = "player_a_choice"
    PLAYER_B_CHOICE = "player_b_choice"
    OPPONENT_CHOICES = "opponent_choices"
