# GCT Physics Engine — regeneration & verification recipes.
#
# Canonical entry points for rebuilding the committed data/*.json artefacts
# from their source protocols in src/.

PYTHON ?= py -3.13
ALLOW_FAIL_PROTOCOLS ?=
REFRESH_EXTRA_SCRIPTS := \
	gct_tau_uniqueness.py \
	gct_mckay_e8.py \
	o14d_advanced_invariants.py \
	o14d_closure_search.py \
	o14d_irrep_decomp.py \
	refresh_compat_json_artifacts.py

.PHONY: refresh-data refresh-all-data parity-check expected-outcome-check json-producer-check status-contract-check registry-id-check registry-appendix-check permanent-register-check permanent-register-fixtures phi-ssot-check verify clean help

help:
	@echo "GCT Physics Engine — Makefile targets"
	@echo "  refresh-data       Run verify_engine.py — regenerates the in-suite"
	@echo "                     subset (~60 protocols listed in verify_engine.py"
	@echo "                     PROTOCOLS) as a side effect of cross-claim"
	@echo "                     consistency assertion (non-zero exit on enforced-"
	@echo "                     claim failure or expected-verdict drift)."
	@echo "  refresh-all-data   Run every src/protocol_*.py once plus standalone"
	@echo "                     JSON producers listed in REFRESH_EXTRA_SCRIPTS,"
	@echo "                     then run verify_independent/run_all.py so every"
	@echo "                     committed data/*.json and results/*.json artifact"
	@echo "                     has a refresh path. Any protocol failure stops the"
	@echo "                     target unless the script name is listed in"
	@echo "                     ALLOW_FAIL_PROTOCOLS."
	@echo "  parity-check       Run refresh-all-data, then fail if regenerated JSON"
	@echo "                     differs from committed data/results artefacts."
	@echo "  expected-outcome-check"
	@echo "                     Fail if a result differs from the preregistered"
	@echo "                     outcome manifest."
	@echo "  json-producer-check"
	@echo "                     Fail if any committed data/*.json or outputs/*.json lacks a source"
	@echo "                     producer reachable from refresh-all-data."
	@echo "  status-contract-check"
	@echo "                     Force every verifier-status decision branch and"
	@echo "                     reject status/band contradictions."
	@echo "  registry-id-check Fail if claim/falsifiability registry IDs are not"
	@echo "                     present and unique."
	@echo "  registry-appendix-check"
	@echo "                     Fail if any App_FSM matrix row's tier/band/lifecycle cell"
	@echo "                     disagrees with the falsifiability registry (SSOT)."
	@echo "  permanent-register-check REGISTER_BASELINE_REF=<local-ref>"
	@echo "                     Validate lifecycle mirrors and append-only retention"
	@echo "                     against an explicit local Git baseline."
	@echo "  permanent-register-fixtures"
	@echo "                     Exercise permanent-register adversarial fixtures."
	@echo "  phi-ssot-check     Fail if any PHI definition forks from the C.PHI SSOT."
	@echo "  verify             Synonym for refresh-data."
	@echo "  clean              Remove src/ __pycache__ artefacts (preserves data/)."

# In-suite regeneration: verify_engine.py iterates its PROTOCOLS list (the
# subset under cross-claim consistency assertion) and each protocol writes its
# own *_results.json into data/. Exit non-zero on enforced-claim failure or on
# protocol-verdict drift from the EXPECTED_NON_PASS registry.
refresh-data: verify

verify:
	cd src && $(PYTHON) verify_engine.py

expected-outcome-check:
	$(PYTHON) src/check_expected_outcomes.py

