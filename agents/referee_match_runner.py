"""Match execution logic for referee."""
from agents.referee_match_state import MatchContext, MatchState, MatchStateMachine
from SHARED.constants import Field, LogEvent, MessageType, Timeout
from SHARED.contracts import (build_choose_parity_call, build_game_invitation,
                              build_game_over, build_match_result_report)
from SHARED.league_sdk.agent_comm import send, send_with_retry
from SHARED.league_sdk.config_loader import load_agent_config, load_system_config

_system_config = load_system_config()
_agents_config = load_agent_config()
_lm_endpoint = _agents_config["league_manager"]["endpoint"]


async def run_match_phases(referee, league_id: str, round_id: int, match_id: str,
                           player_a: str, player_b: str, player_a_endpoint: str, player_b_endpoint: str):
    """Orchestrate a complete match (called when LM sends RUN_MATCH)."""
    referee.logger.log_message(LogEvent.MATCH_START,
        {Field.MATCH_ID: match_id, Field.PLAYER_A: player_a, Field.PLAYER_B: player_b})
    state_machine = MatchStateMachine()
    context = MatchContext(match_id, player_a, player_b)
    referee.active_matches[match_id] = {"state_machine": state_machine, "context": context}
    # Phase 1: Invite players
    if not await invite_players(referee, context, league_id, round_id, match_id,
                                player_a, player_b, player_a_endpoint, player_b_endpoint):
        return
    state_machine.transition(MatchState.COLLECTING_CHOICES)
    # Phase 2: Collect choices
    if not await collect_choices(referee, context, league_id, round_id, match_id,
                                 player_a, player_b, player_a_endpoint, player_b_endpoint):
        return
    # Phase 3: Determine winner
    state_machine.transition(MatchState.DRAWING_NUMBER)
    drawn_number = referee.game_rules.draw_number()
    winner = referee.game_rules.determine_winner(context.player_a_choice, context.player_b_choice, drawn_number)
    referee.logger.log_message("WINNER_DETERMINED", {
        Field.MATCH_ID: match_id, Field.WINNER: winner, Field.DRAWN_NUMBER: drawn_number,
        Field.PLAYER_A_CHOICE: context.player_a_choice, Field.PLAYER_B_CHOICE: context.player_b_choice})
    # Phase 4: Notify players
    await notify_game_over(referee, league_id, round_id, match_id, winner, drawn_number,
                           context, player_a_endpoint, player_b_endpoint)
    # Phase 5: Report to LM
    await report_result(referee, league_id, round_id, match_id, player_a, player_b, winner)
    state_machine.transition(MatchState.FINISHED)
    referee.logger.log_message(LogEvent.MATCH_COMPLETE, {Field.MATCH_ID: match_id, Field.WINNER: winner})
    del referee.active_matches[match_id]


async def invite_players(referee, context, league_id, round_id, match_id,
                         player_a, player_b, ep_a, ep_b) -> bool:
    """Send invitations to players."""
    inv_a = build_game_invitation(league_id, round_id, match_id, referee.referee_id, player_a, player_b)
    inv_b = build_game_invitation(league_id, round_id, match_id, referee.referee_id, player_b, player_a)
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


async def collect_choices(referee, context, league_id, round_id, match_id,
                          player_a, player_b, ep_a, ep_b) -> bool:
    """Collect parity choices from players."""
    req_a = build_choose_parity_call(league_id, round_id, match_id, referee.referee_id, player_a)
    req_b = build_choose_parity_call(league_id, round_id, match_id, referee.referee_id, player_b)
    resp_a = await send(ep_a, req_a)
    resp_b = await send(ep_b, req_b)
    if resp_a and Field.CHOICE in resp_a:
        context.record_choice(player_a, resp_a[Field.CHOICE])
    if resp_b and Field.CHOICE in resp_b:
        context.record_choice(player_b, resp_b[Field.CHOICE])
    if not context.both_choices_received():
        referee.logger.log_error(LogEvent.TIMEOUT, "Choices not received")
        return False
    return True


async def notify_game_over(referee, league_id, round_id, match_id, winner,
                           drawn_number, context, ep_a, ep_b):
    """Send game over notifications to players."""
    msg = build_game_over(league_id, round_id, match_id, referee.referee_id, winner,
                          drawn_number, context.player_a_choice, context.player_b_choice)
    await send(ep_a, msg)
    await send(ep_b, msg)


async def report_result(referee, league_id, round_id, match_id, player_a, player_b, winner):
    """Report match result to League Manager with retry."""
    msg = build_match_result_report(league_id, round_id, match_id, referee.referee_id,
                                    player_a, player_b, winner)
    await send_with_retry(_lm_endpoint, msg,
        max_retries=_system_config.retry_policy["max_retries"],
        timeout=_system_config.timeouts[Timeout.HTTP_REQUEST],
        retry_delay=_system_config.retry_policy["retry_delay"])
