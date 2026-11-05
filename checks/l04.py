"""L04 check: an app built with Claude Code, with a spec, run instructions and history."""

import sys

from _common import ROOT, Report, run

LAB = ROOT / "labs" / "l04-first-app"
CODE_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".mjs"}


def filled(path, min_chars: int) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "TODO" not in text and len(text.strip()) >= min_chars


def main() -> int:
    r = Report("L04 · Harness & Claude Code")

    if filled(LAB / "SPEC.md", 200):
        r.ok("SPEC.md is written")
    else:
        r.fail("SPEC.md still has TODOs or is very short", "Fill in labs/l04-first-app/SPEC.md before building")

    app = LAB / "app"
    code = [p for p in app.rglob("*") if p.suffix in CODE_EXT and "node_modules" not in p.parts] if app.exists() else []
    if code:
        r.ok(f"{len(code)} code file(s) in app/")
    else:
        r.fail("No code in labs/l04-first-app/app/", "Plan and build the app with Claude Code inside app/")

    if filled(LAB / "README.md", 300):
        r.ok("README explains how to run it and how it works")
    else:
        r.fail("README.md still has TODOs", "Fill in 'How to run' and 'How it works' in your own words")

    # Commits after the template's initial commit that touched this lab.
    ok, out = run(["git", "rev-list", "--count", "--min-parents=1", "HEAD", "--", "labs/l04-first-app"])
    commits = int(out) if ok and out.isdigit() else 0
    if commits >= 3:
        r.ok(f"{commits} commits on this lab")
    else:
        r.fail(f"{commits} commit(s) on this lab, need 3", "Commit after each working step: git add labs/l04-first-app && git commit -m '...'")

    ok, out = run(["git", "status", "--porcelain", "--", "labs/l04-first-app"])
    if ok and out:
        r.warn("You have uncommitted changes in the lab", "Commit them so your history matches what you built")

    return r.finish("l04")


if __name__ == "__main__":
    sys.exit(main())
