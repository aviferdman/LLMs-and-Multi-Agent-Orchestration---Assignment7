# ADR 005: FastAPI Framework Choice

**Status**: Accepted  
**Date**: 2025-12-20  
**Context**: HTTP Server Framework Selection

## Context

All agents (League Manager, Referees, Players) need HTTP servers to receive messages. We need a Python framework that is simple, performant, and provides good developer experience.

## Decision

We use **FastAPI** as the HTTP server framework for all agents.

## Rationale

### Why FastAPI?

1. **Modern Python**: Built on Python 3.6+ with type hints
2. **Performance**: One of fastest Python frameworks (via Starlette + Pydantic)
3. **Async/Await**: Native support for asynchronous operations
4. **Auto Documentation**: Built-in OpenAPI/Swagger generation
5. **Type Safety**: Automatic request/response validation via Pydantic
6. **Easy Testing**: Excellent test client support
7. **Minimal Boilerplate**: Clean, concise syntax

### Implementation Benefits

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/mcp")
async def handle_message(message: dict):
    # Automatic validation, JSON parsing
    return {"status": "ok"}
```

### Key Features Used

1. **POST /mcp endpoint**: All agents expose this
2. **Pydantic Models**: Schema validation for messages
3. **CORS Middleware**: Enable cross-origin requests (for GUI)
4. **Lifespan Events**: Startup/shutdown hooks
5. **WebSocket Support**: For real-time updates (API layer)
6. **OpenAPI/Swagger**: Auto-generated documentation

### Development Experience

- **Hot Reload**: `uvicorn --reload` for development
- **Interactive Docs**: `/docs` endpoint for testing
- **Error Messages**: Clear validation errors
- **Type Hints**: IDE autocomplete and type checking

## Technical Stack

- **FastAPI**: Application framework
- **Uvicorn**: ASGI server (production-ready)
- **Pydantic**: Data validation
- **Starlette**: Low-level toolkit (FastAPI built on this)
- **httpx**: HTTP client for inter-agent communication

## Consequences

### Positive
- **Rapid Development**: Write less code, get more features
- **Type Safety**: Catch errors at development time
- **Performance**: Comparable to Node.js/Go frameworks
- **Documentation**: API docs generated automatically
- **Community**: Active development, good support
- **Testing**: Built-in test client simplifies unit tests

### Negative
- **Python-Only**: Can't mix languages (not a concern here)
- **Learning Curve**: Requires understanding async/await
- **Dependency**: Framework-specific patterns
- **Version Compatibility**: Must maintain Python 3.6+

## Code Example: Agent Structure

```python
from fastapi import FastAPI
from SHARED.constants import MessageType

app = FastAPI(title="Player Agent P01")

@app.post("/mcp")
async def handle_message(message: dict):
    msg_type = message.get("message_type")
    
    if msg_type == MessageType.GAME_INVITATION:
        return handle_game_invitation(message)
    elif msg_type == MessageType.CHOOSE_PARITY_CALL:
        return handle_parity_call(message)
    
    return {"status": "unknown_message_type"}

@app.on_event("startup")
async def startup():
    # Register with league manager
    await register_with_league()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8101)
```

## Alternatives Considered

1. **Flask**: Rejected - synchronous, slower, no built-in validation
2. **Django**: Rejected - too heavy, ORM not needed, complex setup
3. **Tornado**: Rejected - older async model, less ergonomic
4. **Sanic**: Rejected - similar to FastAPI but smaller community
5. **aiohttp**: Rejected - lower level, more boilerplate
6. **Bottle**: Rejected - too minimal, lacks features

## Performance Benchmarks

FastAPI performance (from TechEmpower benchmarks):
- **Requests/sec**: ~60,000 (comparable to Go)
- **Latency**: <10ms for simple endpoints
- **Memory**: Low overhead

For our use case (4 players, 2 referees, <100 req/sec):
- ✅ More than adequate
- ✅ Not a bottleneck

## Testing Approach

```python
from fastapi.testclient import TestClient

def test_message_handling():
    client = TestClient(app)
    response = client.post("/mcp", json={
        "message_type": "GAME_INVITATION",
        # ...
    })
    assert response.status_code == 200
```

## Related Decisions
- ADR 002: HTTP Protocol Choice
- ADR 001: Three-Layer Architecture

## Future Considerations

- **Authentication**: Can add OAuth2 if needed
- **Rate Limiting**: FastAPI-limiter available
- **Monitoring**: Prometheus metrics integration
- **GraphQL**: FastAPI + Strawberry if needed
