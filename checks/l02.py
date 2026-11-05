"""L02 check: did hello_llm.py make successful calls with two different models?

hello_llm.py appends every successful run to .fde/l02_runs.json. It only records
a run once the reply and token usage were read, which is what the TODOs do.
"""

import sys

from _common import FDE, Report, read_json


def main() -> int:
    r = Report("L02 · How LLMs work")
    runs = [x for x in read_json(FDE / "l02_runs.json", []) if isinstance(x, dict)]
    good = [x for x in runs if x.get("reply") and x.get("output_tokens", 0) > 0 and x.get("input_tokens", 0) > 0]

    if not runs:
        r.fail("No runs recorded yet", "Finish the TODOs and run: python labs/l02-hello-llm/hello_llm.py")
        return r.finish("l02")

    r.ok(f"{len(good)} successful call(s) recorded, with token usage")
    models = sorted({x["model"] for x in good})
    if len(models) >= 2:
        r.ok(f"Two different models: {models[0]} and {models[1]}")
    elif models:
        r.fail(f"Only one model so far ({models[0]})", "Run again with --model B to try the second model from .env")
    else:
        r.fail("Runs are missing the reply or token usage", "Finish TODO 2 and TODO 3 in hello_llm.py")
    return r.finish("l02")


if __name__ == "__main__":
    sys.exit(main())
