"""Logging utilities for the league system."""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional


class LogLevel(Enum):
    """Log levels for the league system."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class LeagueLogger:
    """JSONL logger for league events."""

    def __init__(self, agent_id: str, log_dir: Path = None):
        """Initialize logger for specific agent."""
        if log_dir is None:
            log_dir = Path("SHARED/logs/agents")

        self.log_file = log_dir / f"{agent_id}.log.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.agent_id = agent_id

    def log_message(
        self,
        event_type: str,
        data: Dict[str, Any],
        level: LogLevel = LogLevel.INFO,
    ) -> None:
        """Log a message event."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "level": level.value,
            "agent_id": self.agent_id,
            "event_type": event_type,
            "data": data,
        }
        self._write_log(log_entry)

    def debug(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log a debug message."""
        self.log_message(event_type, data, LogLevel.DEBUG)

    def info(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log an info message."""
        self.log_message(event_type, data, LogLevel.INFO)

    def warn(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log a warning message."""
        self.log_message(event_type, data, LogLevel.WARN)

    def log_error(
        self,
        error_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log an error event."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "level": LogLevel.ERROR.value,
            "agent_id": self.agent_id,
            "event_type": "ERROR",
            "error_type": error_type,
            "message": message,
            "details": details or {},
        }
        self._write_log(log_entry)

    def log_state_change(
        self,
        old_state: str,
        new_state: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a state transition event."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "level": LogLevel.INFO.value,
            "agent_id": self.agent_id,
            "event_type": "STATE_CHANGE",
            "old_state": old_state,
            "new_state": new_state,
            "context": context or {},
        }
        self._write_log(log_entry)

    def _get_timestamp(self) -> str:
        """Get current UTC timestamp in ISO-8601 format with Z."""
        return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"

    def _write_log(self, log_entry: Dict[str, Any]) -> None:
        """Write log entry to JSONL file."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
