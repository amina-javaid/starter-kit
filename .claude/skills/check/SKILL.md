---
name: check
description: Run a level's check (l02, l03, l04) and print its unlock code if it passes. Use when the student types /check <level> or asks whether their lab is done.
argument-hint: <level, e.g. l03>
---

# /check <level>

The level is: `$ARGUMENTS`

1. Normalise it to `l01`–`l07` (e.g. "3", "L03" and "lab 3" all mean `l03`). For `l01`, run the preflight instead (`/preflight`). If no level was given, run `python checks/profile.py show` and use `next`.

2. Run `python checks/<level>.py` (use `python3` if `python` isn't found). If the file doesn't exist, that level's check isn't open yet. Say so, and point them at its reading on the site.

3. **If it passes:** show the unlock code exactly as printed and say where to paste it. Add one sentence on what they just proved (e.g. for l03: "you wrote the loop Claude Code runs on").

4. **If it fails:** take the first `[FAIL]` and help with *that*:
   - For **l02 / l03**, the failures point at the student's TODOs. Follow the tutoring rule in CLAUDE.md: hints in escalating steps, never the code for the TODO itself. Open the relevant part of the file and ask them what they think should go there.
   - For **l04**, help directly: finishing the spec, committing, or getting the app to run. Leave the README's "How to run" / "How it works" sections for the student to write in their own words.

5. Never edit files under `checks/`, and never produce a code any other way than by running the check.
