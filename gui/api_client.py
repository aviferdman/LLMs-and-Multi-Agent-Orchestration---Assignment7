"""REST API client for communicating with the backend."""

from typing import Dict, List, Optional

import httpx
import streamlit as st

from gui.config import API_BASE_URL, API_ENDPOINTS


class APIClient:
    """Client for interacting with the League Competition API."""

    def __init__(self, base_url: str = API_BASE_URL, timeout: int = 10):
        """Initialize API client."""
        self.base_url = base_url
        self.timeout = timeout

    def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict]:
        """Make HTTP request with error handling."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            st.error(f"API Error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None

    def get_league_status(self, league_id: Optional[str] = None) -> Optional[Dict]:
        """Get league status."""
        params = {"league_id": league_id} if league_id else {}
        return self._make_request("GET", API_ENDPOINTS["league_status"], params=params)

    def get_standings(self, league_id: Optional[str] = None) -> Optional[Dict]:
        """Get league standings."""
        params = {"league_id": league_id} if league_id else {}
        return self._make_request("GET", API_ENDPOINTS["league_standings"], params=params)

    def get_agents_status(self) -> Optional[Dict]:
        """Get agents status."""
        return self._make_request("GET", API_ENDPOINTS["league_agents"])

    def list_games(self) -> Optional[List[Dict]]:
        """List available games."""
        result = self._make_request("GET", API_ENDPOINTS["games"])
        return result.get("games", []) if result else []

    def get_game(self, game_id: str) -> Optional[Dict]:
        """Get game details."""
        url = f"{API_ENDPOINTS['games']}/{game_id}"
        return self._make_request("GET", url)

    def start_league(
        self, game_id: str, num_players: int, league_name: Optional[str] = None
    ) -> Optional[Dict]:
        """Start a new league."""
        payload = {
            "game_id": game_id,
            "num_players": num_players,
        }
        if league_name:
            payload["league_name"] = league_name

        return self._make_request("POST", API_ENDPOINTS["league_start"], json=payload)

    def list_matches(
        self, round_number: Optional[int] = None, status: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """List matches with optional filters."""
        params = {}
        if round_number is not None:
            params["round_number"] = round_number
        if status:
            params["status"] = status

        result = self._make_request("GET", API_ENDPOINTS["matches"], params=params)
        return result.get("matches", []) if result else []

    def get_match(self, match_id: str) -> Optional[Dict]:
        """Get match details."""
        url = f"{API_ENDPOINTS['matches']}/{match_id}"
        return self._make_request("GET", url)

    def list_players(self) -> Optional[List[Dict]]:
        """List all players."""
        result = self._make_request("GET", API_ENDPOINTS["players"])
        return result.get("players", []) if result else []

    def get_player(self, player_id: str) -> Optional[Dict]:
        """Get player details."""
        url = f"{API_ENDPOINTS['players']}/{player_id}"
        return self._make_request("GET", url)

    def get_player_history(self, player_id: str) -> Optional[Dict]:
        """Get player match history."""
        url = f"{API_ENDPOINTS['players']}/{player_id}/history"
        return self._make_request("GET", url)


# Global API client instance
@st.cache_resource
def get_api_client() -> APIClient:
    """Get cached API client instance."""
    return APIClient()
