# L03 · An agent by hand

A support agent for *Parcelly* that answers order questions by calling `lookup_order` in a loop.

The full walkthrough is in the **Lab** tab of L03 on the pre-work site, and the **Demo** tab steps through the exact loop you're building.

| TODO | CTL | What you write |
|---|---|---|
| 1 | **T**ools | The JSON description of `lookup_order` |
| 2 | Act + Observe | Run the tool, append the result as a `tool` message |
| 3 | **L**oop | Call the model until it answers without asking for a tool |

```bash
python labs/l03-agent-by-hand/agent.py "Where is order 4721 and can I still change the address?"
```

Every step is written to `.fde/traces/l03.jsonl`. Open it and read it: that's what debugging an agent looks like.

Stretch: ask about order 9999. Then add an `update_address` tool that asks the user to confirm before running it.

When it works: `/check l03`.
