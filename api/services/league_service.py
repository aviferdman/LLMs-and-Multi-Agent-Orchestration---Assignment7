"""League service for managing league operations."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from api.schemas.league import (
    AgentsStatusResponse,
    AgentStatus,
    LeagueConfigResponse,
    LeagueStatusResponse,
    StandingsResponse,
)
from api.schemas.matches import MatchListResponse, MatchResponse, MatchStatus
from api.services.league_helpers import (
    determine_status,
    get_current_round,
    list_matches,
    load_agents_config,
    load_league_config,
    load_standings,
    parse_standings_to_response,
)


class LeagueService:
    """Service for league-related operations."""

    def __init__(self, data_dir: Path = None, config_dir: Path = None):
        """Initialize league service."""
        self.data_dir = data_dir or Path("SHARED/data")
        self.config_dir = config_dir or Path("SHARED/config")

    def get_league_status(self, league_id: str) -> Optional[LeagueStatusResponse]:
        """Get current league status."""
        config = load_league_config(self.config_dir, league_id)
        if not config:
            return None

        standings = load_standings(self.data_dir, league_id)
        matches = list_matches(self.data_dir, league_id)

        completed = sum(1 for m in matches if m.get("status") == "completed")
        total = len(matches) if matches else config.get("total_rounds", 3) * 2

        return LeagueStatusResponse(
            league_id=league_id,
            status=determine_status(standings, completed, total),
            game_type=config.get("game_type", "even_odd"),
            current_round=get_current_round(standings),
            total_rounds=config.get("total_rounds", 3),
            matches_completed=completed,
            matches_total=total,
            players_registered=len(standings.get("standings", [])),
            referees_registered=2,
        )

    def get_standings(self, league_id: str) -> Optional[StandingsResponse]:
        """Get league standings."""
        standings = load_standings(self.data_dir, league_id)
        if not standings:
            return None

        player_standings = parse_standings_to_response(standings, league_id)

        return StandingsResponse(
            league_id=league_id,
            last_updated=datetime.fromisoformat(
                standings.get("last_updated", datetime.utcnow().isoformat()).replace("Z", "+00:00")
            ),
            standings=player_standings,
        )

    def get_league_config(self, league_id: str) -> Optional[LeagueConfigResponse]:
        """Get league configuration."""
        config = load_league_config(self.config_dir, league_id)
        if not config:
            return None

        return LeagueConfigResponse(
            league_id=league_id,
            game_type=config.get("game_type", "even_odd"),
            total_rounds=config.get("total_rounds", 3),
            matches_per_round=config.get("matches_per_round", 2),
            scoring=config.get("scoring", {"win": 3, "draw": 1, "loss": 0}),
        )

    def get_matches(self, league_id: str) -> MatchListResponse:
        """Get all matches for a league."""
        matches_data = list_matches(self.data_dir, league_id)
        matches = []

        for match in matches_data:
            matches.append(
                MatchResponse(
                    match_id=match.get("match_id", ""),
                    round_number=match.get("round_number", 0),
                    player1_id=match.get("player1_id", ""),
                    player2_id=match.get("player2_id", ""),
                    referee_id=match.get("referee_id"),
                    status=MatchStatus(match.get("status", "completed")),
                    winner_id=match.get("winner_id"),
                    player1_score=match.get("player1_score", 0),
                    player2_score=match.get("player2_score", 0),
                )
            )

        return MatchListResponse(matches=matches, total=len(matches))

    def get_agents_status(self) -> AgentsStatusResponse:
        """Get status of all registered agents."""
        config = load_agents_config(self.config_dir)
        if not config:
            return AgentsStatusResponse(
                players=[], referees=[], all_ready=False, message="No agents config"
            )

        players = [
            AgentStatus(
                agent_id=p.get("agent_id", ""),
                agent_type="player",
                is_registered=True,
                is_ready=True,
                endpoint=f"http://localhost:{p.get('port', 8000)}",
            )
            for p in config.get("players", [])
        ]

        referees = [
            AgentStatus(
                agent_id=r.get("agent_id", ""),
                agent_type="referee",
                is_registered=True,
                is_ready=True,
                endpoint=f"http://localhost:{r.get('port', 8000)}",
            )
            for r in config.get("referees", [])
        ]

        all_ready = len(players) >= 2 and len(referees) >= 1
        msg = "All agents ready" if all_ready else "Waiting for agents"

        return AgentsStatusResponse(
            players=players, referees=referees, all_ready=all_ready, message=msg
        )
