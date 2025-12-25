"""Tests for SHARED/contracts/exceptions.py - Coverage boost."""

import pytest


class TestProtocolValidationError:
    """Tests for ProtocolValidationError exception."""

    def test_basic_creation(self):
        from SHARED.contracts.exceptions import ProtocolValidationError

        error = ProtocolValidationError(
            message_type="TEST_MESSAGE",
            errors=["field1: required", "field2: invalid type"],
        )
        assert error.message_type == "TEST_MESSAGE"
        assert len(error.errors) == 2
        assert error.message_data is None
        assert "TEST_MESSAGE" in str(error)

    def test_with_message_data(self):
        from SHARED.contracts.exceptions import ProtocolValidationError

        data = {"message_type": "TEST", "field": "value"}
        error = ProtocolValidationError(
            message_type="TEST", errors=["error1"], message_data=data
        )
        assert error.message_data == data

    def test_truncates_many_errors(self):
        from SHARED.contracts.exceptions import ProtocolValidationError

        errors = [f"error{i}" for i in range(10)]
        error = ProtocolValidationError("TEST", errors)
        assert "(and 5 more)" in str(error)

    def test_repr(self):
        from SHARED.contracts.exceptions import ProtocolValidationError

        error = ProtocolValidationError("MSG", ["err1", "err2"])
        repr_str = repr(error)
        assert "ProtocolValidationError" in repr_str
        assert "MSG" in repr_str


class TestSchemaNotFoundError:
    """Tests for SchemaNotFoundError exception."""

    def test_creation(self):
        from SHARED.contracts.exceptions import SchemaNotFoundError

        error = SchemaNotFoundError("UNKNOWN_TYPE")
        assert error.message_type == "UNKNOWN_TYPE"
        assert "UNKNOWN_TYPE" in str(error)


class TestInvalidMessageError:
    """Tests for InvalidMessageError exception."""

    def test_creation(self):
        from SHARED.contracts.exceptions import InvalidMessageError

        error = InvalidMessageError("Missing fields")
        assert error.reason == "Missing fields"
        assert error.message_data is None

    def test_with_message_data(self):
        from SHARED.contracts.exceptions import InvalidMessageError

        data = {"bad": "data"}
        error = InvalidMessageError("Bad format", data)
        assert error.message_data == data
        assert "Bad format" in str(error)
