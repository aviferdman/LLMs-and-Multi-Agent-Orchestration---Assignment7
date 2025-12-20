"""Unit tests for PlayerHistoryRepository."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import os
import tempfile
import shutil
from SHARED.league_sdk.repositories import PlayerHistoryRepository

class TestPlayerHistoryRepository:
    """Test PlayerHistoryRepository class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo = PlayerHistoryRepository("P01", Path(self.temp_dir))
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_history(self):
        """Test saving and loading player history."""
        history = {
            "player_id": "P01",
            "matches": [{"match_id": "R1M1", "result": "win"}]
        }
        
        self.repo.save_history(history)
        loaded = self.repo.load_history()
        
        assert loaded["player_id"] == "P01"
        assert len(loaded["matches"]) == 1
    
    def test_append_match(self):
        """Test appending match to history."""
        history = {
            "player_id": "P01",
            "matches": []
        }
        
        self.repo.save_history(history)
        self.repo.append_match({"match_id": "R1M1"})
        
        loaded = self.repo.load_history()
        assert len(loaded["matches"]) == 1

if __name__ == "__main__":
    print("=" * 60)
    print("PLAYER HISTORY REPOSITORY TESTS")
    print("=" * 60)
    
    phr = TestPlayerHistoryRepository()
    phr.setup_method()
    try:
        phr.test_save_and_load_history()
        print("  ✓ save_and_load_history")
    except Exception as e:
        print(f"  ✗ save_and_load_history: {e}")
    finally:
        phr.teardown_method()
    
    phr = TestPlayerHistoryRepository()
    phr.setup_method()
    try:
        phr.test_append_match()
        print("  ✓ append_match")
    except Exception as e:
        print(f"  ✗ append_match: {e}")
    finally:
        phr.teardown_method()
    
    print("\n✅ PLAYER HISTORY REPOSITORY TESTS COMPLETED!")
