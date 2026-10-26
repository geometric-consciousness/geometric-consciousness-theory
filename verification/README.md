# Verification records

Public records of the preregistered tests reported in v1.3.0. Files under this folder are byte-exact
copies of frozen inputs and machine outputs, so their SHA-256 values can be checked against the
bundle manifests.

- [`constant_control_test/`](constant_control_test/README.md): φ against random constants on 21
  measured constants (App PSC §PSC.9.6). v1 and v2 invalid; v3 NEGATIVE-FRAGILE.
- [`observer_test/`](observer_test/README.md): observer-correction sign test. Rule A refuted.

The gauge-running audit of App GRF §GRF.4.3 is reported in that section.
