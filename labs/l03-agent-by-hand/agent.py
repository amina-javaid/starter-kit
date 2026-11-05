"""L03 · An agent by hand: Context, Tools, Loop.

A support agent for Parcelly, a fictional delivery company. It answers order
questions by calling a lookup_order tool in a loop. No frameworks.

    python labs/l03-agent-by-hand/agent.py "Where is order 4721 and can I still change the address?"

Provided: the model call, the tool function, tracing.
Your job: the three TODOs that turn a chatbot into an agent.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
TRACE = ROOT / ".fde" / "traces" / "l03.jsonl"
MAX_STEPS = 6

SYSTEM = (
    "You are the support agent for Parcelly, a delivery company. "
    "Use your tools to look up order data. Never guess order details. "
    "If an order can't be found, say so. Be brief and friendly."
)

# ── C · Context ────────────────────────────────────────────────────────────
# Everything the model sees is in `messages` (built in run_agent) plus TOOLS.

# ── T · Tools ──────────────────────────────────────────────────────────────

def lookup_order(order_id: str) -> dict:
    orders = json.loads((HERE / "orders.json").read_text(encoding="utf-8"))
    return orders.get(str(order_id).lstrip("#"), {"error": f"No order with id {order_id}"})


TOOL_FUNCTIONS = {"lookup_order": lookup_order}

# TODO 1 (Tools): describe lookup_order so the model knows it exists.
# OpenRouter uses the OpenAI tool format:
#   {"type": "function",
#    "function": {"name": ..., "description": ...,
#                 "parameters": {"type": "object",
#                                "properties": {<arg name>: {"type": "string", "description": ...}},
#                                "required": [<arg name>]}}}
# The description matters: it's the only thing the model reads to decide when to use the tool.
TOOLS = []


# ── Provided plumbing: model call, tool runner, trace ─────────────────────

def load_env() -> dict:
    env = {}
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                key, val = line.split("=", 1)
                env[key.strip()] = val.strip().strip('"').strip("'")
    return env


ENV = load_env()
MODEL = ENV.get("AGENT_MODEL") or ENV.get("MODEL_A", "")


def trace(event: dict) -> None:
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    with TRACE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def call_model(messages: list) -> dict:
    """One trip to the model. Returns the assistant message (may contain tool_calls)."""
    trace({"type": "model_request", "messages": len(messages), "tool_messages": sum(m["role"] == "tool" for m in messages)})
    payload = {"model": MODEL, "messages": messages, "temperature": 0}
    if TOOLS:
        payload["tools"] = TOOLS
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {ENV.get('OPENROUTER_API_KEY', '')}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            msg = json.load(resp)["choices"][0]["message"]
    except urllib.error.HTTPError as e:
        sys.exit(f"OpenRouter returned HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")

    calls = msg.get("tool_calls") or []
    trace({"type": "model_response", "content": msg.get("content"), "tool_calls": [c["function"]["name"] for c in calls]})
    if calls:
        for c in calls:
            print(f"PLAN     model wants {c['function']['name']}({c['function']['arguments']})")
    return {k: v for k, v in msg.items() if k in ("role", "content", "tool_calls")}


def run_tool(name: str, args: dict) -> str:
    """Execute a tool the model asked for. Returns the result as a JSON string."""
    fn = TOOL_FUNCTIONS.get(name)
    result = fn(**args) if fn else {"error": f"Unknown tool {name}"}
    print(f"ACT      ran {name}({args})")
    print(f"OBSERVE  {result}")
    trace({"type": "tool_run", "name": name, "args": args, "result": result})
    return json.dumps(result)


# ── L · Loop ───────────────────────────────────────────────────────────────

def handle_tool_call(call: dict, messages: list) -> None:
    """Act + Observe for one tool call from the model."""
    name = call["function"]["name"]
    args = json.loads(call["function"]["arguments"] or "{}")

    # TODO 2 (Act + Observe):
    #   1. run the tool:  result = run_tool(name, args)
    #   2. append the result to `messages` so the model sees it next turn:
    #      {"role": "tool", "tool_call_id": call["id"], "content": result}
    raise NotImplementedError("TODO 2: run the tool and append its result to messages")


def run_agent(question: str) -> str:
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    TRACE.write_text("", encoding="utf-8")  # fresh trace per run
    trace({"type": "run_start", "model": MODEL, "question": question})

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]

    # TODO 3 (Loop): repeat up to MAX_STEPS times:
    #   1. reply = call_model(messages), then append reply to messages
    #   2. if the reply has no "tool_calls": that's the answer. Return reply["content"]
    #   3. otherwise call handle_tool_call(call, messages) for each tool call, and loop again
    # If you run out of steps, return a polite "I couldn't finish" message.
    raise NotImplementedError("TODO 3: write the agent loop")


if __name__ == "__main__":
    if not MODEL:
        sys.exit("No MODEL_A in .env. Run /preflight first.")
    q = " ".join(sys.argv[1:]) or "Where is order 4721 and can I still change the address?"
    print(f"USER     {q}\n")
    answer = run_agent(q)
    print(f"\nANSWER   {answer}")
    trace({"type": "run_end", "answer": answer})
