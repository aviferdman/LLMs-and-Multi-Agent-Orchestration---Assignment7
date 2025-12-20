"""Tests for GUI API client module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from gui.api_client import APIClient


class TestAPIClient:
    """Tests for the APIClient class."""

    def test_init_with_custom_base_url(self):
        """Test initializing APIClient with custom base URL."""
        custom_url = "http://localhost:9000/api/v1"
        client = APIClient(base_url=custom_url)
        assert client.base_url == custom_url

    def test_init_with_default_base_url(self):
        """Test initializing APIClient with default base URL."""
        client = APIClient()
        assert "api/v1" in client.base_url
        assert client.base_url.startswith("http://")

    @patch('gui.api_client.requests.get')
    def test_get_league_status_success(self, mock_get):
        """Test successful retrieval of league status."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "active",
            "current_round": 2,
            "total_rounds": 6
        }
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_league_status()

        assert result["status"] == "active"
        assert result["current_round"] == 2
        assert result["total_rounds"] == 6
        mock_get.assert_called_once()

    @patch('gui.api_client.requests.get')
    def test_get_league_status_error(self, mock_get):
        """Test error handling when getting league status."""
        mock_get.side_effect = Exception("Connection error")

        client = APIClient()
        result = client.get_league_status()

        assert result is None or isinstance(result, dict)

    @patch('gui.api_client.requests.get')
    def test_get_standings_success(self, mock_get):
        """Test successful retrieval of standings."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "standings": [
                {"player_id": "player_01", "rank": 1, "points": 10},
                {"player_id": "player_02", "rank": 2, "points": 8}
            ]
        }
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_standings()

        assert len(result["standings"]) == 2
        assert result["standings"][0]["rank"] == 1
        mock_get.assert_called_once()

    @patch('gui.api_client.requests.get')
    def test_get_matches_with_filters(self, mock_get):
        """Test getting matches with filter parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "matches": [],
            "total": 0
        }
        mock_get.return_value = mock_response

        client = APIClient()
        client.get_matches(status="completed", round_number=1)

        # Verify the request was made with query parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "params" in call_args.kwargs or len(call_args.args) > 1

    @patch('gui.api_client.requests.get')
    def test_get_players_success(self, mock_get):
        """Test successful retrieval of players."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "players": [
                {"player_id": "player_01", "strategy": "random"},
                {"player_id": "player_02", "strategy": "smart"}
            ]
        }
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_players()

        assert len(result["players"]) == 2
        mock_get.assert_called_once()

    @patch('gui.api_client.requests.get')
    def test_get_player_by_id_success(self, mock_get):
        """Test getting specific player by ID."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "player_id": "player_01",
            "strategy": "random",
            "stats": {"wins": 5, "losses": 3}
        }
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_player_by_id("player_01")

        assert result["player_id"] == "player_01"
        assert result["stats"]["wins"] == 5
        mock_get.assert_called_once()

    @patch('gui.api_client.requests.get')
    def test_get_player_history_success(self, mock_get):
        """Test getting player match history."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "player_id": "player_01",
            "history": [
                {"match_id": "match_1", "result": "win"},
                {"match_id": "match_2", "result": "loss"}
            ]
        }
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_player_history("player_01")

        assert len(result["history"]) == 2
        mock_get.assert_called_once()

    @patch('gui.api_client.requests.get')
    def test_get_games_success(self, mock_get):
        """Test getting available games."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "games": [
                {"game_id": "even_odd", "name": "Even-Odd Game"}
            ]
        }
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_games()

        assert len(result["games"]) == 1
        assert result["games"][0]["game_id"] == "even_odd"
        mock_get.assert_called_once()

    @patch('gui.api_client.requests.get')
    def test_timeout_handling(self, mock_get):
        """Test handling of request timeout."""
        from requests.exceptions import Timeout
        mock_get.side_effect = Timeout("Request timeout")

        client = APIClient()
        result = client.get_league_status()

        # Should handle timeout gracefully
        assert result is None or isinstance(result, dict)

    @patch('gui.api_client.requests.get')
    def test_connection_error_handling(self, mock_get):
        """Test handling of connection errors."""
        from requests.exceptions import ConnectionError
        mock_get.side_effect = ConnectionError("Cannot connect")

        client = APIClient()
        result = client.get_standings()

        # Should handle connection error gracefully
        assert result is None or isinstance(result, dict)

    @patch('gui.api_client.requests.get')
    def test_invalid_json_response(self, mock_get):
        """Test handling of invalid JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_league_status()

        # Should handle invalid JSON gracefully
        assert result is None or isinstance(result, dict)

    @patch('gui.api_client.requests.get')
    def test_404_error_handling(self, mock_get):
        """Test handling of 404 Not Found errors."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not found"}
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_player_by_id("nonexistent_player")

        # Should handle 404 gracefully
        assert result is None or "error" in result

    @patch('gui.api_client.requests.get')
    def test_500_error_handling(self, mock_get):
        """Test handling of 500 Server Error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal server error"}
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_matches()

        # Should handle 500 error gracefully
        assert result is None or "error" in result
