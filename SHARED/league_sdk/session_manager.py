"""Session manager - handles agent sessions and connection lifecycle."""

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
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id, "agent_id": self.agent_id,
            "agent_type": self.agent_type, "endpoint": self.endpoint,
            "state": self.state.value, "auth_token": self.auth_token,
            "created_at": self.created_at, "last_activity": self.last_activity,
        }


class SessionManager:
    """Manages agent sessions throughout their lifecycle."""
    
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
        self._agent_sessions: Dict[str, str] = {}
    
    def create_session(
        self, agent_id: str, agent_type: str, endpoint: str, metadata: Optional[Dict] = None
    ) -> Session:
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
        """Close session for an agent."""
        session_id = self._agent_sessions.get(agent_id)
        return self.close_session(session_id) if session_id else False
    
    def get_active_sessions(self, agent_type: Optional[str] = None) -> Dict[str, Session]:
        """Get all active sessions, optionally filtered by type."""
        return {
            sid: s for sid, s in self._sessions.items()
            if s.is_active() and (agent_type is None or s.agent_type == agent_type)
        }
    
    def get_session_count(self, state: Optional[SessionState] = None) -> int:
        if state is None:
            return len(self._sessions)
        return sum(1 for s in self._sessions.values() if s.state == state)
