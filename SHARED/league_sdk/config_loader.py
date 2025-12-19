"""Configuration loading utilities."""

import json
from pathlib import Path
from typing import Dict, Any
from .config_models import (
    SystemConfig,
    LeagueConfig,
    PlayerConfig,
    RefereeConfig,
    GameConfig,
)

def _load_json(file_path: Path) -> Dict[str, Any]:
    """Load and parse JSON file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_system_config(config_dir: Path = None) -> SystemConfig:
    """Load system configuration."""
    if config_dir is None:
        config_dir = Path("SHARED/config")
    
    config_path = config_dir / "system.json"
    data = _load_json(config_path)
    
    return SystemConfig(
        schema_version=data["schema_version"],
        protocol_version=data.get("protocol_version", "league.v1"),
        timeouts=data.get("timeouts", {}),
        retry_policy=data.get("retry_policy", {}),
    )

def load_league_config(league_id: str, config_dir: Path = None) -> LeagueConfig:
    """Load league configuration."""
    if config_dir is None:
        config_dir = Path("SHARED/config/leagues")
    
    config_path = config_dir / f"{league_id}.json"
    data = _load_json(config_path)
    
    return LeagueConfig(
        league_id=data["league_id"],
        game_type=data["game_type"],
        scoring=data["scoring"],
        total_rounds=data["total_rounds"],
        matches_per_round=data.get("matches_per_round", 2),
    )

def load_agent_config(config_dir: Path = None) -> Dict[str, Any]:
    """Load agent configurations."""
    if config_dir is None:
        config_dir = Path("SHARED/config/agents")
    
    config_path = config_dir / "agents_config.json"
    return _load_json(config_path)

def load_game_config(game_id: str, config_dir: Path = None) -> GameConfig:
    """Load game configuration."""
    if config_dir is None:
        config_dir = Path("SHARED/config/games")
    
    config_path = config_dir / "games_registry.json"
    data = _load_json(config_path)
    
    game_data = data.get("games", {}).get(game_id)
    if not game_data:
        raise ValueError(f"Game {game_id} not found in registry")
    
    return GameConfig(
        game_id=game_id,
        game_name=game_data["game_name"],
        rules_version=game_data["rules_version"],
        max_players=game_data["max_players"],
        metadata=game_data.get("metadata", {}),
    )
