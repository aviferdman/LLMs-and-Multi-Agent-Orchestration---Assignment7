"""Schema loading and caching utilities.

Handles loading JSON schemas from disk and caching them.
"""

import json
import logging
from pathlib import Path
from typing import Dict

from jsonschema import Draft7Validator, RefResolver

from SHARED.contracts.exceptions import SchemaNotFoundError

logger = logging.getLogger(__name__)

# Schema directory path
SCHEMAS_DIR = Path(__file__).parent / "schemas"

# Cache for loaded schemas
_schema_cache: Dict[str, dict] = {}

# Cache for compiled validators
_validator_cache: Dict[str, Draft7Validator] = {}

# Message type to schema file mapping
MESSAGE_TYPE_TO_SCHEMA = {
    # League Manager source
    "ROUND_ANNOUNCEMENT": "round_announcement.schema.json",
    "ROUND_COMPLETED": "round_completed.schema.json",
    "LEAGUE_STANDINGS_UPDATE": "league_standings_update.schema.json",
    "LEAGUE_COMPLETED": "league_completed.schema.json",
    "LEAGUE_QUERY_RESPONSE": "league_query_response.schema.json",
    "LEAGUE_ERROR": "league_error.schema.json",
    "LEAGUE_STATUS": "league_status.schema.json",
    "MATCH_RESULT_ACK": "match_result_ack.schema.json",
    "RUN_MATCH": "run_match.schema.json",
    "SHUTDOWN_COMMAND": "shutdown_command.schema.json",
    # Registration
    "REFEREE_REGISTER_REQUEST": "referee_register_request.schema.json",
    "REFEREE_REGISTER_RESPONSE": "referee_register_response.schema.json",
    "LEAGUE_REGISTER_REQUEST": "league_register_request.schema.json",
    "LEAGUE_REGISTER_RESPONSE": "league_register_response.schema.json",
    # Referee source
    "GAME_INVITATION": "game_invitation.schema.json",
    "CHOOSE_PARITY_CALL": "choose_parity_call.schema.json",
    "GAME_OVER": "game_over.schema.json",
    "MATCH_RESULT_REPORT": "match_result_report.schema.json",
    "GAME_ERROR": "game_error.schema.json",
    "RUN_MATCH_ACK": "run_match_ack.schema.json",
    # Player source
    "GAME_JOIN_ACK": "game_join_ack.schema.json",
    "CHOOSE_PARITY_RESPONSE": "choose_parity_response.schema.json",
    "LEAGUE_QUERY": "league_query.schema.json",
    "SHUTDOWN_ACK": "shutdown_ack.schema.json",
    # Launcher source
    "START_LEAGUE": "start_league.schema.json",
}


def load_schema(schema_file: str) -> dict:
    """Load a JSON schema file from the schemas directory.

    Args:
        schema_file: Name of the schema file (e.g., "game_invitation.schema.json")

    Returns:
        Parsed JSON schema as a dictionary

    Raises:
        SchemaNotFoundError: If the schema file doesn't exist
        json.JSONDecodeError: If the schema file is invalid JSON
    """
    if schema_file in _schema_cache:
        return _schema_cache[schema_file]

    schema_path = SCHEMAS_DIR / schema_file
    if not schema_path.exists():
        raise SchemaNotFoundError(schema_file)

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    _schema_cache[schema_file] = schema
    return schema


def get_validator(message_type: str) -> Draft7Validator:
    """Get or create a validator for the given message type.

    Args:
        message_type: The protocol message type

    Returns:
        A configured Draft7Validator instance

    Raises:
        SchemaNotFoundError: If no schema exists for this message type
    """
    if message_type in _validator_cache:
        return _validator_cache[message_type]

    schema_file = MESSAGE_TYPE_TO_SCHEMA.get(message_type)
    if not schema_file:
        raise SchemaNotFoundError(message_type)

    schema = load_schema(schema_file)

    # Create resolver for $ref handling
    resolver = RefResolver(
        base_uri=f"file:///{SCHEMAS_DIR.as_posix()}/",
        referrer=schema,
        handlers={"file": lambda uri: load_schema(Path(uri).name)},
    )

    # Create and cache validator
    validator = Draft7Validator(schema, resolver=resolver)
    _validator_cache[message_type] = validator

    return validator


def clear_cache() -> None:
    """Clear all cached schemas and validators.

    Useful for testing or when schemas have been modified.
    """
    _schema_cache.clear()
    _validator_cache.clear()