# Full-boundary regeneration: every src/protocol_*.py is run once, regardless
# of whether it appears in verify_engine.py's PROTOCOLS list. Then the
# standalone JSON producers in REFRESH_EXTRA_SCRIPTS are run to cover shipped
# data/*.json artefacts whose source files intentionally do not use the
# protocol_ prefix. Individual protocol failures abort the loop unless the
# script name appears in ALLOW_FAIL_PROTOCOLS.
refresh-all-data:
	@cd src && for f in protocol_*.py; do \
		echo ">>> $$f"; \
		case " $(ALLOW_FAIL_PROTOCOLS) " in \
			*" $$f "*) $(PYTHON) "$$f" || echo "   (allowed non-zero exit from $$f)";; \
			*) $(PYTHON) "$$f";; \
		esac; \
	done
	@cd src && for f in $(REFRESH_EXTRA_SCRIPTS); do \
		echo ">>> $$f"; \
		case " $(ALLOW_FAIL_PROTOCOLS) " in \
			*" $$f "*) $(PYTHON) "$$f" || echo "   (allowed non-zero exit from $$f)";; \
			*) $(PYTHON) "$$f";; \
		esac; \
	done
	@echo ">>> verify_independent/run_all.py"
	@$(PYTHON) verify_independent/run_all.py
	# NOTE: build_falsifiability_matrix.py and build_app_r.py are SEED/UPDATE tools
	# for App_FM / App_R, not part of the byte-parity refresh. Those manuscript
	# scorecards are generator-seeded then curated; the curation is wider than
	# prose (LaTeX rendering, scorecard-sourced observed columns, and tier-disposition
	# rows sourced outside the registry — see README "Reproducibility scope" for the
	# three divergence classes). They are NOT regenerated here: regeneration replaces
	# the curated content. Run them manually + re-curate
	# when registry rows change:
	#   $(PYTHON) build_falsifiability_matrix.py   # seeds App_FM rows
	#   $(PYTHON) build_app_r.py                   # seeds App_R rows
	@echo ">>> check_data_json_producers.py --strict"
	@cd src && $(PYTHON) check_data_json_producers.py --strict
	@echo ">>> check_verifier_status_contract.py"
	@$(PYTHON) verify_independent/check_verifier_status_contract.py
	@echo ">>> check_registry_ids.py --strict"
	@cd src && $(PYTHON) check_registry_ids.py --strict
	@echo ">>> check_registry_appendix_consistency.py --strict"
	@cd src && $(PYTHON) check_registry_appendix_consistency.py --strict
	@echo ">>> scripts/check_phi_ssot.py"
	@$(PYTHON) scripts/check_phi_ssot.py
	@echo ""
	@echo "refresh-all-data complete. Run 'make verify' to re-assert cross-claim consistency."

json-producer-check:
	cd src && $(PYTHON) check_data_json_producers.py --strict

status-contract-check:
	$(PYTHON) verify_independent/check_verifier_status_contract.py

registry-id-check:
	cd src && $(PYTHON) check_registry_ids.py --strict

# registry-appendix-check: SSOT field-consistency gate. App_FSM is generator-seeded
# from falsifiability_registry.json then editorially enriched with curated prose the
# bare generator cannot reproduce (figure embeds, scope-disclosure paragraphs,
# engine-verification detail), so byte-equality is NOT the contract. The contract is
# FIELD agreement: every App_FSM matrix row's tier, falsification-band, and lifecycle cells must match
# the registry (the SSOT). This catches the hand-edit drift class (tier flips,
# gate-value drift) that byte-parity-exclusion left unguarded.
registry-appendix-check:
	cd src && $(PYTHON) check_registry_appendix_consistency.py --strict

# The baseline is deliberately explicit. The gate never guesses a remote or
# silently treats the current tree as its own append-only history.
permanent-register-check:
	cd src && $(PYTHON) check_permanent_registers.py --strict --baseline-ref "$(REGISTER_BASELINE_REF)"

permanent-register-fixtures:
	$(PYTHON) verify_independent/self_consistency/check_permanent_registers_fixtures.py

# phi-ssot-check: single-source-of-truth gate for the golden ratio PHI. Every
# PHI definition under src/ and verify_independent/ must source C.PHI (the SSOT)
# via one of the canonical patterns, or be listed in the script's by-design
# SSOT_EXEMPT set (epistemic-circularity guards, from-scratch reproducers).
# Catches inline-literal PHI redefinitions that would silently fork the constant.
phi-ssot-check:
	$(PYTHON) scripts/check_phi_ssot.py

# parity-check verifies that the GENERATED data artifacts reproduce byte-for-byte.
# The manuscript scorecard appendices App_FM and App_R are generator-SEEDED (rows
# from falsifiability_registry.json + scorecard.json) and then CURATED. The curation
# spans more than prose: LaTeX rendering of generator-emitted cells, observed-value
# columns sourced from scorecard.json, and a residual set of tier-disposition rows
# being synced row-by-row into the registry SSOT (numeric/band fields are kept
# registry-consistent). They are therefore not byte-reproducible yet and are
# excluded from this byte-parity gate (see README "Reproducibility scope" for the
# three divergence classes and the closure plan). Re-seeding is `make refresh-all-data`.
parity-check: refresh-all-data
	@test -z "$$(git -c safe.directory="$(abspath ..)" -C .. status --porcelain --untracked-files=all -- GCT_Physics_Engine/data GCT_Physics_Engine/verify_independent/results GCT_Physics_Engine/config GCT_Physics_Engine/falsifiability_registry.json GCT_Physics_Engine/outputs)" || { \
		echo "Generated-artifact parity failed (modified, missing, or untracked paths):"; \
		git -c safe.directory="$(abspath ..)" -C .. status --short --untracked-files=all -- GCT_Physics_Engine/data GCT_Physics_Engine/verify_independent/results GCT_Physics_Engine/config GCT_Physics_Engine/falsifiability_registry.json GCT_Physics_Engine/outputs; \
		exit 1; \
	}

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
