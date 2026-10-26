"""Deterministic adversarial fixtures for the permanent-register validator."""
from __future__ import annotations

import sys
from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))
from check_permanent_registers import (  # noqa: E402
    O_ID, O_LIFECYCLES, P_ID, P_LIFECYCLES,
    open_problem_citations, prediction_citations,
    validate_append_only, validate_lifecycle, validate_sequence,
)


def expect_pass(label: str, errors: list[str]) -> None:
    if errors:
        raise AssertionError(f"{label} unexpectedly failed: {errors}")


def expect_fail(label: str, errors: list[str]) -> None:
    if not errors:
        raise AssertionError(f"{label} unexpectedly passed")


def expect_citations(label: str, text: str, expected: set[str]) -> None:
    actual = prediction_citations(text)
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")


def expect_unresolved(label: str, text: str, defined: set[str]) -> None:
    unresolved = prediction_citations(text) - defined
    if not unresolved:
        raise AssertionError(f"{label}: malformed or unknown token was masked")


def expect_open_citations(label: str, text: str, expected: set[str]) -> None:
    actual = open_problem_citations(text)
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")


def expect_open_unresolved(label: str, text: str, defined: set[str]) -> None:
    unresolved = open_problem_citations(text) - defined
    if not unresolved:
        raise AssertionError(f"{label}: malformed or unknown token was masked")


def main() -> int:
    expect_pass("numeric gap", validate_sequence(["P.1", "P.3"], P_ID, "fixture"))
    expect_pass("descriptive companion", validate_sequence(["P.3", "P.3-centroid-context", "P.4"], P_ID, "fixture"))
    expect_citations(
        "full descriptive citation exactly once",
        "see P.3-centroid-context",
        {"P.3-centroid-context"},
    )
    expect_citations("letter companion exactly", "see P.1b", {"P.1b"})
    expect_citations("ordinary prose compound", "a P.7-equivalent construction", {"P.7"})
    expect_citations(
        "prediction range shorthand",
        "rows P.7c-e",
        {"P.7c", "P.7d", "P.7e"},
    )
    defined = {"P.3", "P.3-centroid-context", "P.1b"}
    expect_unresolved("uppercase descriptive tail", "see P.3-Upper", defined)
    expect_unresolved("underscore tail", "see P.3_bad", defined)
    expect_unresolved("unknown letter suffix", "see P.3q", defined)
    expect_unresolved("unknown descriptive suffix", "see P.3-unknown", defined)
    expect_unresolved("incomplete hyphen", "see P.3-", defined)
    expect_unresolved("trailing junk", "see P.3-centroid-contextXYZ", defined)
    expect_open_citations("O letter companion exactly", "see O.13b", {"O.13b"})
    open_defined = {"O.13", "O.13b"}
    expect_open_unresolved("O uppercase suffix", "see O.13B", open_defined)
    expect_open_unresolved("O underscore tail", "see O.13_bad", open_defined)
    expect_open_unresolved("O incomplete hyphen", "see O.13-", open_defined)
    expect_open_unresolved("O unknown suffix", "see O.13z", open_defined)
    expect_open_unresolved("O trailing junk", "see O.13bJUNK", open_defined)
    expect_fail("duplicate", validate_sequence(["P.1", "P.1"], P_ID, "fixture"))
    expect_fail("descending", validate_sequence(["P.2", "P.1"], P_ID, "fixture"))
    expect_fail("schema", validate_sequence(["P.01"], P_ID, "fixture"))
    expect_fail("invalid lifecycle", validate_lifecycle("O.1", "DONE", None, O_LIFECYCLES, "fixture"))
    expect_fail("closed without version", validate_lifecycle("O.1", "CLOSED", None, O_LIFECYCLES, "fixture"))
    expect_fail("invalid closure version", validate_lifecycle("O.1", "CLOSED", "1.2", O_LIFECYCLES, "fixture"))
    expect_fail("open with closure version", validate_lifecycle("O.1", "OPEN", "v1.2.0", O_LIFECYCLES, "fixture"))
    expect_pass("valid closure version", validate_lifecycle("O.1", "CLOSED", "v1.2.0", O_LIFECYCLES, "fixture"))
    old = [{"id": "P.1", "lifecycle_status": "CLOSED", "closed_in": "v1.2.0"}]
    expect_pass("retained history", validate_append_only(old, old, "fixture"))
    expect_fail("deleted history", validate_append_only([], old, "fixture"))
    expect_fail("reopened history", validate_append_only([{"id": "P.1", "lifecycle_status": "ACTIVE", "closed_in": None}], old, "fixture"))
    expect_fail("changed closure version", validate_append_only([{"id": "P.1", "lifecycle_status": "CLOSED", "closed_in": "v1.3.0"}], old, "fixture"))
    expect_pass("active prediction", validate_lifecycle("P.1", "ACTIVE", None, P_LIFECYCLES, "fixture"))
    # An unresolved reference is the set difference used by the full validator.
    expect_fail("unresolved citation", ["P.99"] if {"P.99"} - {"P.1"} else [])
    expect_unresolved(
        "misspelled full descriptive citation",
        "see P.3-centroid-contex",
        {"P.3", "P.3-centroid-context"},
    )
    print("PASS permanent-register fixtures: exact full-token parsing + adversarial failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
