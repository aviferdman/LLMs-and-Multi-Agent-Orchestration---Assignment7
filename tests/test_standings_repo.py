"""Unit tests for StandingsRepository."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import os
import tempfile
import shutil
from SHARED.league_sdk.repositories import StandingsRepository

class TestStandingsRepository:
    """Test StandingsRepository class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo = StandingsRepository("test_league", Path(self.temp_dir))
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_standings(self):
        """Test saving and loading standings."""
        standings = {
            "version": 1,
            "standings": [
                {"player_id": "P01", "points": 3, "rank": 1}
            ]
        }
        
        self.repo.save(standings)
        loaded = self.repo.load()
        
        assert loaded["version"] == 1
        assert len(loaded["standings"]) == 1
        assert loaded["standings"][0]["player_id"] == "P01"
    
    def test_update_player(self):
        """Test updating player stats."""
        standings = {
            "version": 1,
            "standings": [
                {"player_id": "P01", "wins": 0, "losses": 0, 
                 "draws": 0, "games_played": 0, "rank": 1}
            ]
        }
        
        self.repo.save(standings)
        self.repo.update_player("P01", wins=1)
        
        loaded = self.repo.load()
        assert loaded["standings"][0]["wins"] == 1
        assert loaded["standings"][0]["games_played"] == 1

if __name__ == "__main__":
    print("=" * 60)
    print("STANDINGS REPOSITORY TESTS")
    print("=" * 60)
    
    sr = TestStandingsRepository()
    sr.setup_method()
    try:
        sr.test_save_and_load_standings()
        print("  ✓ save_and_load_standings")
    except Exception as e:
        print(f"  ✗ save_and_load_standings: {e}")
    finally:
        sr.teardown_method()
    
    sr = TestStandingsRepository()
    sr.setup_method()
    try:
        sr.test_update_player()
        print("  ✓ update_player")
    except Exception as e:
        print(f"  ✗ update_player: {e}")
    finally:
        sr.teardown_method()
    
    print("\n✅ STANDINGS REPOSITORY TESTS COMPLETED!")
