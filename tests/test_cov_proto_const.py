"""Tests for SHARED.protocol_constants module."""

import pytest
from SHARED.protocol_constants import (
    generate_request_id,
    reset_request_id_counter,
    generate_timestamp,
    generate_deadline,
    generate_conversation_id,
    format_sender,
    JSONRPCMethod,
    JSONRPC_VERSION,
    PROTOCOL_VERSION,
)


class TestGenerateRequestId:
    """Tests for generate_request_id function."""

    def test_generates_sequential_ids(self):
        """Test generates sequential IDs."""
        reset_request_id_counter("test_agent")
        id1 = generate_request_id("test_agent")
        id2 = generate_request_id("test_agent")
        assert id2 == id1 + 1

    def test_different_agents_have_separate_counters(self):
        """Test different agents have separate counters."""
        reset_request_id_counter()
        id_a = generate_request_id("agent_a")
        id_b = generate_request_id("agent_b")
        assert id_a == 1
        assert id_b == 1


class TestResetRequestIdCounter:
    """Tests for reset_request_id_counter function."""

    def test_reset_specific_agent(self):
        """Test resetting specific agent counter."""
        generate_request_id("agent_x")
        reset_request_id_counter("agent_x")
        new_id = generate_request_id("agent_x")
        assert new_id == 1

    def test_reset_all_counters(self):
        """Test resetting all counters."""
        generate_request_id("agent_1")
        generate_request_id("agent_2")
        reset_request_id_counter()
        assert generate_request_id("agent_1") == 1
        assert generate_request_id("agent_2") == 1


class TestGenerateTimestamp:
    """Tests for generate_timestamp function."""

    def test_returns_iso_format(self):
        """Test returns ISO format timestamp."""
        ts = generate_timestamp()
        assert "T" in ts
        assert ts.endswith("Z")

    def test_includes_milliseconds(self):
        """Test timestamp includes milliseconds."""
        ts = generate_timestamp()
        assert "." in ts


class TestGenerateDeadline:
    """Tests for generate_deadline function."""

    def test_returns_future_timestamp(self):
        """Test returns timestamp in future."""
        deadline = generate_deadline(60)
        assert deadline.endswith("Z")
        assert "T" in deadline


class TestGenerateConversationId:
    """Tests for generate_conversation_id function."""

    def test_returns_uuid_string(self):
        """Test returns UUID-format string."""
        conv_id = generate_conversation_id()
        assert len(conv_id) == 36
        assert conv_id.count("-") == 4

    def test_generates_unique_ids(self):
        """Test generates unique IDs."""
        ids = [generate_conversation_id() for _ in range(10)]
        assert len(set(ids)) == 10


class TestFormatSender:
    """Tests for format_sender function."""

    def test_formats_player_sender(self):
        """Test formats player sender."""
        sender = format_sender("player", "P01")
        assert sender == "player:P01"

    def test_formats_referee_sender(self):
        """Test formats referee sender."""
        sender = format_sender("referee", "REF01")
        assert sender == "referee:REF01"

    def test_league_manager_unchanged(self):
        """Test league_manager returns unchanged."""
        sender = format_sender("league_manager", "LM")
        assert sender == "league_manager"

    def test_launcher_unchanged(self):
        """Test launcher returns unchanged."""
        sender = format_sender("launcher", "L1")
        assert sender == "launcher"


class TestConstants:
    """Tests for protocol constants."""

    def test_jsonrpc_version(self):
        """Test JSON-RPC version is 2.0."""
        assert JSONRPC_VERSION == "2.0"

    def test_protocol_version_format(self):
        """Test protocol version format."""
        assert "league" in PROTOCOL_VERSION

    def test_jsonrpc_methods_are_strings(self):
        """Test JSONRPCMethod values are strings."""
        assert isinstance(JSONRPCMethod.REGISTER_PLAYER.value, str)
        assert isinstance(JSONRPCMethod.GAME_OVER.value, str)
