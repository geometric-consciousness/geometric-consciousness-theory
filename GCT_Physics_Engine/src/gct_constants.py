#!/usr/bin/env python3
"""Named SSOT constants facade for protocol imports.

Most protocols use ``gct_utils.C`` directly. A small number need explicit
module-level names so hardcoded ledger anchors are visible to static audits.
"""

from __future__ import annotations

from gct_utils import C


ALPHA2_INV_GUT_A2 = float(C.ALPHA2_INV_GUT_A2)


def validate() -> bool:
    return ALPHA2_INV_GUT_A2 > 0


if __name__ == "__main__":
    print(f"ALPHA2_INV_GUT_A2={ALPHA2_INV_GUT_A2:g}")
