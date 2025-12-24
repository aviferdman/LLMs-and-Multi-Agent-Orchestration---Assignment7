"""Unit tests for SHARED.league_sdk.config_loader module.

Tests configuration file loading functionality.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import os

import pytest

from SHARED.league_sdk.config_loader import (
    load_agent_config,
    load_game_config,
    load_league_config,
    load_system_config,
)


def test_load_system_config():
    """Test loading system configuration."""
    config = load_system_config()

    assert config is not None
    assert hasattr(config, "protocol_version")
    assert config.protocol_version == "league.v2"
    assert hasattr(config, "timeouts")
    assert hasattr(config, "retry_policy")


def test_load_league_config():
    """Test loading league configuration."""
    league_id = "league_2025_even_odd"
    config = load_league_config(league_id)

    assert config is not None
    assert config.league_id == league_id
    assert config.game_type == "even_odd"
    assert hasattr(config, "scoring")
    assert config.status == "ACTIVE"
    assert config.participants is not None
    assert config.participants.min_players == 2


def test_load_agent_config():
    """Test loading agent configuration."""
    config = load_agent_config()

    assert config is not None
    assert "league_manager" in config
    assert "referees" in config
    assert "players" in config

    # Verify league manager
    lm = config["league_manager"]
    assert lm["agent_id"] == "LM01"
    assert lm["version"] == "1.0.0"

    # Verify referees
    assert len(config["referees"]) == 2
    assert config["referees"][0]["referee_id"] == "REF01"
    assert config["referees"][0]["max_concurrent_matches"] == 1

    # Verify players
    assert len(config["players"]) == 4
    assert config["players"][0]["player_id"] == "P01"
    assert config["players"][0]["active"] is True


def test_load_game_config():
    """Test loading game configuration."""
    game_type = "even_odd"
    config = load_game_config(game_type)

    assert config is not None
    assert config.game_id == game_type
    assert config.game_name == "Even-Odd Parity Game"
    assert hasattr(config, "rules_version")
    assert config.max_players == 2


def test_load_nonexistent_league():
    """Test loading non-existent league raises error."""
    with pytest.raises(FileNotFoundError):
        load_league_config("nonexistent_league")


def test_load_nonexistent_game():
    """Test loading non-existent game raises error."""
    with pytest.raises((FileNotFoundError, KeyError, ValueError)):
        load_game_config("nonexistent_game")


if __name__ == "__main__":
    print("=" * 60)
    print("CONFIG LOADER TESTS")
    print("=" * 60)

    tests = [
        ("load_system_config", test_load_system_config),
        ("load_league_config", test_load_league_config),
        ("load_agent_config", test_load_agent_config),
        ("load_game_config", test_load_game_config),
        ("load_nonexistent_league", test_load_nonexistent_league),
        ("load_nonexistent_game", test_load_nonexistent_game),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            print(f"Testing {name}...", end=" ")
            test_func()
            print("✓")
            passed += 1
        except Exception as e:
            print(f"✗ {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"SUMMARY: {passed}/{len(tests)} tests passed")
    print("=" * 60)

    if failed == 0:
        print("\n✅ ALL CONFIG LOADER TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
