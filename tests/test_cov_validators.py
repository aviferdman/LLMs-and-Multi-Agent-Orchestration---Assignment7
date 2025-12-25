"""Tests for validation helpers and message validators - Coverage boost."""

import pytest


class TestValidationHelpers:
    """Tests for validation helper functions."""

    def test_validate_incoming_no_errors(self):
        from SHARED.contracts.validation_helpers import validate_incoming

        message = {"message_type": "TEST", "data": "value"}
        validator = lambda m: []
        errors = validate_incoming(message, validator)
        assert errors == []

    def test_validate_incoming_with_errors_log(self):
        from SHARED.contracts.validation_helpers import validate_incoming

        message = {"message_type": "TEST_MSG"}
        validator = lambda m: ["error1", "error2"]
        errors = validate_incoming(message, validator, log_errors=True)
        assert len(errors) == 2

    def test_validate_incoming_many_errors(self):
        from SHARED.contracts.validation_helpers import validate_incoming

        message = {"message_type": "TEST"}
        validator = lambda m: ["e1", "e2", "e3", "e4", "e5"]
        errors = validate_incoming(message, validator, log_errors=True)
        assert len(errors) == 5

    def test_validate_incoming_raises_on_error(self):
        from SHARED.contracts.exceptions import ProtocolValidationError
        from SHARED.contracts.validation_helpers import validate_incoming

        message = {"message_type": "FAIL_MSG"}
        validator = lambda m: ["validation error"]
        with pytest.raises(ProtocolValidationError):
            validate_incoming(message, validator, raise_on_error=True)

    def test_validated_builder_decorator(self):
        from SHARED.contracts.validation_helpers import validated_builder

        def mock_validator(msg):
            if "error" in msg:
                raise ValueError("Invalid")

        @validated_builder(mock_validator)
        def build_message():
            return {"message_type": "TEST", "value": 1}

        result = build_message()
        assert result["message_type"] == "TEST"


class TestMessageValidator:
    """Tests for message validation functions."""

    def test_validate_message_not_dict(self):
        from SHARED.contracts.message_validator import validate_message

        errors = validate_message("not a dict")
        assert "Message must be a dictionary" in errors

    def test_validate_message_missing_type(self):
        from SHARED.contracts.message_validator import validate_message

        errors = validate_message({"field": "value"})
        assert any("message_type" in e for e in errors)

    def test_validate_message_unknown_type(self):
        from SHARED.contracts.message_validator import validate_message

        errors = validate_message({"message_type": "NONEXISTENT_TYPE_XYZ"})
        assert len(errors) > 0

    def test_validate_or_raise_not_dict(self):
        from SHARED.contracts.exceptions import InvalidMessageError
        from SHARED.contracts.message_validator import validate_or_raise

        with pytest.raises(InvalidMessageError):
            validate_or_raise("not a dict")

    def test_validate_or_raise_missing_type(self):
        from SHARED.contracts.exceptions import InvalidMessageError
        from SHARED.contracts.message_validator import validate_or_raise

        with pytest.raises(InvalidMessageError):
            validate_or_raise({"some_field": "value"})

    def test_validate_incoming_function(self):
        from SHARED.contracts.message_validator import validate_incoming

        errors = validate_incoming({"field": "no type"}, log_errors=True)
        assert len(errors) > 0

    def test_validate_incoming_with_raise(self):
        from SHARED.contracts.exceptions import ProtocolValidationError
        from SHARED.contracts.message_validator import validate_incoming

        with pytest.raises(ProtocolValidationError):
            validate_incoming({"bad": "msg"}, raise_on_error=True)

    def test_get_schema_unknown(self):
        from SHARED.contracts.message_validator import get_schema

        result = get_schema("TOTALLY_UNKNOWN_MESSAGE")
        assert result is None

    def test_list_message_types(self):
        from SHARED.contracts.message_validator import list_message_types

        types = list_message_types()
        assert isinstance(types, list)
        assert len(types) > 0
        assert "GAME_INVITATION" in types
