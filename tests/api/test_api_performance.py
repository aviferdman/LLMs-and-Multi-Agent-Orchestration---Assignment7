"""Performance tests for API endpoints."""

import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_health_check_response_time():
    """Test that health check responds quickly."""
    start = time.time()
    response = client.get("/health")
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 0.1

def test_games_list_response_time():
    """Test that games list responds quickly."""
    start = time.time()
    response = client.get("/api/v1/games")
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 0.5

def test_concurrent_requests():
    """Test handling of concurrent requests."""

    def make_request():
        return client.get("/health")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(20)]
        results = [f.result() for f in futures]

    assert all(r.status_code == 200 for r in results)

def test_multiple_endpoint_calls():
    """Test performance of multiple different endpoints."""
    endpoints = [
        "/health",
        "/api/v1/games",
        "/api/v1/league/status",
        "/api/v1/matches",
        "/api/v1/players",
    ]

    start = time.time()
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code in [200, 404, 500]
    duration = time.time() - start

    assert duration < 2.0

def test_pagination_performance():
    """Test pagination doesn't degrade performance significantly."""
    start1 = time.time()
    response1 = client.get("/api/v1/matches?skip=0&limit=10")
    duration1 = time.time() - start1

    start2 = time.time()
    response2 = client.get("/api/v1/matches?skip=10&limit=10")
    duration2 = time.time() - start2

    assert response1.status_code in [200, 404]
    assert response2.status_code in [200, 404]
    assert abs(duration1 - duration2) < 0.5
