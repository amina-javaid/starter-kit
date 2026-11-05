---
name: start
description: Start or resume the FDE pre-work. Sets the student's GitHub handle, shows which levels have passed, and says exactly what to do next. Use when the student types /start or asks "where am I" / "what's next".
---

# /start: where am I, what's next

1. Run `python checks/profile.py show` (use `python3` if `python` isn't found).

2. **No handle yet** (`profile` is empty): welcome the student in two sentences: this repo is their tutor for the pre-work, and each level's check prints an unlock code for the site. Then ask for their **GitHub handle**, the same one they saved on the pre-work site. When they answer, run `python checks/profile.py set <handle>`.

3. **Tell them where they are**, using `passed` and `next` from the output:

   | next | Say |
   |---|---|
   | `l01` | Copy `.env.example` to `.env`, paste the OpenRouter key, then run `/preflight`. After that, fill in `ME.md`, commit and push, and paste the commit URL on the site. |
   | `l02` | Read L02 on the site, then open `labs/l02-hello-llm/hello_llm.py` and do the 3 TODOs. Check with `/check l02`. |
   | `l03` | Step through the loop in L03's Demo tab, then do the 3 TODOs in `labs/l03-agent-by-hand/agent.py`. Check with `/check l03`. |
   | `l04` | Fill in `labs/l04-first-app/SPEC.md`, then build the app with plan mode, committing as you go. Check with `/check l04`. |
   | `l05` or later | L05–L07 are coming soon. Meanwhile, read Book Ch 2, 4 and 5, and try the demos on the site. |

4. Keep it to one short message: a status line (e.g. "Passed: L01, L02"), then the next step as numbered actions. Offer `/explain <term>` for anything unfamiliar.
