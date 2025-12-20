## API Test Suite Documentation

### Phase 14: API Testing - COMPLETE ✅

This directory contains comprehensive tests for the REST API layer (Phase 13).

### Test Files Created

1. **test_league_routes.py** (80 lines)
   - Tests for `/api/v1/league/status` endpoint
   - Tests for `/api/v1/league/standings` endpoint  
   - Health check and root endpoint tests
   - 5 test functions

2. **test_matches_routes.py** (78 lines)
   - Tests for `/api/v1/matches` list endpoint
   - Tests for `/api/v1/matches/{match_id}` detail endpoint
   - Pagination and filtering tests
   - 404 error handling tests
   - 5 test functions

3. **test_players_routes.py** (96 lines)
   - Tests for `/api/v1/players` list endpoint
   - Tests for `/api/v1/players/{player_id}` detail endpoint
   - Tests for `/api/v1/players/{player_id}/history` endpoint
   - 404 error handling tests
   - 5 test functions

4. **test_games_routes.py** (63 lines)
   - Tests for `/api/v1/games` list endpoint
   - Tests for `/api/v1/games/{game_id}` detail endpoint
   - Game validation tests (player ranges, rules)
   - 404 error handling tests
   - 7 test functions

5. **test_api_integration.py** (96 lines)
   - Full API workflow integration tests
   - Response format compliance tests
   - Data consistency tests (rankings, points)
   - 3 integration test functions

6. **test_api_performance.py** (66 lines)
   - Response time benchmarks (<0.1s for health, <0.5s for games)
   - Concurrent request handling (20 requests, 10 workers)
   - Multiple endpoint performance tests
   - Pagination performance tests
   - 5 performance test functions

7. **test_openapi_spec.py** (95 lines)
   - OpenAPI JSON specification validation
   - Swagger UI and ReDoc accessibility tests
   - Endpoint documentation completeness checks
   - Response schema validation
   - 9 specification test functions

8. **test_websocket.py** (146 lines)
   - WebSocket connection establishment tests
   - Ping/pong functionality tests
   - Subscribe/unsubscribe to match events
   - Error handling for invalid JSON
   - Event structure validation for all event types:
     - MatchStartEvent
     - PlayerThinkingEvent
     - PlayerMoveEvent
     - RoundResultEvent
     - MatchEndEvent
   - 13 WebSocket test functions

### Test Summary

- **Total Test Files**: 8
- **Total Test Functions**: 52
- **Total Lines of Code**: ~620 lines
- **Coverage Areas**:
  - ✅ All REST API endpoints
  - ✅ WebSocket live updates
  - ✅ Error handling (404, invalid data)
  - ✅ Performance benchmarks
  - ✅ OpenAPI/Swagger compliance
  - ✅ Integration workflows
  - ✅ Event structures

### Running the Tests

#### Prerequisites
```bash
# Install the project in editable mode
pip install -e .

# Ensure pytest and dependencies are installed
pip install pytest pytest-cov fastapi[all] httpx
```

#### Run All API Tests
```bash
python -m pytest tests/api/ -v
```

#### Run Specific Test File
```bash
python -m pytest tests/api/test_games_routes.py -v
```

#### Run Specific Test Function
```bash
python -m pytest tests/api/test_games_routes.py::test_list_games_success -v
```

#### Run with Coverage
```bash
python -m pytest tests/api/ --cov=api --cov-report=html
```

### Known Issues

**Import Path Configuration**:
The tests require the project root to be in Python's path. We've created:
- `tests/conftest.py` - Root level pytest configuration
- `tests/api/conftest.py` - API-specific pytest configuration
- `pytest.ini` - Project-wide pytest settings with `pythonpath = .`

If imports fail, you can run tests with explicit PYTHONPATH:
```bash
# Windows
set PYTHONPATH=%CD% && python -m pytest tests/api/ -v

# Linux/Mac
PYTHONPATH=. python -m pytest tests/api/ -v
```

### Test Design Principles

1. **Isolation**: Each test uses fixtures for test data setup
2. **Mocking**: Tests use FastAPI's TestClient (no actual server needed)
3. **Coverage**: Tests cover success paths, error paths, and edge cases
4. **Performance**: Performance tests set realistic benchmarks
5. **Documentation**: OpenAPI tests ensure API is well-documented

### Future Enhancements

- Add authentication/authorization tests when implemented
- Add rate limiting tests
- Add database transaction rollback for integration tests
- Add load testing with locust or similar tools
- Add contract testing with Pact or similar frameworks

### Phase 14 Completion Status

✅ **100% COMPLETE** - All planned test files created and documented

**Next Steps**: 
- Phase 15: GUI Testing (tests/gui/)
- Phase 16: Final Integration Testing
