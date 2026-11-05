---
name: preflight
description: L01 environment check. Verifies Git, Python, Node, Docker, Claude Code, the OpenRouter key and the GitHub remote, explains any failures, and prints the L01 unlock code when everything passes. Use when the student types /preflight or asks if their setup is ready.
---

# /preflight: is this machine ready?

1. Run `python checks/preflight.py` (use `python3` if `python` isn't found or opens the Microsoft Store).

2. If there are `[FAIL]` lines, go through them **one at a time**, starting with the first:
   - Explain in one plain sentence what's missing and why the bootcamp needs it.
   - Give the exact fix for *their* OS (check the platform; Windows and macOS fixes differ). Installs that need a download or admin rights must be done by the student. Walk them through it; don't attempt GUI installs.
   - After installing anything, remind them to **fully restart VS Code** so the terminal picks up the new PATH.
   - Re-run the check after each fix.

3. Never open, print or `cat` the `.env` file. If the key is the problem, tell them to open `.env` themselves and check it's one line: `OPENROUTER_API_KEY=sk-or-...` with no quotes or spaces.

4. `[WARN]` lines don't block. Mention them briefly (Docker is needed from L06).

5. When the script prints `PASSED`, show the unlock code exactly as printed, and remind them of the second half of L01: fill in `ME.md`, then `git add ME.md`, `git commit -m "Introduce myself"`, `git push`, and paste the commit URL on the site's L01 Check tab.
