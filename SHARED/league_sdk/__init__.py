"""League SDK - Core components for AI Agent League Competition System."""

from .config_models import (
    SystemConfig,
    LeagueConfig,
    PlayerConfig,
    RefereeConfig,
    GameConfig,
)
from .config_loader import (
    load_system_config,
    load_league_config,
    load_agent_config,
    load_game_config,
)
from .transport import (
    BaseTransport,
    HTTPTransport,
    STDIOTransport,
    TransportType,
    create_transport,
    register_transport,
)
from .session_manager import (
    Session,
    SessionState,
    SessionManager,
)
from .agent_comm import (
    send,
    send_with_retry,
    get_transport,
    set_transport,
    reset_transport,
)

__version__ = "1.0.0"
__all__ = [
    # Config models
    "SystemConfig",
    "LeagueConfig",
    "PlayerConfig",
    "RefereeConfig",
    "GameConfig",
    # Config loaders
    "load_system_config",
    "load_league_config",
    "load_agent_config",
    "load_game_config",
    # Transport abstraction
    "BaseTransport",
    "HTTPTransport",
    "STDIOTransport",
    "TransportType",
    "create_transport",
    "register_transport",
    # Session management
    "Session",
    "SessionState",
    "SessionManager",
    # Agent communication (high-level API)
    "send",
    "send_with_retry",
    "get_transport",
    "set_transport",
    "reset_transport",
]
