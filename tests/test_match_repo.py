"""Unit tests for MatchRepository."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import shutil
import tempfile

import pytest

from SHARED.league_sdk.repositories import MatchRepository


class TestMatchRepository:
    """Test MatchRepository class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo = MatchRepository("test_league", Path(self.temp_dir))

    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_save_and_load_match(self):
        """Test saving and loading match data."""
        match_data = {
            "match_id": "R1M1",
            "player_a": "P01",
            "player_b": "P02",
            "winner": "PLAYER_A",
        }

        self.repo.save_match("R1M1", match_data)
        loaded = self.repo.load_match("R1M1")

        assert loaded["match_id"] == "R1M1"
        assert loaded["player_a"] == "P01"
        assert loaded["winner"] == "PLAYER_A"

    def test_list_matches(self):
        """Test listing all matches."""
        self.repo.save_match("R1M1", {"match_id": "R1M1"})
        self.repo.save_match("R1M2", {"match_id": "R1M2"})

        match_ids = self.repo.list_matches()
        assert len(match_ids) == 2
        assert "R1M1" in match_ids
        assert "R1M2" in match_ids


if __name__ == "__main__":
    print("=" * 60)
    print("MATCH REPOSITORY TESTS")
    print("=" * 60)

    mr = TestMatchRepository()
    mr.setup_method()
    try:
        mr.test_save_and_load_match()
        print("  ✓ save_and_load_match")
    except Exception as e:
        print(f"  ✗ save_and_load_match: {e}")
    finally:
        mr.teardown_method()

    mr = TestMatchRepository()
    mr.setup_method()
    try:
        mr.test_list_matches()
        print("  ✓ list_matches")
    except Exception as e:
        print(f"  ✗ list_matches: {e}")
    finally:
        mr.teardown_method()

    print("\n✅ MATCH REPOSITORY TESTS COMPLETED!")
