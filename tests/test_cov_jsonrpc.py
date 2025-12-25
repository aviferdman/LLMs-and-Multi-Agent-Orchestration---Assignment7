"""Tests for SHARED.contracts.jsonrpc_helpers module."""

import pytest
from SHARED.contracts.jsonrpc_helpers import (
    wrap_jsonrpc_request,
    wrap_jsonrpc_response,
    wrap_jsonrpc_error,
    extract_jsonrpc_params,
    get_jsonrpc_id,
)


class TestWrapJsonrpcRequest:
    """Tests for wrap_jsonrpc_request function."""

    def test_wraps_params_in_jsonrpc_request(self):
        """Test params are wrapped in JSON-RPC format."""
        msg = wrap_jsonrpc_request("test_method", {"key": "value"})
        assert msg["jsonrpc"] == "2.0"
        assert msg["method"] == "test_method"
        assert msg["params"] == {"key": "value"}

    def test_includes_id_field(self):
        """Test JSON-RPC request includes ID field."""
        msg = wrap_jsonrpc_request("test", {"data": 1})
        assert "id" in msg

    def test_uses_provided_agent_id(self):
        """Test uses agent ID when provided."""
        msg = wrap_jsonrpc_request("test", {}, agent_id="P01")
        assert "id" in msg


class TestWrapJsonrpcResponse:
    """Tests for wrap_jsonrpc_response function."""

    def test_wraps_result_in_response(self):
        """Test result is wrapped in JSON-RPC response."""
        msg = wrap_jsonrpc_response({"status": "ok"}, request_id="req-1")
        assert msg["jsonrpc"] == "2.0"
        assert msg["result"] == {"status": "ok"}
        assert msg["id"] == "req-1"

    def test_response_has_jsonrpc_version(self):
        """Test response has JSON-RPC version."""
        msg = wrap_jsonrpc_response({"data": 1}, "id-1")
        assert msg["jsonrpc"] == "2.0"


class TestWrapJsonrpcError:
    """Tests for wrap_jsonrpc_error function."""

    def test_wraps_error_in_response(self):
        """Test error is wrapped in JSON-RPC error response."""
        msg = wrap_jsonrpc_error(-32600, "Invalid request", request_id="req-1")
        assert msg["jsonrpc"] == "2.0"
        assert "error" in msg
        assert msg["error"]["code"] == -32600

    def test_error_includes_message(self):
        """Test error includes error message."""
        msg = wrap_jsonrpc_error(-32601, "Method not found", "req-2")
        assert msg["error"]["message"] == "Method not found"


class TestExtractJsonrpcParams:
    """Tests for extract_jsonrpc_params function."""

    def test_extracts_params_from_request(self):
        """Test extracts params from JSON-RPC request."""
        request = {"jsonrpc": "2.0", "method": "test", "params": {"a": 1}, "id": "1"}
        params = extract_jsonrpc_params(request)
        assert params == {"a": 1}

    def test_returns_original_if_no_params(self):
        """Test returns original message if no params."""
        request = {"jsonrpc": "2.0", "method": "test", "id": "1"}
        params = extract_jsonrpc_params(request)
        assert params == request  # Returns original if no params


class TestGetJsonrpcId:
    """Tests for get_jsonrpc_id function."""

    def test_gets_id_from_request(self):
        """Test gets ID from JSON-RPC request."""
        request = {"jsonrpc": "2.0", "method": "test", "id": "request-123"}
        req_id = get_jsonrpc_id(request)
        assert req_id == "request-123"

    def test_returns_none_if_no_id(self):
        """Test returns None if no ID (notification)."""
        request = {"jsonrpc": "2.0", "method": "notify"}
        req_id = get_jsonrpc_id(request)
        assert req_id is None
