"""Session manager - handles agent sessions and connection lifecycle.

Provides SessionManager for delegated session handling - agents should use this
rather than managing auth tokens and registration state manually.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class SessionState(str, Enum):
    """Session lifecycle states."""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class AgentType(str, Enum):
    """Agent type constants for session management."""
    PLAYER = "player"
    REFEREE = "referee"
    LEAGUE_MANAGER = "league_manager"


@dataclass
class Session:
    """Represents an agent session."""
    session_id: str
    agent_id: str
    agent_type: str
    endpoint: str
    state: SessionState = SessionState.PENDING
    auth_token: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_activity: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_active(self) -> bool:
        return self.state == SessionState.ACTIVE
    
    def touch(self) -> None:
        self.last_activity = datetime.now(timezone.utc).isoformat()


class SessionManager:
    """Manages agent sessions throughout their lifecycle."""
    
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
        self._agent_sessions: Dict[str, str] = {}
    
    def create_session(self, agent_id: str, agent_type: str, endpoint: str,
                       metadata: Optional[Dict] = None) -> Session:
        """Create a new session for an agent."""
        session_id = str(uuid.uuid4())
        session = Session(
            session_id=session_id, agent_id=agent_id, agent_type=agent_type,
            endpoint=endpoint, state=SessionState.ACTIVE,
            auth_token=str(uuid.uuid4()), metadata=metadata or {},
        )
        self._sessions[session_id] = session
        self._agent_sessions[agent_id] = session_id
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)
    
    def get_session_by_agent(self, agent_id: str) -> Optional[Session]:
        session_id = self._agent_sessions.get(agent_id)
        return self._sessions.get(session_id) if session_id else None
    
    def validate_token(self, agent_id: str, token: str) -> bool:
        """Validate an authentication token for an agent."""
        session = self.get_session_by_agent(agent_id)
        if session and session.is_active() and session.auth_token == token:
            session.touch()
            return True
        return False
    
    def close_session(self, session_id: str) -> bool:
        """Close a session."""
        session = self._sessions.get(session_id)
        if session:
            session.state = SessionState.CLOSED
            self._agent_sessions.pop(session.agent_id, None)
            return True
        return False
    
    def close_session_by_agent(self, agent_id: str) -> bool:
        session_id = self._agent_sessions.get(agent_id)
        return self.close_session(session_id) if session_id else False
    
    def is_registered(self, agent_id: str) -> bool:
        """Check if an agent is already registered with an active session."""
        session = self.get_session_by_agent(agent_id)
        return session is not None and session.is_active()
    
    def get_endpoint(self, agent_id: str) -> Optional[str]:
        session = self.get_session_by_agent(agent_id)
        return session.endpoint if session else None
    
    def get_auth_token(self, agent_id: str) -> Optional[str]:
        session = self.get_session_by_agent(agent_id)
        return session.auth_token if session else None
    
    def get_registered_agent_ids(self, agent_type: Optional[str] = None) -> list:
        """Get list of registered agent IDs, optionally filtered by type."""
        return [s.agent_id for s in self._sessions.values()
                if s.is_active() and (agent_type is None or s.agent_type == agent_type)]
    
    def get_registered_agents_data(self, agent_type: Optional[str] = None) -> Dict[str, Dict]:
        """Get registered agents data in dict format for backward compatibility."""
        result = {}
        for s in self._sessions.values():
            if s.is_active() and (agent_type is None or s.agent_type == agent_type):
                result[s.agent_id] = {"agent_id": s.agent_id, "auth_token": s.auth_token,
                                       "endpoint": s.endpoint, "registered_at": s.created_at}
        return result


# Global singleton instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Get the global SessionManager singleton instance."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager


def reset_session_manager() -> None:
    """Reset the session manager (useful for testing)."""
    global _session_manager
    _session_manager = None
