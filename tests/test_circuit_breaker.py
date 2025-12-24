"""Unit tests for Circuit Breaker pattern."""

import pytest
from datetime import datetime, timedelta

from SHARED.league_sdk.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerRegistry,
    CircuitState,
    get_circuit_breaker_registry,
)


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_initial_state_closed(self):
        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED

    def test_can_execute_when_closed(self):
        cb = CircuitBreaker()
        assert cb.can_execute() is True

    def test_record_success_keeps_closed(self):
        cb = CircuitBreaker()
        cb.record_success()
        assert cb.state == CircuitState.CLOSED
        assert cb.failures == 0

    def test_failures_increment(self):
        cb = CircuitBreaker(failure_threshold=5)
        cb.record_failure()
        assert cb.failures == 1
        cb.record_failure()
        assert cb.failures == 2

    def test_opens_after_threshold(self):
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.CLOSED
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

    def test_cannot_execute_when_open(self):
        cb = CircuitBreaker(failure_threshold=2, reset_timeout=60)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        assert cb.can_execute() is False

    def test_transitions_to_half_open(self):
        cb = CircuitBreaker(failure_threshold=2, reset_timeout=1)
        cb.record_failure()
        cb.record_failure()
        cb._last_failure_time = datetime.now() - timedelta(seconds=2)
        assert cb.state == CircuitState.HALF_OPEN

    def test_can_execute_in_half_open(self):
        cb = CircuitBreaker(failure_threshold=2, reset_timeout=1)
        cb.record_failure()
        cb.record_failure()
        cb._last_failure_time = datetime.now() - timedelta(seconds=2)
        assert cb.can_execute() is True
        assert cb.can_execute() is False

    def test_success_in_half_open_closes(self):
        cb = CircuitBreaker(failure_threshold=2, reset_timeout=1)
        cb.record_failure()
        cb.record_failure()
        cb._last_failure_time = datetime.now() - timedelta(seconds=2)
        cb.can_execute()
        cb.record_success()
        assert cb.state == CircuitState.CLOSED

    def test_failure_in_half_open_reopens(self):
        cb = CircuitBreaker(failure_threshold=2, reset_timeout=1)
        cb.record_failure()
        cb.record_failure()
        cb._last_failure_time = datetime.now() - timedelta(seconds=2)
        cb.can_execute()
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

    def test_reset(self):
        cb = CircuitBreaker(failure_threshold=2)
        cb.record_failure()
        cb.record_failure()
        cb.reset()
        assert cb.state == CircuitState.CLOSED
        assert cb.failures == 0

    def test_get_status(self):
        cb = CircuitBreaker(failure_threshold=3, reset_timeout=30)
        cb.record_failure()
        status = cb.get_status()
        assert status["state"] == "CLOSED"
        assert status["failures"] == 1


class TestCircuitBreakerRegistry:
    """Tests for CircuitBreakerRegistry."""

    def test_creates_breaker(self):
        reg = CircuitBreakerRegistry()
        b = reg.get_breaker("http://test.com")
        assert b.state == CircuitState.CLOSED

    def test_same_breaker_same_endpoint(self):
        reg = CircuitBreakerRegistry()
        b1 = reg.get_breaker("http://test.com")
        b2 = reg.get_breaker("http://test.com")
        assert b1 is b2

    def test_different_breakers_different_endpoints(self):
        reg = CircuitBreakerRegistry()
        b1 = reg.get_breaker("http://a.com")
        b2 = reg.get_breaker("http://b.com")
        assert b1 is not b2

    def test_can_execute_delegates(self):
        reg = CircuitBreakerRegistry(default_failure_threshold=2)
        reg.record_failure("http://test.com")
        reg.record_failure("http://test.com")
        assert reg.can_execute("http://test.com") is False
        assert reg.can_execute("http://other.com") is True

    def test_get_all_status(self):
        reg = CircuitBreakerRegistry()
        reg.get_breaker("http://a.com")
        reg.get_breaker("http://b.com")
        status = reg.get_all_status()
        assert "http://a.com" in status
        assert "http://b.com" in status

    def test_reset_all(self):
        reg = CircuitBreakerRegistry(default_failure_threshold=1)
        reg.record_failure("http://a.com")
        reg.record_failure("http://b.com")
        reg.reset_all()
        assert reg.can_execute("http://a.com") is True
        assert reg.can_execute("http://b.com") is True


def test_global_registry():
    """Test global registry singleton."""
    r1 = get_circuit_breaker_registry()
    r2 = get_circuit_breaker_registry()
    assert r1 is r2
