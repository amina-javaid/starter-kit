"""L03 check: read the agent's latest trace and confirm one full loop happened.

The trace events are written by the parts of agent.py that are already provided
(call_model and run_tool), so the check only passes when the student's TODOs
actually wire them into a loop.
"""

import json
import sys

from _common import FDE, Report


def load_trace() -> list:
    path = FDE / "traces" / "l03.jsonl"
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    return events


def main() -> int:
    r = Report("L03 · LLM → Agent")
    events = load_trace()
    if not events:
        r.fail("No trace found", 'Run: python labs/l03-agent-by-hand/agent.py "Where is order 4721?"')
        return r.finish("l03")

    responses = [e for e in events if e.get("type") == "model_response"]
    requests = [e for e in events if e.get("type") == "model_request"]
    tools = [e for e in events if e.get("type") == "tool_run"]

    asked = [e for e in responses if e.get("tool_calls")]
    if asked:
        names = sorted({c for e in asked for c in e["tool_calls"]})
        r.ok(f"Plan: the model asked for a tool ({', '.join(names)})")
    else:
        r.fail("The model never asked for a tool", "TODO 1: describe lookup_order in TOOLS so the model knows it exists")

    if tools:
        r.ok(f"Act: your code ran {tools[0]['name']}({tools[0].get('args')})")
    else:
        r.fail("No tool was executed", "TODO 2: when the reply has tool_calls, run them with run_tool()")

    fed_back = [e for e in requests if e.get("tool_messages", 0) > 0]
    if fed_back:
        r.ok("Observe: the tool result was sent back to the model")
    else:
        r.fail("The tool result never went back to the model", "TODO 2: append the result to messages as a role='tool' message")

    final = responses[-1] if responses else {}
    if final and not final.get("tool_calls") and final.get("content"):
        r.ok(f"Loop: finished with an answer after {len(responses)} model call(s)")
    else:
        r.fail("The run didn't end with a plain answer", "TODO 3: loop until the model replies without tool_calls (or MAX_STEPS)")

    return r.finish("l03")


if __name__ == "__main__":
    sys.exit(main())
