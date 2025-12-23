"""Analyze JSON-RPC compliance in agent logs."""
import json
import glob


def validate_jsonrpc(msg):
    """Validate JSON-RPC 2.0 compliance."""
    issues = []
    
    if "jsonrpc" not in msg:
        issues.append("Missing jsonrpc field")
        return issues
    
    if msg["jsonrpc"] != "2.0":
        issues.append(f"Invalid jsonrpc version: {msg['jsonrpc']}")
    
    if "id" not in msg:
        issues.append("Missing id field")
    
    has_method = "method" in msg
    has_result = "result" in msg
    has_error = "error" in msg
    
    if has_method:
        # It's a request - must have params
        if "params" not in msg:
            issues.append("Request missing params field")
    elif has_result:
        # Success response - OK
        pass
    elif has_error:
        # Error response
        error = msg.get("error", {})
        if "code" not in error or "message" not in error:
            issues.append("Error response missing code/message")
    else:
        issues.append("Neither request (method) nor response (result/error)")
    
    return issues


def main():
    log_files = glob.glob("SHARED/logs/agents/*.jsonl")
    all_messages = []
    issues_found = []
    
    for log_file in log_files:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    event_type = entry.get("event_type", "")
                    data = entry.get("data", {})
                    agent = entry.get("agent_id", "unknown")
                    
                    if event_type in ("SENT", "RECEIVED"):
                        if isinstance(data, dict) and "jsonrpc" in data:
                            issues = validate_jsonrpc(data)
                            if issues:
                                issues_found.append({
                                    "agent": agent,
                                    "event": event_type,
                                    "issues": issues,
                                    "msg": str(data)[:200]
                                })
                            msg_type = "request" if "method" in data else "response"
                            all_messages.append({
                                "agent": agent,
                                "event": event_type,
                                "type": msg_type,
                                "method": data.get("method", "N/A"),
                                "id": data.get("id"),
                            })
                        elif event_type == "SENT" and isinstance(data, dict) and "jsonrpc" not in data:
                            issues_found.append({
                                "agent": agent,
                                "event": event_type,
                                "issues": ["Plain response (not JSON-RPC wrapped)"],
                                "msg": str(data)[:200]
                            })
                except json.JSONDecodeError:
                    pass
    
    print("=" * 50)
    print("JSON-RPC 2.0 COMPLIANCE REPORT")
    print("=" * 50)
    print()
    
    if issues_found:
        print("⚠️  ISSUES FOUND:")
        print("-" * 40)
        for issue in issues_found:
            print(f"  Agent: {issue['agent']}, Event: {issue['event']}")
            print(f"  Issues: {issue['issues']}")
            print(f"  Message: {issue['msg']}...")
            print()
    else:
        print("✅ NO COMPLIANCE ISSUES FOUND")
        print()
    
    print(f"Total JSON-RPC messages analyzed: {len(all_messages)}")
    requests = [m for m in all_messages if m["type"] == "request"]
    responses = [m for m in all_messages if m["type"] == "response"]
    print(f"  Requests: {len(requests)}")
    print(f"  Responses: {len(responses)}")
    print()
    
    print("Request methods used:")
    methods = {}
    for m in requests:
        methods[m["method"]] = methods.get(m["method"], 0) + 1
    for method, count in sorted(methods.items()):
        print(f"  {method}: {count}")
    
    print()
    print("Message flow by agent:")
    for agent in sorted(set(m["agent"] for m in all_messages)):
        agent_msgs = [m for m in all_messages if m["agent"] == agent]
        sent = len([m for m in agent_msgs if m["event"] == "SENT"])
        recv = len([m for m in agent_msgs if m["event"] == "RECEIVED"])
        print(f"  {agent}: SENT={sent}, RECEIVED={recv}")


if __name__ == "__main__":
    main()
