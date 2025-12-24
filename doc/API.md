# API Reference Documentation

**Document Version**: 1.0  
**Last Updated**: December 2025

---

## Overview

This document provides comprehensive API documentation for all public classes and functions in the AI Agent League Competition System.

---

## Table of Contents

1. [league_sdk Module](#league_sdk-module)
2. [Configuration Classes](#configuration-classes)
3. [Repository Classes](#repository-classes)
4. [Logger Classes](#logger-classes)
5. [Protocol Types](#protocol-types)
6. [Agent Interfaces](#agent-interfaces)

---

## league_sdk Module

### config_loader.py

#### `load_system_config()`

Load the global system configuration.

**Returns:**
- `dict`: System configuration dictionary with network, timeout, and retry settings.

**Raises:**
- `FileNotFoundError`: If system.json is not found.
- `json.JSONDecodeError`: If file contains invalid JSON.

**Example:**
```python
from SHARED.league_sdk.config_loader import load_system_config

config = load_system_config()
print(config['timeouts']['move_timeout_sec'])  # 30
```

---

#### `load_agents_config()`

Load the agents configuration registry.

**Returns:**
- `dict`: Contains league_manager, referees[], and players[] configurations.

**Raises:**
- `FileNotFoundError`: If agents_config.json is not found.

**Example:**
```python
from SHARED.league_sdk.config_loader import load_agents_config

agents = load_agents_config()
for player in agents['players']:
    print(f"{player['id']}: {player['endpoint']}")
```

---

#### `load_league_config(league_id: str)`

Load configuration for a specific league.

**Parameters:**
- `league_id` (str): The unique identifier for the league.

**Returns:**
- `dict`: League configuration including scoring, participants, and schedule settings.

**Raises:**
- `FileNotFoundError`: If league configuration file is not found.

**Example:**
```python
config = load_league_config('league_2025_even_odd')
print(config['scoring']['win_points'])  # 2
```

---

#### `ConfigLoader` (class)

Centralized configuration loader with caching.

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `load_system()` | None | `SystemConfig` | Load cached system config |
| `load_agents()` | None | `AgentsConfig` | Load cached agents config |
| `load_league(league_id)` | `str` | `LeagueConfig` | Load cached league config |
| `get_referee_by_id(id)` | `str` | `RefereeConfig` | Find referee by ID |
| `get_player_by_id(id)` | `str` | `PlayerConfig` | Find player by ID |

---

## Configuration Classes

### config_models.py

#### `SystemConfig` (dataclass)

```python
@dataclass
class SystemConfig:
    schema_version: str
    system_id: str
    protocol_version: str
    timeouts: Dict[str, int]
    retry_policy: Dict[str, Any]
```

**Fields:**
- `schema_version`: Configuration schema version (e.g., "1.0.0")
- `system_id`: Unique system identifier
- `protocol_version`: Protocol version (e.g., "league.v2")
- `timeouts`: Timeout values in seconds
- `retry_policy`: Retry configuration

---

#### `AgentConfig` (dataclass)

```python
@dataclass
class AgentConfig:
    agent_id: str
    agent_type: str
    display_name: str
    port: int
    endpoint: str
    capabilities: Optional[List[str]] = None
```

---

#### `LeagueConfig` (dataclass)

```python
@dataclass
class LeagueConfig:
    league_id: str
    game_type: str
    status: str
    scoring: ScoringConfig
    total_rounds: int
    matches_per_round: int
```

---

## Repository Classes

### repositories.py

#### `StandingsRepository` (class)

Manages league standings data persistence.

**Constructor:**
```python
StandingsRepository(league_id: str, data_root: Path = DATA_ROOT)
```

**Parameters:**
- `league_id` (str): The league identifier.
- `data_root` (Path, optional): Root data directory.

**Methods:**

##### `load() -> Dict`

Load current standings from file.

**Returns:**
- `dict`: Standings data including rankings and player statistics.

**Example:**
```python
repo = StandingsRepository('league_2025_even_odd')
standings = repo.load()
for player in standings['standings']:
    print(f"{player['rank']}. {player['display_name']}: {player['points']} pts")
```

##### `save(standings: Dict) -> None`

Save standings to file with timestamp.

**Parameters:**
- `standings` (dict): Complete standings data to save.

##### `update_player(player_id: str, result: str, points: int) -> None`

Update a player's standings after a match.

**Parameters:**
- `player_id` (str): Player identifier
- `result` (str): Match result ("WIN", "LOSS", or "DRAW")
- `points` (int): Points to add

---

#### `MatchRepository` (class)

Manages individual match data persistence.

**Constructor:**
```python
MatchRepository(league_id: str, data_root: Path = DATA_ROOT)
```

**Methods:**

##### `save_match(match_id: str, match_data: Dict) -> None`

Save match data to JSON file.

##### `get_match(match_id: str) -> Optional[Dict]`

Retrieve match data by ID.

**Returns:**
- `dict` or `None`: Match data if found, None otherwise.

##### `list_matches() -> List[str]`

List all match IDs in the league.

---

#### `PlayerHistoryRepository` (class)

Manages player match history for strategy building.

**Constructor:**
```python
PlayerHistoryRepository(player_id: str, data_root: Path = DATA_ROOT)
```

**Methods:**

##### `get_history() -> Optional[Dict]`

Get player's complete match history.

##### `add_match_result(match_result: Dict) -> None`

Add a new match result to history.

**Parameters:**
- `match_result` (dict): Match result data including opponent, choice, result.

---

## Logger Classes

### logger.py

#### `JsonLogger` (class)

JSONLines logger for structured event logging.

**Constructor:**
```python
JsonLogger(component: str, league_id: Optional[str] = None)
```

**Parameters:**
- `component` (str): Component identifier (e.g., "league_manager")
- `league_id` (str, optional): League context for logging

**Methods:**

##### `log(event_type: str, level: str = "INFO", **details) -> None`

Log an event with optional details.

**Parameters:**
- `event_type` (str): Event type identifier
- `level` (str): Log level (DEBUG, INFO, WARNING, ERROR)
- `**details`: Additional key-value details

##### `info(event_type: str, **details) -> None`

Shorthand for INFO level logging.

##### `error(event_type: str, **details) -> None`

Shorthand for ERROR level logging.

##### `debug(event_type: str, **details) -> None`

Shorthand for DEBUG level logging.

##### `warning(event_type: str, **details) -> None`

Shorthand for WARNING level logging.

**Example:**
```python
logger = JsonLogger("referee", "league_2025_even_odd")
logger.info("MATCH_STARTED", match_id="R1M1", players=["P01", "P02"])
logger.error("TIMEOUT", match_id="R1M1", player_id="P02", timeout_sec=30)
```

---

#### `AgentLogger` (class)

Agent-specific logger with message direction tracking.

**Constructor:**
```python
AgentLogger(agent_id: str, logs_dir: Path = LOG_ROOT)
```

**Methods:**

##### `log_sent(message_type: str, peer: str, details: dict = None) -> None`

Log a sent message.

##### `log_received(message_type: str, peer: str, details: dict = None) -> None`

Log a received message.

**Example:**
```python
logger = AgentLogger("P01")
logger.log_sent("PARITY_CHOICE", "REF01", {"choice": "even"})
logger.log_received("GAME_OVER", "REF01", {"result": "WIN"})
```

---

## Protocol Types

### protocol_types.py

#### Message Type Constants

```python
class MessageType:
    REFEREE_REGISTER_REQUEST = "REFEREE_REGISTER_REQUEST"
    REFEREE_REGISTER_RESPONSE = "REFEREE_REGISTER_RESPONSE"
    LEAGUE_REGISTER_REQUEST = "LEAGUE_REGISTER_REQUEST"
    LEAGUE_REGISTER_RESPONSE = "LEAGUE_REGISTER_RESPONSE"
    ROUND_ANNOUNCEMENT = "ROUND_ANNOUNCEMENT"
    GAME_INVITATION = "GAME_INVITATION"
    GAME_JOIN_ACK = "GAME_JOIN_ACK"
    CHOOSE_PARITY_CALL = "CHOOSE_PARITY_CALL"
    PARITY_CHOICE = "PARITY_CHOICE"
    GAME_OVER = "GAME_OVER"
    MATCH_RESULT_REPORT = "MATCH_RESULT_REPORT"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    INVALID_MOVE_ERROR = "INVALID_MOVE_ERROR"
```

---

## Agent Interfaces

### Player Strategy Interface

All player strategies must implement:

```python
class StrategyInterface:
    def choose_parity(self, opponent_history: List[str]) -> str:
        """
        Choose a parity based on opponent history.
        
        Parameters:
            opponent_history: List of opponent's previous choices
            
        Returns:
            str: "even" or "odd"
        """
        pass
```

### Available Strategies

| Strategy | Class | Description |
|----------|-------|-------------|
| random | `RandomStrategy` | 50/50 random choice |
| frequency | `FrequencyStrategy` | Counter opponent's most common |
| pattern | `PatternStrategy` | Detect 3-choice patterns |
| timeout | `TimeoutStrategy` | Test timeout handling |

---

**Document Owner**: Assignment 7 Team  
**Status**: ✅ Complete
