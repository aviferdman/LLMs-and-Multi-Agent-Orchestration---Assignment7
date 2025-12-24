# ADR 002: HTTP Protocol Choice

**Status**: Accepted  
**Date**: 2025-12-20  
**Context**: Inter-Agent Communication Protocol

## Context

Agents in the league competition system need to communicate for registration, match coordination, and result reporting. We need a reliable, simple protocol for inter-agent messaging.

## Decision

We use **HTTP/REST with JSON payloads** for all inter-agent communication.

## Rationale

### Why HTTP?
1. **Ubiquity**: Every programming language has HTTP libraries
2. **Simplicity**: Well-understood request/response model
3. **Tooling**: Easy to debug (curl, Postman, browser dev tools)
4. **Firewall-friendly**: Port 80/443 typically allowed
5. **Stateless**: Each message is independent

### Why JSON?
1. **Human-readable**: Easy to debug and inspect
2. **Schema validation**: Pydantic models for type safety
3. **Language-agnostic**: Supported everywhere
4. **Compact**: Reasonable size for our messages
5. **Nested structures**: Supports complex message formats

### Implementation Details
- **FastAPI** framework for HTTP servers
- **httpx** library for HTTP clients
- **POST /mcp** endpoint on all agents (Model Communication Protocol)
- **Timeout**: 30 seconds default
- **Retry**: 3 attempts with exponential backoff

## Consequences

### Positive
- No additional infrastructure needed (no message broker)
- Synchronous request/response is easier to reason about
- Built-in error handling (HTTP status codes)
- Easy to implement in any language
- Simple to test and debug

### Negative
- Not suitable for real-time streaming (addressed by WebSocket in API layer)
- Blocking calls can cause cascading delays
- No built-in message queuing
- Higher latency than binary protocols

## Alternatives Considered

1. **gRPC**: Rejected - too complex for this scope, binary protocol harder to debug
2. **WebSockets**: Rejected for agent-to-agent (used in API layer for live updates)
3. **MQTT**: Rejected - requires message broker infrastructure
4. **Raw TCP Sockets**: Rejected - too low-level, need to build protocol
5. **Message Queue (RabbitMQ/Kafka)**: Rejected - over-engineered for requirements

## Security Considerations

- **Authentication**: Token-based (auth_token in messages)
- **HTTPS**: Should be used in production (currently HTTP for simplicity)
- **Rate Limiting**: Not implemented (trusted environment)

## Related Decisions
- ADR 001: Three-Layer Architecture
- ADR 003: JSON Message Format
- ADR 005: FastAPI Framework
