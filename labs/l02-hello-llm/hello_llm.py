"""L02 · Your first LLM call.

Calls a model through OpenRouter with nothing but the Python standard library,
then prints the reply and how many tokens you paid for.

    python labs/l02-hello-llm/hello_llm.py                       # MODEL_A from .env
    python labs/l02-hello-llm/hello_llm.py --model B             # MODEL_B from .env
    python labs/l02-hello-llm/hello_llm.py -q "Your own question"

Three TODOs below. They are the lesson: write them yourself (the tutor will hint).
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")


def load_env() -> dict:
    env = {}
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                key, val = line.split("=", 1)
                env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def call_llm(api_key: str, payload: dict) -> dict:
    """POST the payload to OpenRouter's chat completions endpoint, return the JSON response."""
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"OpenRouter returned HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


def record_run(model: str, reply: str, input_tokens: int, output_tokens: int, seconds: float) -> None:
    """Saves the run to .fde/l02_runs.json so /check l02 can see it."""
    path = ROOT / ".fde" / "l02_runs.json"
    path.parent.mkdir(exist_ok=True)
    runs = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    runs.append({
        "model": model, "reply": reply[:200], "input_tokens": input_tokens,
        "output_tokens": output_tokens, "seconds": round(seconds, 2),
        "at": datetime.now(timezone.utc).isoformat(),
    })
    path.write_text(json.dumps(runs, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["A", "B"], default="A")
    parser.add_argument("-q", "--question", default="In two sentences: what is a token, and why should a product team care?")
    args = parser.parse_args()

    env = load_env()
    api_key = env.get("OPENROUTER_API_KEY") or sys.exit("No OPENROUTER_API_KEY in .env. Run /preflight first.")
    model = env.get(f"MODEL_{args.model}") or sys.exit(f"No MODEL_{args.model} in .env.")

    # TODO 1: build the conversation.
    # A list of two dicts, each with a "role" and "content":
    #   - a "system" message that sets the assistant's behaviour (keep it short)
    #   - a "user" message containing args.question
    messages = None

    if messages is None:
        sys.exit("TODO 1 isn't done yet: build the messages list.")

    payload = {"model": model, "messages": messages, "temperature": 0.2}
    started = time.time()
    data = call_llm(api_key, payload)
    seconds = time.time() - started

    # TODO 2: pull the reply text out of `data`.
    # Print `data` once if you're unsure what it looks like. The reply lives inside
    # the first item of data["choices"].
    reply = None

    # TODO 3: read the token usage.
    # `data` has a "usage" block. Set the two variables below from it.
    input_tokens = None
    output_tokens = None

    if reply is None or input_tokens is None or output_tokens is None:
        sys.exit("TODO 2 or TODO 3 isn't done yet. Tip: print(json.dumps(data, indent=2)) to see the response.")

    print(f"\nModel:   {model}")
    print(f"Time:    {seconds:.2f}s")
    print(f"Tokens:  {input_tokens} in / {output_tokens} out\n")
    print(reply)
    record_run(model, reply, input_tokens, output_tokens, seconds)


if __name__ == "__main__":
    main()
