"""Player invitation logic for referee matches."""

from agents.referee_match_state import MatchContext
from SHARED.constants import Field, LogEvent, MessageType
from SHARED.contracts import build_game_invitation
from SHARED.league_sdk.agent_comm import send


async def invite_players(
    referee, context, league_id, round_id, match_id, player_a, player_b, ep_a, ep_b
) -> bool:
    """Send invitations to players."""
    inv_a = build_game_invitation(
        league_id=league_id,
        round_id=round_id,
        match_id=match_id,
        referee_id=referee.referee_id,
        player_id=player_a,
        opponent_id=player_b,
        role_in_match="player_a",
        game_type="even_odd",
    )
    inv_b = build_game_invitation(
        league_id=league_id,
        round_id=round_id,
        match_id=match_id,
        referee_id=referee.referee_id,
        player_id=player_b,
        opponent_id=player_a,
        role_in_match="player_b",
        game_type="even_odd",
    )
    resp_a = await send(ep_a, inv_a)
    resp_b = await send(ep_b, inv_b)
    if resp_a and resp_a.get(Field.MESSAGE_TYPE) == MessageType.GAME_JOIN_ACK:
        context.record_join(player_a, resp_a.get(Field.CONVERSATION_ID))
    if resp_b and resp_b.get(Field.MESSAGE_TYPE) == MessageType.GAME_JOIN_ACK:
        context.record_join(player_b, resp_b.get(Field.CONVERSATION_ID))
    if not context.both_players_joined():
        referee.logger.log_error(LogEvent.TIMEOUT, "Players did not join")
        return False
    return True
