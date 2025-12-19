"""Agent, game, and system constants."""

class AgentID:
    """All agent identifiers."""
    LEAGUE_MANAGER = "LM01"
    REFEREE_01 = "REF01"
    REFEREE_02 = "REF02"
    PLAYER_01 = "P01"
    PLAYER_02 = "P02"
    PLAYER_03 = "P03"
    PLAYER_04 = "P04"

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

class ParityChoice:
    """Parity choices in Even-Odd game."""
    EVEN = "EVEN"
    ODD = "ODD"

class Winner:
    """Winner designation values."""
    PLAYER_A = "PLAYER_A"
    PLAYER_B = "PLAYER_B"
    DRAW = "DRAW"

EVEN_ODD_MIN_NUMBER = 1
EVEN_ODD_MAX_NUMBER = 10

class StrategyType:
    """Player strategy types."""
    RANDOM = "random"
    FREQUENCY = "frequency"
    PATTERN = "pattern"

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

class FileName:
    """Standard file names."""
    SYSTEM_CONFIG = "system.json"
    AGENTS_CONFIG = "agents_config.json"
    GAMES_REGISTRY = "games_registry.json"
    STANDINGS = "standings.json"

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

class Points:
    """Point values for match outcomes."""
    WIN = 3
    DRAW = 1
    LOSS = 0
