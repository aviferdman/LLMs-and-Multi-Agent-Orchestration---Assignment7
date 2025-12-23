"""JSON-RPC 2.0 helper functions for protocol messages."""

from typing import Any, Dict, Optional

from SHARED.protocol_constants import JSONRPC_VERSION, generate_request_id


def wrap_jsonrpc_request(
    method: str,
    params: Dict[str, Any],
    request_id: Optional[int] = None,
    agent_id: str = "default",
) -> Dict[str, Any]:
    """Wrap protocol params in JSON-RPC 2.0 request format.

    Args:
        method: JSON-RPC method name
        params: Protocol message content
        request_id: Optional explicit request ID (auto-generated if None)
        agent_id: Agent identifier for ID generation

    Returns:
        JSON-RPC 2.0 request envelope
    """
    return {
        "jsonrpc": JSONRPC_VERSION,
        "method": method,
        "params": params,
        "id": request_id if request_id is not None else generate_request_id(agent_id),
    }


def wrap_jsonrpc_response(
    result: Dict[str, Any],
    request_id: int,
) -> Dict[str, Any]:
    """Wrap protocol result in JSON-RPC 2.0 response format.

    Args:
        result: Protocol message content
        request_id: ID from the original request (must match)

    Returns:
        JSON-RPC 2.0 response envelope
    """
    return {
        "jsonrpc": JSONRPC_VERSION,
        "result": result,
        "id": request_id,
    }


def wrap_jsonrpc_error(
    code: int,
    message: str,
    request_id: Optional[int] = None,
    data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Wrap error in JSON-RPC 2.0 error response format.

    Args:
        code: Error code
        message: Error message
        request_id: ID from the original request (None if request was invalid)
        data: Optional additional error data

    Returns:
        JSON-RPC 2.0 error response envelope
    """
    error = {"code": code, "message": message}
    if data:
        error["data"] = data
    return {
        "jsonrpc": JSONRPC_VERSION,
        "error": error,
        "id": request_id,
    }


def extract_jsonrpc_params(message: Dict[str, Any]) -> Dict[str, Any]:
    """Extract params from JSON-RPC request, or return message if not wrapped.

    Args:
        message: Incoming message (may or may not be JSON-RPC wrapped)

    Returns:
        The params dict if JSON-RPC wrapped, otherwise the original message
    """
    if message.get("jsonrpc") == JSONRPC_VERSION and "params" in message:
        return message["params"]
    return message


def get_jsonrpc_id(message: Dict[str, Any]) -> Optional[int]:
    """Get the request ID from a JSON-RPC message.

    Args:
        message: Incoming JSON-RPC message

    Returns:
        The request ID, or None if not a JSON-RPC message
    """
    if message.get("jsonrpc") == JSONRPC_VERSION:
        return message.get("id")
    return None


def is_jsonrpc_request(message: Dict[str, Any]) -> bool:
    """Check if message is a JSON-RPC 2.0 request."""
    return (
        message.get("jsonrpc") == JSONRPC_VERSION
        and "method" in message
        and "id" in message
    )


def is_jsonrpc_response(message: Dict[str, Any]) -> bool:
    """Check if message is a JSON-RPC 2.0 response."""
    return (
        message.get("jsonrpc") == JSONRPC_VERSION
        and ("result" in message or "error" in message)
        and "id" in message
    )
