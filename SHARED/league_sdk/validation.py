"""Message validation utilities for the league protocol."""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from SHARED.constants import MessageType, Field

def validate_message(message: Dict[str, Any]) -> bool:
    """
    Validate a protocol message has all required fields.
    
    Args:
        message: Message dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required = [Field.PROTOCOL, Field.CONVERSATION_ID, Field.TIMESTAMP, Field.MESSAGE_TYPE]
    return all(field in message for field in required)

def validate_timestamp(timestamp: str) -> bool:
    """
    Validate timestamp is in ISO-8601 format with Z suffix.
    
    Args:
        timestamp: Timestamp string to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not timestamp.endswith('Z'):
        return False
    
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def validate_uuid(uuid_str: str) -> bool:
    """
    Validate UUID format (8-4-4-4-12 hex digits).
    
    Args:
        uuid_str: UUID string to validate
        
    Returns:
        True if valid UUID format, False otherwise
    """
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(pattern, uuid_str.lower()))

def validate_message_type(msg_type: str) -> bool:
    """
    Validate message type is a known protocol message.
    
    Args:
        msg_type: Message type string
        
    Returns:
        True if valid message type, False otherwise
    """
    valid_types = [
        MessageType.GAME_INVITATION,
        MessageType.GAME_JOIN_ACK,
        MessageType.CHOOSE_PARITY_CALL,
        MessageType.PARITY_CHOICE,
        MessageType.GAME_OVER,
        MessageType.MATCH_RESULT_REPORT,
        MessageType.MATCH_RESULT_ACK,
        MessageType.LEAGUE_REGISTER_REQUEST,
        MessageType.LEAGUE_REGISTER_RESPONSE,
        MessageType.REFEREE_REGISTER_REQUEST,
        MessageType.REFEREE_REGISTER_RESPONSE
    ]
    return msg_type in valid_types

def validate_required_fields(message: Dict[str, Any], 
                            required_fields: List[str]) -> Optional[str]:
    """
    Validate message has all required fields for its type.
    
    Args:
        message: Message to validate
        required_fields: List of required field names
        
    Returns:
        None if valid, error message string if invalid
    """
    missing = [f for f in required_fields if f not in message]
    if missing:
        return f"Missing required fields: {', '.join(missing)}"
    return None

def validate_protocol_version(protocol: str, expected: str = "league.v2") -> bool:
    """
    Validate protocol version matches expected version.
    
    Args:
        protocol: Protocol version from message
        expected: Expected protocol version
        
    Returns:
        True if matches, False otherwise
    """
    return protocol == expected

def get_validation_errors(message: Dict[str, Any]) -> List[str]:
    """
    Get all validation errors for a message.
    
    Args:
        message: Message to validate
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    if not validate_message(message):
        errors.append("Missing required base fields")
        return errors
    
    if not validate_timestamp(message.get(Field.TIMESTAMP, "")):
        errors.append("Invalid timestamp format")
    
    if not validate_uuid(message.get(Field.CONVERSATION_ID, "")):
        errors.append("Invalid message ID format")
    
    if not validate_message_type(message.get(Field.MESSAGE_TYPE, "")):
        errors.append("Invalid message type")
    
    if not validate_protocol_version(message.get(Field.PROTOCOL, "")):
        errors.append("Invalid protocol version")
    
    return errors
