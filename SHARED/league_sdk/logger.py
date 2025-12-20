"""Logging utilities for the league system."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class LeagueLogger:
    """JSONL logger for league events."""

    def __init__(self, agent_id: str, log_dir: Path = None):
        """Initialize logger for specific agent."""
        if log_dir is None:
            log_dir = Path("SHARED/logs/agents")

        self.log_file = log_dir / f"{agent_id}.log.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.agent_id = agent_id

    def log_message(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log a message event."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "agent_id": self.agent_id,
            "event_type": event_type,
            "data": data,
        }
        self._write_log(log_entry)

    def log_error(
        self, error_type: str, message: str, details: Dict[str, Any] = None
    ) -> None:
        """Log an error event."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "agent_id": self.agent_id,
            "event_type": "ERROR",
            "error_type": error_type,
            "message": message,
            "details": details or {},
        }
        self._write_log(log_entry)

    def log_state_change(
        self, old_state: str, new_state: str, context: Dict[str, Any] = None
    ) -> None:
        """Log a state transition event."""
        log_entry = {
            "timestamp": self._get_timestamp(),
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
