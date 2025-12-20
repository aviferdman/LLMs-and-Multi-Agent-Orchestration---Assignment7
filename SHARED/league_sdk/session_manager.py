"""Session manager - handles agent sessions and connection lifecycle."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class SessionState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"

class AgentType(str, Enum):
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
        session_id = str(uuid.uuid4())
        session = Session(session_id=session_id, agent_id=agent_id, agent_type=agent_type,
                          endpoint=endpoint, state=SessionState.ACTIVE,
                          auth_token=str(uuid.uuid4()), metadata=metadata or {})
        self._sessions[session_id] = session
        self._agent_sessions[agent_id] = session_id
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def get_session_by_agent(self, agent_id: str) -> Optional[Session]:
        session_id = self._agent_sessions.get(agent_id)
        return self._sessions.get(session_id) if session_id else None

    def validate_token(self, agent_id: str, token: str) -> bool:
        session = self.get_session_by_agent(agent_id)
        if session and session.is_active() and session.auth_token == token:
            session.touch()
            return True
        return False

    def close_session(self, session_id: str) -> bool:
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
        session = self.get_session_by_agent(agent_id)
        return session is not None and session.is_active()

    def get_endpoint(self, agent_id: str) -> Optional[str]:
        session = self.get_session_by_agent(agent_id)
        return session.endpoint if session else None

    def get_auth_token(self, agent_id: str) -> Optional[str]:
        session = self.get_session_by_agent(agent_id)
        return session.auth_token if session else None

    def get_registered_agent_ids(self, agent_type: Optional[str] = None) -> list:
        return [s.agent_id for s in self._sessions.values()
                if s.is_active() and (agent_type is None or s.agent_type == agent_type)]

    def get_registered_agents_data(self, agent_type: Optional[str] = None) -> Dict[str, Dict]:
        result = {}
        for s in self._sessions.values():
            if s.is_active() and (agent_type is None or s.agent_type == agent_type):
                result[s.agent_id] = {"agent_id": s.agent_id, "auth_token": s.auth_token,
                                      "endpoint": s.endpoint, "registered_at": s.created_at}
        return result


_session_manager: Optional[SessionManager] = None

def get_session_manager() -> SessionManager:
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager

def reset_session_manager() -> None:
    global _session_manager
    _session_manager = None
