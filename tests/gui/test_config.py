"""Tests for GUI configuration module."""

import pytest
from pathlib import Path

import gui.config as config

class TestGUIConfig:
    """Tests for the GUI configuration module."""

    def test_api_base_url(self):
        """Test API base URL configuration."""
        assert config.API_BASE_URL is not None
        assert "127.0.0.1" in config.API_BASE_URL or "localhost" in config.API_BASE_URL

    def test_websocket_url(self):
        """Test WebSocket URL configuration."""
        assert config.WEBSOCKET_URL is not None
        assert config.WEBSOCKET_URL.startswith("ws://")

    def test_page_title(self):
        """Test page title configuration."""
        assert config.PAGE_TITLE is not None
        assert len(config.PAGE_TITLE) > 0

    def test_page_icon(self):
        """Test page icon configuration."""
        assert config.PAGE_ICON is not None
        assert len(config.PAGE_ICON) > 0

    def test_refresh_intervals(self):
        """Test refresh interval configurations."""
        assert config.REFRESH_INTERVAL_DASHBOARD > 0
        assert config.REFRESH_INTERVAL_LIVE > 0
        assert config.REFRESH_INTERVAL_STANDINGS > 0
        assert isinstance(config.REFRESH_INTERVAL_DASHBOARD, int)

    def test_api_endpoints(self):
        """Test API endpoints are defined."""
        assert "league_status" in config.API_ENDPOINTS
        assert "league_standings" in config.API_ENDPOINTS
        assert "games" in config.API_ENDPOINTS
        assert "matches" in config.API_ENDPOINTS
        assert "players" in config.API_ENDPOINTS

    def test_colors_defined(self):
        """Test color scheme is defined."""
        assert "primary" in config.COLORS
        assert "secondary" in config.COLORS
        assert "success" in config.COLORS
        assert "warning" in config.COLORS
        assert "danger" in config.COLORS

    def test_status_icons_defined(self):
        """Test status icons are defined."""
        assert "waiting" in config.STATUS_ICONS
        assert "thinking" in config.STATUS_ICONS
        assert "submitted" in config.STATUS_ICONS
        assert "completed" in config.STATUS_ICONS

    def test_medals_defined(self):
        """Test medals for top players are defined."""
        assert 1 in config.MEDALS
        assert 2 in config.MEDALS
        assert 3 in config.MEDALS

    def test_api_version(self):
        """Test API version is defined."""
        assert config.API_VERSION is not None
        assert isinstance(config.API_VERSION, str)

    def test_layout_configuration(self):
        """Test layout configuration."""
        assert config.LAYOUT is not None
        assert config.LAYOUT in ["wide", "centered"]

    def test_data_directory_path(self):
        """Test data directory path exists."""
        assert config.DATA_DIR is not None
        assert isinstance(config.DATA_DIR, Path)

    def test_project_root_path(self):
        """Test project root path exists."""
        assert config.PROJECT_ROOT is not None
        assert isinstance(config.PROJECT_ROOT, Path)

    def test_url_formats(self):
        """Test URL formats are correct."""
        assert config.API_BASE_URL.startswith(("http://", "https://"))
        assert config.WEBSOCKET_URL.startswith(("ws://", "wss://"))
