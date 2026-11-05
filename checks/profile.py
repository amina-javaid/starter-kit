"""Set or show the GitHub handle that unlock codes are tied to.

    python checks/profile.py set <github-handle>
    python checks/profile.py show
"""

import json
import sys

from _common import PROFILE, PROGRESS, SITE_URL, read_json, write_json
from _gate import normalize_handle

LEVELS = ["l01", "l02", "l03", "l04", "l05", "l06", "l07"]


def main(argv):
    if len(argv) >= 3 and argv[1] == "set":
        h = normalize_handle(argv[2])
        if not h:
            print("Give a GitHub handle, e.g. python checks/profile.py set octocat")
            return 1
        write_json(PROFILE, {"github_handle": h})
        print(f"Saved GitHub handle @{h}. Use the same handle on {SITE_URL}.")
        return 0

    profile = read_json(PROFILE, {})
    progress = read_json(PROGRESS, {})
    print(json.dumps({"profile": profile, "passed": sorted(progress), "next": next((l for l in LEVELS if l not in progress), None)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
