#!/usr/bin/env python3
"""In-memory negative and idempotence fixtures for publication metadata."""

from __future__ import annotations

import copy

import manage_publication_metadata as manager


def expect_value_error(label, function):
    try:
        function()
    except ValueError:
        return
    raise AssertionError(f"{label}: expected ValueError")


def main() -> int:
    metadata = manager.load_json(manager.METADATA_PATH)
    expected = manager.load_json(manager.EXPECTED_PATH)
    de_result = manager.load_json(manager.DE_PATH)
    publication = metadata["publication_summary"]
    handles = publication["calibrated_discrete_coefficient_handles"]
    handle_notes = publication["calibrated_discrete_coefficient_handle_notes"]
    handle_scope = publication["calibrated_discrete_coefficient_subset_scope"]
    derived = manager.derive_publication_summary(expected, de_result, handles, handle_notes, handle_scope)
    manager.validate_metadata(metadata, derived)
    assert derived["calibrated_discrete_coefficient_handle_count"] == len(handles) == 6

    malformed = copy.deepcopy(metadata)
    malformed.pop("publication_summary")
    expect_value_error("missing publication summary", lambda: manager.validate_metadata(malformed, derived))

    bad_identity = copy.deepcopy(metadata)
    bad_identity["version"] = "release-candidate"
    expect_value_error("malformed version", lambda: manager.validate_metadata(bad_identity, derived))

    closure_drift = copy.deepcopy(expected)
    closure_drift["protocols"][0]["scientific_closure"] = "open"
    expect_value_error(
        "producer/metadata count drift",
        lambda: manager.validate_metadata(
            metadata, manager.derive_publication_summary(closure_drift, de_result, handles, handle_notes, handle_scope)
        ),
    )

    bad_de = copy.deepcopy(de_result)
    del bad_de["best_fit"]["joint_marginal_distance_diagnostic"]
    expect_value_error(
        "malformed dark-energy result",
        lambda: manager.derive_publication_summary(expected, bad_de, handles, handle_notes, handle_scope),
    )
    expect_value_error(
        "duplicate handle authority",
        lambda: manager.derive_publication_summary(
            expected, de_result, handles + [handles[0]], handle_notes, handle_scope
        ),
    )
    incomplete_notes = dict(handle_notes)
    incomplete_notes.pop(handles[-1])
    expect_value_error(
        "incomplete handle-note authority",
        lambda: manager.derive_publication_summary(expected, de_result, handles, incomplete_notes, handle_scope),
    )

    readme = manager.README_PATH.read_text(encoding="utf-8")
    rendered = manager.render_readme(readme, derived)
    assert manager.render_readme(rendered, derived) == rendered
    stale_readme = readme.replace("7 confirmed", "6 confirmed", 1)
    assert manager.render_readme(stale_readme, derived) == rendered
    stale_readme_protocol = rendered.replace("62/62 expected results", "61/62 expected results", 1)
    assert manager.render_readme(stale_readme_protocol, derived) == rendered
    stale_readme_handle_count = rendered.replace(
        manager.handle_statement(derived), manager.handle_statement(derived).replace("6 calibrated", "5 calibrated"), 1
    )
    assert manager.render_readme(stale_readme_handle_count, derived) == rendered
    stale_readme_handle_list = rendered.replace(
        manager.handle_statement(derived),
        manager.handle_statement(derived).replace("(1440, 12, 360, 2, 10phi^2, and 1/5)", "(1440 and 12)"),
        1,
    )
    assert manager.render_readme(stale_readme_handle_list, derived) == rendered
    canonical_inventory = manager.readme_handle_inventory(derived)
    for line in canonical_inventory.splitlines():
        if line.startswith("- "):
            mutated = rendered.replace(line, line + " [STALE]", 1)
            assert mutated != rendered
            assert manager.render_readme(mutated, derived) == rendered
    redundant_opening = (
        " A named precision/gauge comparison subset contains six calibrated Tier-3 discrete coefficient handles, "
        "counted separately from the six continuous anchors: stale duplicate values remain separately catalogued."
    )
    assert manager.render_readme(redundant_opening + rendered, derived) == rendered
    redundant_repeat = (
        " The named precision/gauge comparison subset's six calibrated Tier-3 discrete coefficient handles "
        "contain stale duplicate values; additional sector-specific handles are separately catalogued."
    )
    assert manager.render_readme(redundant_repeat + rendered, derived) == rendered

    citation = manager.CITATION_PATH.read_text(encoding="utf-8")
    rendered_citation = manager.render_citation(citation, derived, metadata)
    assert manager.render_citation(rendered_citation, derived, metadata) == rendered_citation
    assert "phantom crossing" not in rendered_citation.lower()
    stale_citation_protocol = rendered_citation.replace("62/62 expected results", "61/62 expected results", 1)
    assert manager.render_citation(stale_citation_protocol, derived, metadata) == rendered_citation
    stale_citation_handle_count = rendered_citation.replace(
        manager.handle_statement(derived), manager.handle_statement(derived).replace("6 calibrated", "5 calibrated"), 1
    )
    assert manager.render_citation(stale_citation_handle_count, derived, metadata) == rendered_citation
    stale_citation_handle_list = rendered_citation.replace(
        manager.handle_statement(derived),
        manager.handle_statement(derived).replace("(1440, 12, 360, 2, 10phi^2, and 1/5)", "(1440 and 12)"),
        1,
    )
    assert manager.render_citation(stale_citation_handle_list, derived, metadata) == rendered_citation

    zenodo = manager.load_json(manager.ZENODO_PATH)
    rendered_zenodo = manager.render_zenodo(zenodo, derived, metadata)
    assert manager.render_zenodo(rendered_zenodo, derived, metadata) == rendered_zenodo
    assert "phantom crossing" not in [item.lower() for item in rendered_zenodo["keywords"]]
    stale_zenodo_protocol = copy.deepcopy(rendered_zenodo)
    stale_zenodo_protocol["description"] = stale_zenodo_protocol["description"].replace(
        "62/62 expected results", "61/62 expected results", 1
    )
    assert manager.render_zenodo(stale_zenodo_protocol, derived, metadata) == rendered_zenodo
    stale_zenodo_handle_count = copy.deepcopy(rendered_zenodo)
    stale_zenodo_handle_count["description"] = stale_zenodo_handle_count["description"].replace(
        manager.handle_statement(derived), manager.handle_statement(derived).replace("6 calibrated", "5 calibrated"), 1
    )
    assert manager.render_zenodo(stale_zenodo_handle_count, derived, metadata) == rendered_zenodo
    stale_zenodo_handle_list = copy.deepcopy(rendered_zenodo)
    stale_zenodo_handle_list["description"] = stale_zenodo_handle_list["description"].replace(
        manager.handle_statement(derived),
        manager.handle_statement(derived).replace("(1440, 12, 360, 2, 10phi^2, and 1/5)", "(1440 and 12)"),
        1,
    )
    assert manager.render_zenodo(stale_zenodo_handle_list, derived, metadata) == rendered_zenodo

    print("PASS: publication metadata malformed/drift/idempotence fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
