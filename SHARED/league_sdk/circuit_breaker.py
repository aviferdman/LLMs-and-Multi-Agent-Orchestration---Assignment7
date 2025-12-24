"""Circuit Breaker pattern for resilient HTTP communication.

States: CLOSED (normal), OPEN (blocking), HALF_OPEN (testing)
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Optional


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    """Circuit breaker for a single endpoint."""

    def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60):
        """Initialize with failure threshold and reset timeout (seconds)."""
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self._failures = 0
        self._half_open_calls = 0
        self._last_failure_time: Optional[datetime] = None
        self._state = CircuitState.CLOSED

    @property
    def state(self) -> CircuitState:
        """Get current state, auto-transition OPEN->HALF_OPEN after timeout."""
        if self._state == CircuitState.OPEN and self._timeout_elapsed():
            self._state = CircuitState.HALF_OPEN
            self._half_open_calls = 0
        return self._state

    @property
    def failures(self) -> int:
        """Get failure count."""
        return self._failures

    def _timeout_elapsed(self) -> bool:
        """Check if reset timeout has passed."""
        if self._last_failure_time is None:
            return True
        return (datetime.now() - self._last_failure_time).total_seconds() > self.reset_timeout

    def can_execute(self) -> bool:
        """Check if request can proceed."""
        s = self.state
        if s == CircuitState.CLOSED:
            return True
        if s == CircuitState.OPEN:
            return False
        if self._half_open_calls < 1:
            self._half_open_calls += 1
            return True
        return False

    def record_success(self) -> None:
        """Record success, reset to CLOSED."""
        self._failures = 0
        self._half_open_calls = 0
        self._state = CircuitState.CLOSED

    def record_failure(self) -> None:
        """Record failure, may open circuit."""
        self._failures += 1
        self._last_failure_time = datetime.now()
        if self._state == CircuitState.HALF_OPEN or self._failures >= self.failure_threshold:
            self._state = CircuitState.OPEN

    def reset(self) -> None:
        """Manual reset to CLOSED."""
        self._failures = 0
        self._half_open_calls = 0
        self._last_failure_time = None
        self._state = CircuitState.CLOSED

    def get_status(self) -> Dict:
        """Get monitoring status."""
        return {"state": self.state.value, "failures": self._failures}


class CircuitBreakerRegistry:
    """Registry managing circuit breakers per endpoint."""

    def __init__(self, default_failure_threshold: int = 5, default_reset_timeout: int = 60):
        """Initialize with default settings."""
        self._breakers: Dict[str, CircuitBreaker] = {}
        self._threshold = default_failure_threshold
        self._timeout = default_reset_timeout

    def get_breaker(self, endpoint: str) -> CircuitBreaker:
        """Get or create breaker for endpoint."""
        if endpoint not in self._breakers:
            self._breakers[endpoint] = CircuitBreaker(self._threshold, self._timeout)
        return self._breakers[endpoint]

    def can_execute(self, endpoint: str) -> bool:
        """Check if request to endpoint allowed."""
        return self.get_breaker(endpoint).can_execute()

    def record_success(self, endpoint: str) -> None:
        """Record success for endpoint."""
        self.get_breaker(endpoint).record_success()

    def record_failure(self, endpoint: str) -> None:
        """Record failure for endpoint."""
        self.get_breaker(endpoint).record_failure()

    def get_all_status(self) -> Dict[str, Dict]:
        """Get all breaker statuses."""
        return {ep: b.get_status() for ep, b in self._breakers.items()}

    def reset_all(self) -> None:
        """Reset all breakers."""
        for b in self._breakers.values():
            b.reset()


_registry: Optional[CircuitBreakerRegistry] = None


def get_circuit_breaker_registry() -> CircuitBreakerRegistry:
    """Get global circuit breaker registry."""
    global _registry
    if _registry is None:
        _registry = CircuitBreakerRegistry()
    return _registry
