"""Protocol network configuration constants.

Contains port assignments and endpoint URLs.
DEPRECATED: Use agents_config.json for configuration.
"""


class Port:
    """Default port assignments.

    DEPRECATED: Use agents_config.json for port configuration.
    """

    LEAGUE_MANAGER = 8000
    REFEREE_01 = 8001
    REFEREE_02 = 8002
    PLAYER_01 = 8101
    PLAYER_02 = 8102
    PLAYER_03 = 8103
    PLAYER_04 = 8104


class Endpoint:
    """Default endpoint URLs.

    DEPRECATED: Use agents_config.json for endpoint configuration.
    """

    LEAGUE_MANAGER = "http://localhost:8000/mcp"
    REFEREE_01 = "http://localhost:8001/mcp"
    REFEREE_02 = "http://localhost:8002/mcp"
    PLAYER_01 = "http://localhost:8101/mcp"
    PLAYER_02 = "http://localhost:8102/mcp"
    PLAYER_03 = "http://localhost:8103/mcp"
    PLAYER_04 = "http://localhost:8104/mcp"
