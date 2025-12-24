"""Player invitation logic for referee matches."""

from SHARED.constants import Field, LogEvent, MessageType
from SHARED.contracts import build_game_invitation
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params, is_jsonrpc_request
from SHARED.league_sdk.agent_comm import send


def _extract_message(resp: dict) -> dict:
    """Extract message content from JSON-RPC envelope if present."""
    if not resp:
        return {}
    if is_jsonrpc_request(resp):
        return extract_jsonrpc_params(resp)
    return resp


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
    # Extract params from JSON-RPC envelope if response is wrapped
    msg_a = _extract_message(resp_a)
    msg_b = _extract_message(resp_b)
    if msg_a.get(Field.MESSAGE_TYPE) == MessageType.GAME_JOIN_ACK:
        context.record_join(player_a, msg_a.get(Field.CONVERSATION_ID))
    if msg_b.get(Field.MESSAGE_TYPE) == MessageType.GAME_JOIN_ACK:
        context.record_join(player_b, msg_b.get(Field.CONVERSATION_ID))
    if not context.both_players_joined():
        referee.logger.log_error(LogEvent.TIMEOUT, "Players did not join")
        return False
    return True
