"""League SDK - Core components for AI Agent League Competition System."""

from .agent_comm import (get_transport, reset_transport, send, send_with_retry,
                         set_transport)
from .config_loader import (load_agent_config, load_game_config,
                            load_league_config, load_system_config)
from .config_models import (GameConfig, LeagueConfig, PlayerConfig,
                            RefereeConfig, SystemConfig)
from .session_manager import (AgentType, Session, SessionManager, SessionState,
                              get_session_manager, reset_session_manager)
from .transport import (BaseTransport, HTTPTransport, STDIOTransport,
                        TransportType, create_transport, register_transport)

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
    "AgentType",
    "get_session_manager",
    "reset_session_manager",
    # Agent communication (high-level API)
    "send",
    "send_with_retry",
    "get_transport",
    "set_transport",
    "reset_transport",
]
