"""L01 preflight: is this machine ready for the bootcamp?

    python checks/preflight.py            (Mac/Linux: python3 checks/preflight.py)
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request

from _common import ROOT, Report, handle, load_env, run


def version_tuple(text: str) -> tuple:
    m = re.search(r"(\d+)\.(\d+)", text)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def check_openrouter_key(r: Report, key: str):
    base = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    req = urllib.request.Request(f"{base}/key", headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            json.load(resp)
        r.ok("OpenRouter accepted your API key")
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            r.fail("OpenRouter rejected your API key", "Create a new key at openrouter.ai/keys and paste it into .env")
        else:
            r.warn(f"Couldn't verify the key with OpenRouter (HTTP {e.code})", "Not fatal. You'll find out in the L02 lab.")
    except (urllib.error.URLError, OSError) as e:
        r.warn(f"Couldn't reach OpenRouter to verify the key ({e})", "Check your internet connection or proxy. Not fatal.")


def main() -> int:
    r = Report("L01 preflight")

    # Git
    ok, out = run(["git", "--version"])
    if ok:
        r.ok(out)
        name_ok, name = run(["git", "config", "user.name"])
        mail_ok, mail = run(["git", "config", "user.email"])
        if name_ok and mail_ok and name and mail:
            r.ok(f"Git identity: {name} <{mail}>")
        else:
            r.fail("Git doesn't know who you are", 'git config --global user.name "Your Name" && git config --global user.email you@example.com')
    else:
        r.fail("Git not found", "Install from git-scm.com (Windows: Git for Windows), then restart VS Code")

    # Python
    if sys.version_info >= (3, 10):
        r.ok(f"Python {sys.version.split()[0]}")
    else:
        r.fail(f"Python {sys.version.split()[0]} is too old", "Install Python 3.10+ from python.org")

    # Node + npm
    ok, out = run(["node", "--version"])
    if ok and version_tuple(out) >= (20, 0):
        r.ok(f"Node {out}")
    elif ok:
        r.fail(f"Node {out} is too old", "Install the LTS version from nodejs.org")
    else:
        r.fail("Node not found", "Install the LTS version from nodejs.org, then restart VS Code")
    # npm is a .cmd shim on Windows, which subprocess can't run without the extension.
    ok, out = run(["npm.cmd" if os.name == "nt" else "npm", "--version"])
    if ok:
        r.ok(f"npm {out}")
    else:
        r.fail("npm not found", "It comes with Node. Reinstall Node from nodejs.org")

    # Docker (needed from L06, so a warning for now)
    ok, out = run(["docker", "--version"])
    if ok:
        r.ok(out)
    else:
        r.warn("Docker not found", "You need Docker Desktop from L06. Install it now from docker.com so it's ready")

    # Claude Code
    ok, out = run(["claude", "--version"])
    if ok:
        r.ok(f"Claude Code CLI {out}")
    elif os.environ.get("CLAUDECODE"):
        r.ok("Running inside Claude Code")
        r.warn("The claude command isn't on your PATH", "Fine for pre-work. Install the CLI too (see the Claude Code docs) so you can use it from any terminal")
    else:
        r.fail("Claude Code not found", "Install Claude Code (VS Code extension + CLI). See Book Ch 1 §1.2")

    # API key
    env = load_env()
    key = env.get("OPENROUTER_API_KEY", "")
    if not (ROOT / ".env").exists():
        r.fail(".env file missing", "Copy .env.example to .env and paste your OpenRouter key")
    elif not key or key.startswith("sk-or-...") or key == "your-key-here":
        r.fail("OPENROUTER_API_KEY is empty in .env", "Create a key at openrouter.ai/keys and paste it after OPENROUTER_API_KEY=")
    elif not key.startswith("sk-or-"):
        r.fail("OPENROUTER_API_KEY doesn't look like an OpenRouter key", "It should start with sk-or-")
    else:
        r.ok("OPENROUTER_API_KEY is set in .env")
        check_openrouter_key(r, key)

    ok, out = run(["git", "check-ignore", ".env"])
    if not ok:
        r.fail(".env is not git-ignored", "Restore .gitignore from the template. Never commit API keys")

    # GitHub remote
    ok, url = run(["git", "remote", "get-url", "origin"])
    h = handle()
    if not ok:
        r.fail("No GitHub remote", "Create your copy with 'Use this template' on GitHub and clone that, not the original")
    else:
        r.ok(f"Remote: {url}")
        if h and f"/{h}/" not in url.lower() and f":{h}/" not in url.lower():
            r.warn(f"The remote isn't under @{h}", "Fine if you used an org. Make sure you can push to it")

    if h:
        r.ok(f"GitHub handle: @{h}")
    else:
        r.fail("No GitHub handle set", "Run /start, or: python checks/profile.py set <your-github-handle>")

    return r.finish("l01")


if __name__ == "__main__":
    sys.exit(main())
