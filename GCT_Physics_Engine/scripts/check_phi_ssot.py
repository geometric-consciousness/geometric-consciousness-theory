#!/usr/bin/env python3
"""
check_phi_ssot.py - CI guard for PHI single-source-of-truth.

Walks src/ and verify_independent/ and flags any PHI definition that
is not one of the canonical SSOT-compliant patterns:

    PHI = float(C.PHI)
    PHI = C.PHI
    PHI = MATH.PHI

Exit code: 0 if clean, 1 if violations found.

Permitted exceptions are listed in SSOT_EXEMPT below: these are
by-design standalone files that must not depend on the GCT engine SSOT
(epistemic-circularity guards or from-scratch reproducers).
"""

import re
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parent.parent

# Files exempted from the SSOT rule by intentional design isolation:
# standalone files that must not depend on the GCT engine SSOT
# (epistemic-circularity guards or from-scratch reproducers).
SSOT_EXEMPT = {
    "verify_independent/constants.py",   # epistemic-circularity guard for independent verification
    "reproduce_standard_model.py",        # Tier 0 from-scratch reproducer, no engine deps by design
}

# Capture any `PHI = <RHS>` line; check RHS against the SSOT allow-list.
PHI_DEF_PATTERN = re.compile(r"^\s*PHI\s*=\s*([^#\n]+?)(?:\s*#.*)?$")
SSOT_ALLOWED_RHS = {
    "float(C.PHI)",
    "C.PHI",
    "MATH.PHI",
    # The try/except SSOT-with-fallback pattern: files that do not import
    # gct_utils unconditionally use a try/except block that sets
    # _PHI_FROM_SSOT = float(C.PHI) when gct_utils is available, falling
    # back to the inline (1+sqrt(5))/2 numerical-identity expression
    # otherwise. The assignment `PHI = _PHI_FROM_SSOT` is canonical
    # because the upstream block sources C.PHI when the SSOT chain is
    # importable; the fallback branch is the IEEE-754-identical numerical
    # value used only when gct_utils itself cannot be imported (e.g., in
    # standalone test execution outside the engine harness).
    "_PHI_FROM_SSOT",
}


def main():
    violations = []
    for py_file in sorted(ENGINE_ROOT.rglob("*.py")):
        rel = py_file.relative_to(ENGINE_ROOT).as_posix()
        if rel.startswith("scripts/check_phi_ssot.py"):
            continue
        if rel.startswith("src/gct_utils.py"):
            # gct_utils.py IS the SSOT module; it defines PHI = C.PHI
            continue
        try:
            text = py_file.read_text(encoding="utf-8")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            m = PHI_DEF_PATTERN.match(line)
            if not m:
                continue
            rhs = m.group(1).strip()
            if rhs in SSOT_ALLOWED_RHS:
                continue
            if rel in SSOT_EXEMPT:
                continue
            violations.append((rel, lineno, line.strip()))

    if not violations:
        print("PHI SSOT: CLEAN. All PHI definitions use the canonical pattern.")
        return 0

    print(f"PHI SSOT: {len(violations)} VIOLATIONS")
    print()
    print("The following files redefine PHI inline outside the SSOT pattern:")
    print("  Canonical pattern: PHI = float(C.PHI)  (after `from gct_utils import C`)")
    print()
    for rel, lineno, src in violations:
        print(f"  {rel}:{lineno}: {src}")
    print()
    print("Migrate to the SSOT pattern, or if the file is by-design")
    print("standalone (epistemic-circularity guard, from-scratch reproducer),")
    print("add it to SSOT_EXEMPT at the top of this script.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
