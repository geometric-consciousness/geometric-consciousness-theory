#!/usr/bin/env python3
"""Focused deterministic fixtures for the codebase-structure inventory."""

from __future__ import annotations

import random
import subprocess
import tempfile
from pathlib import Path

import manage_codebase_structure as manager


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expect_inventory_error(label: str, function) -> None:
    try:
        function()
    except manager.InventoryError:
        return
    raise AssertionError(f"{label}: expected InventoryError")


def main() -> int:
    authority = [
        ".github/workflows/audit.yml",
        "CODEBASE_STRUCTURE.md",
        "GCT_Physics_Engine/data/result2.json",
        "GCT_Physics_Engine/data/result10.json",
        "build_scripts/manage_codebase_structure.py",
        "content/Figures/Volume 2/Figura áurea 2.svg",
        "content/Figures/Volume 2/Figura áurea 10.svg",
        "output/reference result.json",
    ]
    rendered = manager.render_tree(authority)
    require(
        manager.parse_rendered_paths(rendered) == manager.normalize_inventory(authority),
        "render/parser exact path-set round trip failed",
    )

    shuffled = list(authority)
    random.Random(144).shuffle(shuffled)
    require(manager.render_tree(shuffled) == rendered, "shuffled input changed deterministic output")
    require(rendered.index("result2.json") < rendered.index("result10.json"), "natural file order failed")
    require(rendered.index("áurea 2.svg") < rendered.index("áurea 10.svg"), "Unicode natural order failed")

    added = authority + ["new untracked Δ/result3.json"]
    missing, extra = manager.compare_path_sets(rendered, added)
    require(
        missing == ["new untracked Δ/result3.json"] and not extra,
        "tracked/untracked addition was not detected",
    )

    deleted = authority[:-1]
    missing, extra = manager.compare_path_sets(rendered, deleted)
    require(
        not missing and extra == ["output/reference result.json"],
        "deleted/stale path was not detected",
    )

    without_engine = [path for path in authority if not path.startswith("GCT_Physics_Engine/")]
    missing, extra = manager.compare_path_sets(manager.render_tree(without_engine), authority)
    require(
        missing == [
            "GCT_Physics_Engine/data/result2.json",
            "GCT_Physics_Engine/data/result10.json",
        ] and not extra,
        "whole top-level omission was not detected",
    )

    audit_probe = manager.normalize_inventory([
        "_audit_workspace/private/report.md",
        "nested/_audit_workspace/public.md",
        "README.md",
    ])
    require(
        audit_probe == ["nested/_audit_workspace/public.md", "README.md"],
        "audit exclusion was broader than root _audit_workspace/**",
    )

    expect_inventory_error("duplicate path", lambda: manager.normalize_inventory(["a.txt", "a.txt"]))
    expect_inventory_error("parent traversal", lambda: manager.normalize_inventory(["../a.txt"]))
    expect_inventory_error("Windows separator", lambda: manager.normalize_inventory([r"content\a.md"]))

    require(
        manager.GIT_LS_FILES_ARGS == (
            "git", "ls-files", "--cached", "--others", "--exclude-standard", "-z",
        ),
        "Git inventory command drifted",
    )

    # Exercise the real Git authority: cached, non-ignored untracked, ignored,
    # explicitly tracked audit material, Unicode/spaces, and an unstaged delete.
    with tempfile.TemporaryDirectory() as directory:
        probe = Path(directory)
        subprocess.run(("git", "init", "-q"), cwd=probe, check=True)
        (probe / ".gitignore").write_text("ignored.tmp\n", encoding="utf-8")
        (probe / "tracked.txt").write_text("tracked\n", encoding="utf-8")
        (probe / "untracked Δ file.txt").write_text("untracked\n", encoding="utf-8")
        (probe / "ignored.tmp").write_text("ignored\n", encoding="utf-8")
        audit = probe / "_audit_workspace" / "private.md"
        audit.parent.mkdir()
        audit.write_text("private\n", encoding="utf-8")
        subprocess.run(("git", "add", ".gitignore", "tracked.txt"), cwd=probe, check=True)
        subprocess.run(("git", "add", "-f", "_audit_workspace/private.md"), cwd=probe, check=True)
        require(
            manager.git_inventory(probe) == [
                ".gitignore", "tracked.txt", "untracked Δ file.txt",
            ],
            "real Git tracked/untracked/ignored/audit inventory semantics failed",
        )
        (probe / "tracked.txt").unlink()
        expect_inventory_error("unstaged tracked deletion", lambda: manager.git_inventory(probe))

    print("PASS CODEBASE_STRUCTURE fixtures: exact sets, natural order, Unicode, exclusions, stale paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
