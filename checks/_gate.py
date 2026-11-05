"""Unlock codes. Must stay byte-for-byte identical to site/lib/gate.ts.

code = "L03-" + base32(sha256("l03|<handle>|<SALT>"))[:8] split 4-4

This is friction, not security: the salt is public in both repos. Pre-work runs
on the honor system; the code just proves the check script ran on your machine.
"""

import base64
import hashlib

SALT = "fde-starter-v1"


def normalize_handle(handle: str) -> str:
    return handle.strip().lstrip("@").lower()


def code_for(level: str, handle: str) -> str:
    msg = f"{level.lower()}|{normalize_handle(handle)}|{SALT}"
    b = base64.b32encode(hashlib.sha256(msg.encode("utf-8")).digest()).decode("ascii")[:8]
    return f"{level.upper()}-{b[:4]}-{b[4:8]}"
