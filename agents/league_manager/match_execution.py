"""Match execution via referee for League Manager.

DEPRECATED: This module is no longer used.

Per CONTRACTS.md, there is no RUN_MATCH message. Referees self-start matches
when they receive ROUND_ANNOUNCEMENT and identify matches assigned to them
via the referee_endpoint field.

Match execution now works as follows:
1. LM sends ROUND_ANNOUNCEMENT to all agents
2. Referees filter matches by referee_endpoint, look up player endpoints
   from agents_config.json, and start matches autonomously
3. Referees send MATCH_RESULT_REPORT to LM when matches complete
4. LM responds with MATCH_RESULT_ACK

See: round_execution.py, referee_http_handlers.py
"""

# This file is kept for backwards compatibility but all functions are removed.
# If you need to migrate code that depended on execute_match_via_referee,
# the new flow is implemented in round_execution.py (LM side) and
# referee_http_handlers.handle_round_announcement (referee side).
