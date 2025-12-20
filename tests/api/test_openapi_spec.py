"""Tests for OpenAPI specification validation."""

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_openapi_json_accessible():
    """Test that OpenAPI JSON spec is accessible."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

def test_openapi_spec_structure():
    """Test that OpenAPI spec has required fields."""
    response = client.get("/openapi.json")
    spec = response.json()

    assert "openapi" in spec
    assert "info" in spec
    assert "paths" in spec

def test_openapi_info_complete():
    """Test that OpenAPI info section is complete."""
    response = client.get("/openapi.json")
    spec = response.json()
    info = spec["info"]

    assert info["title"] == "League Competition API"
    assert info["version"] == "1.0.0"
    assert "description" in info
    assert "contact" in info
    assert "license" in info

def test_all_endpoints_documented():
    """Test that all major endpoints are documented."""
    response = client.get("/openapi.json")
    spec = response.json()
    paths = spec["paths"]

    required_paths = [
        "/health",
        "/api/v1/league/status",
        "/api/v1/league/standings",
        "/api/v1/games",
        "/api/v1/matches",
        "/api/v1/players",
    ]

    for path in required_paths:
        assert path in paths, f"Path {path} not documented"

def test_swagger_ui_accessible():
    """Test that Swagger UI is accessible."""
    response = client.get("/docs")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_redoc_accessible():
    """Test that ReDoc is accessible."""
    response = client.get("/redoc")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_endpoints_have_tags():
    """Test that endpoints have proper tags."""
    response = client.get("/openapi.json")
    spec = response.json()

    for path, methods in spec["paths"].items():
        for method, details in methods.items():
            if method != "parameters":
                assert "tags" in details, f"{method} {path} missing tags"

def test_responses_have_schemas():
    """Test that endpoints define response schemas."""
    response = client.get("/openapi.json")
    spec = response.json()

    for path, methods in spec["paths"].items():
        for method, details in methods.items():
            if method in ["get", "post", "put", "delete"]:
                assert "responses" in details
                assert "200" in details["responses"] or "201" in details["responses"]
