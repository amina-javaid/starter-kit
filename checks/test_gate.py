"""Gate parity vectors. site/scripts/gate-parity.mjs checks the same values.

    python checks/test_gate.py
"""

import sys

from _gate import code_for

VECTORS = [
    ("l01", "octocat", "L01-P7FU-GO2U"),
    ("l03", "@OctoCat ", "L03-3CDD-PMXG"),
    ("l04", "amina-traversaal", "L04-HX5H-ESQD"),
]


def main() -> int:
    bad = 0
    for level, handle, want in VECTORS:
        got = code_for(level, handle)
        mark = "ok  " if got == want else "FAIL"
        bad += got != want
        print(f"{mark} {level} {handle!r:22} {got}  (want {want})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
