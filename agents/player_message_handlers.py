"""Message handlers for player agent HTTP endpoint.

This module provides the route handling logic for incoming messages.
"""

import asyncio
from typing import TYPE_CHECKING, Any, Dict

from fastapi import Request
from fastapi.responses import JSONResponse

from agents.player_handlers import handle_game_over, handle_invitation, handle_parity_call
from SHARED.constants import Field, LogEvent, MessageType, Status

if TYPE_CHECKING:
    from agents.generic_player import GenericPlayer


async def handle_mcp_message(player: "GenericPlayer", request: Request) -> JSONResponse:
    """Handle incoming MCP protocol messages.

    Args:
        player: The GenericPlayer instance
        request: FastAPI request object

    Returns:
        JSONResponse with the appropriate response
    """
    try:
        message = await request.json()
        player.logger.log_message(LogEvent.RECEIVED, message)
        msg_type = message.get(Field.MESSAGE_TYPE)

        response = _dispatch_message(player, message, msg_type)
        player.logger.log_message(LogEvent.SENT, response)
        return JSONResponse(content=response)

    except Exception as e:
        player.logger.log_error(LogEvent.REQUEST_ERROR, str(e))
        return JSONResponse(content={Field.STATUS: Status.ERROR}, status_code=500)


def _dispatch_message(
    player: "GenericPlayer", message: Dict[str, Any], msg_type: str
) -> Dict[str, Any]:
    """Dispatch message to appropriate handler."""
    if msg_type == MessageType.GAME_INVITATION:
        return handle_invitation(
            player.player_id, message, player.logger, message.get(Field.CONVERSATION_ID)
        )
    if msg_type == MessageType.CHOOSE_PARITY_CALL:
        return handle_parity_call(player.player_id, message, player.strategy, player.logger)
    if msg_type == MessageType.GAME_OVER:
        handle_game_over(message, player.logger)
        return {Field.STATUS: Status.ACKNOWLEDGED}
    if msg_type == MessageType.ROUND_ANNOUNCEMENT:
        player.logger.log_message(
            "ROUND_ANNOUNCEMENT_RECEIVED", {"round_id": message.get(Field.ROUND_ID)}
        )
        return {Field.STATUS: Status.ACKNOWLEDGED}
    if msg_type == MessageType.ROUND_COMPLETED:
        player.logger.log_message(
            "ROUND_COMPLETED_RECEIVED", {"round_id": message.get(Field.ROUND_ID)}
        )
        return {Field.STATUS: Status.ACKNOWLEDGED}
    if msg_type == MessageType.LEAGUE_STANDINGS_UPDATE:
        player.logger.log_message(
            "STANDINGS_UPDATE_RECEIVED", {"round_id": message.get(Field.ROUND_ID)}
        )
        return {Field.STATUS: Status.ACKNOWLEDGED}
    if msg_type == MessageType.LEAGUE_COMPLETED:
        player.logger.log_message(
            "LEAGUE_COMPLETED_RECEIVED", {"final_standings": message.get("final_standings", [])}
        )
        asyncio.create_task(player._shutdown_gracefully())
        return {Field.STATUS: Status.ACKNOWLEDGED}
    if msg_type == MessageType.SHUTDOWN_COMMAND:
        player.logger.log_message("SHUTDOWN_RECEIVED", {})
        asyncio.create_task(player._shutdown_gracefully())
        return {Field.STATUS: Status.ACKNOWLEDGED}

    return {Field.STATUS: Status.ERROR, "message": "Unknown message type"}
