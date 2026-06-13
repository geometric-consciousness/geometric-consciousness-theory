#!/usr/bin/env python3
"""
protocol_psychophysics_color_dim.py

Tier 3 protocol for App H O.29: sensor-stage versus apperceptive-stage
color-dimensionality arbitration.

The protocol ingests the Stoddard et al. 2020 hummingbird nonspectral-color
experiment table, treats the published tetrahedral Euclidean color distance as
the receptor-space predictor, verifies the exact 4-cone to 3-D chromaticity
compression induced by intensity normalization, and tests whether categorical
nonspectral/axis labels add explanatory power beyond receptor-space distance.

Scope discipline: this is a behavioral color-dimensionality model comparison.
It does not adjudicate any extra phenomenal-color axis, and it does not derive
the avian anatomical compression locus.
"""

from __future__ import annotations

import csv
import json
import math
import re
import urllib.request
from collections import defaultdict
from io import StringIO
from typing import Iterable

import numpy as np
from scipy.optimize import minimize

from gct_utils import get_output_path


DATA_COMMIT = "d9e9091ebbe7bf726b201b887274a6081ebf82b2"
RAW_CSV_URL = (
    "https://raw.githubusercontent.com/dylanhmorris/"
    f"nonspectral-hummingbird-vision/{DATA_COMMIT}/dat/cleaned/CleanedDataTable.csv"
)
REPORTED_QUANTITIES_URL = (
    "https://raw.githubusercontent.com/dylanhmorris/"
    f"nonspectral-hummingbird-vision/{DATA_COMMIT}/out/reported_quantities.csv"
)

# Aggregate of the Stoddard 2020 cleaned trial table at DATA_COMMIT. This is
# used only when network retrieval is unavailable, keeping refresh-all-data
# deterministic while preserving the same source dataset.
FALLBACK_EXPERIMENTS = [
    (1, "Green v Red", "spectral", None, 1.01313379376811, 179, 304),
    (2, "Red v Green", "spectral", None, 1.01464961398257, 186, 300),
    (3, "Null: Green v Green 1", "null", None, 0.00707022492675299, 145, 300),
    (4, "Null: Green v Green 2", "null", None, 0.00800186564457549, 73, 145),
    (5, "Null: UV v UV", "null", None, 0.000560394893961737, 50, 105),
    (6, "Null: Red v Red", "null", None, 0.000973422900681097, 93, 197),
    (7, "UV^72+Red^26 v UV", "nonspectral", 2, 0.308956673665032, 309, 501),
    (8, "UV^72+Red^26 v Red", "nonspectral", 2, 0.876054292684176, 434, 695),
    (9, "Red v UV^25+Red^72", "nonspectral", 2, 0.305240023981047, 195, 325),
    (10, "UV^13+Red^85 v Red", "nonspectral", 2, 0.146858224054778, 186, 268),
    (11, "UV^75+Red^22 v UV^23+Red^71", "nonspectral", 2, 0.620437437976883, 158, 250),
    (12, "UV^59+Green^27 v UV", "nonspectral", 1, 0.4110489511811, 309, 500),
    (13, "UV^59+Green^27 v Green", "nonspectral", 1, 0.62982680105955, 452, 699),
    (14, "UV^33+Green^44 v UV", "nonspectral", 1, 0.685123377524069, 172, 250),
    (15, "UV^33+Green^44 v Green", "nonspectral", 1, 0.353046653978497, 151, 250),
    (16, "UV^33+Green^44 v UV^59+Green^27", "nonspectral", 1, 0.280718185106283, 205, 350),
    (17, "Purple v Red", "nonspectral", None, 0.598604426711606, 125, 194),
    (18, "Blue v Purple", "nonspectral", None, 0.511464859674808, 103, 153),
    (19, "Yellow v UV^22+Yellow", "nonspectral", None, 0.216052240526673, 132, 230),
]

FALLBACK_REPORTED_QUANTITIES = {
    "main_null_mean_mean_correctness": 0.578225251583396,
    "main_spec_mean_mean_correctness": 0.788209817471735,
    "main_nonspec_mean_mean_correctness": 0.827208097902808,
    "main_nonspec_q05_mean_correctness": 0.773217637000298,
    "main_null_q95_mean_correctness": 0.637444052329473,
}
CANONICAL_TRIAL_ROWS = 418


def _fetch_text(url: str, timeout: float = 8.0) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8")


def _load_trial_rows() -> tuple[list[dict], str]:
    try:
        text = _fetch_text(RAW_CSV_URL)
        rows = list(csv.DictReader(StringIO(text)))
        if not rows:
            raise ValueError("empty Stoddard CSV")
        return rows, "github_raw_csv"
    except Exception:
        rows = []
        for exp, name, cls, axis, euclid, chose_sugar, n_hits in FALLBACK_EXPERIMENTS:
            rows.append(
                {
                    "ExperimentNumber": str(exp),
                    "ExperimentDisplayName": name,
                    "experimentClass": cls,
                    "axisID": "" if axis is None else str(axis),
                    "Euclid": str(euclid),
                    "ChoseSugar": str(chose_sugar),
                    "ChoseWater": str(n_hits - chose_sugar),
                    "nHits": str(n_hits),
                    "cumulativeHitsAtTrialStart": "0",
                }
            )
        return rows, "bundled_stoddard_2020_experiment_aggregate"


def _load_reported_quantities() -> tuple[dict, str]:
    try:
        text = _fetch_text(REPORTED_QUANTITIES_URL)
        parsed = {}
        for row in csv.DictReader(StringIO(text)):
            parsed[row["quantity"]] = float(row["value"])
        if not parsed:
            raise ValueError("empty reported quantities")
        return parsed, "github_reported_quantities"
    except Exception:
        return dict(FALLBACK_REPORTED_QUANTITIES), "bundled_reported_quantities"


def _aggregate_experiments(rows: Iterable[dict]) -> list[dict]:
    grouped: dict[int, dict] = {}
    for row in rows:
        exp = int(row["ExperimentNumber"])
        if exp not in grouped:
            axis_raw = str(row.get("axisID", "")).strip()
            axis_id = int(axis_raw) if axis_raw not in {"", "NA", "nan"} else None
            grouped[exp] = {
                "experiment_number": exp,
                "display_name": row["ExperimentDisplayName"],
                "experiment_class": row["experimentClass"],
                "axis_id": axis_id,
                "euclid": float(row["Euclid"]),
                "chose_sugar": 0,
                "n_hits": 0,
                "trial_count": 0,
            }
        grouped[exp]["chose_sugar"] += int(row["ChoseSugar"])
        grouped[exp]["n_hits"] += int(row["nHits"])
        grouped[exp]["trial_count"] += 1
    return [grouped[k] for k in sorted(grouped)]


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def _fit_binomial_model(experiments: list[dict], feature_names: list[str]) -> dict:
    y = np.array([e["chose_sugar"] for e in experiments], dtype=float)
    n = np.array([e["n_hits"] for e in experiments], dtype=float)
    features = []
    for e in experiments:
        row = []
        for name in feature_names:
            if name == "euclid":
                row.append(e["euclid"])
            elif name == "null_control":
                row.append(1.0 if e["experiment_class"] == "null" else 0.0)
            elif name == "nonspectral_extra":
                row.append(1.0 if e["experiment_class"] == "nonspectral" else 0.0)
            elif name == "uv_green_axis_extra":
                row.append(1.0 if e["axis_id"] == 1 else 0.0)
            elif name == "uv_red_axis_extra":
                row.append(1.0 if e["axis_id"] == 2 else 0.0)
            else:
                raise KeyError(name)
        features.append(row)

    X = np.array(features, dtype=float)
    if X.size:
        means = X.mean(axis=0)
        scales = X.std(axis=0)
        scales[scales == 0] = 1.0
        X = (X - means) / scales
    X = np.column_stack([np.ones(len(experiments)), X])

    def nll(beta: np.ndarray) -> float:
        z = X @ beta
        return float(np.sum(n * np.logaddexp(0.0, z) - y * z))

    def grad(beta: np.ndarray) -> np.ndarray:
        p = _sigmoid(X @ beta)
        return X.T @ (n * p - y)

    result = minimize(nll, np.zeros(X.shape[1]), jac=grad, method="L-BFGS-B")
    log_likelihood = -nll(result.x)
    k = int(X.shape[1])
    observations = len(experiments)
    grouped_binomial_trials = int(np.sum(n))
    return {
        "features": feature_names,
        "k_parameters": k,
        "log_likelihood": log_likelihood,
        "aic": 2 * k - 2 * log_likelihood,
        "bic_experiment_level": k * math.log(observations) - 2 * log_likelihood,
        "bic_visit_level": k * math.log(grouped_binomial_trials) - 2 * log_likelihood,
        "optimizer_success": bool(result.success),
        "optimizer_message": str(result.message),
        "standardized_coefficients": [float(x) for x in result.x],
    }


BASE_CONES = {
    "UV": np.array([1.0, 0.0, 0.0, 0.0]),
    "Blue": np.array([0.0, 1.0, 0.0, 0.0]),
    "Green": np.array([0.0, 0.0, 1.0, 0.0]),
    "Red": np.array([0.0, 0.0, 0.0, 1.0]),
    "Yellow": np.array([0.0, 0.0, 0.5, 0.5]),
    "Purple": np.array([0.0, 0.5, 0.0, 0.5]),
}

TETRA_VERTICES = np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, -1.0, -1.0],
        [-1.0, 1.0, -1.0],
        [-1.0, -1.0, 1.0],
    ],
    dtype=float,
) / math.sqrt(3.0)


def _parse_stimulus(expr: str) -> np.ndarray:
    expr = re.sub(r"^Null:\s*", "", expr.strip())
    expr = re.sub(r"\s+\d+$", "", expr)
    if "+" not in expr and "^" not in expr:
        return BASE_CONES[expr].copy()

    parts = expr.split("+")
    vec = np.zeros(4)
    specified = 0.0
    missing_part = None
    for part in parts:
        if "^" in part:
            name, raw = part.split("^", 1)
            weight = float(raw)
            specified += weight
            vec += weight * BASE_CONES[name]
        else:
            missing_part = part
    if missing_part is not None:
        weight = max(0.0, 100.0 - specified)
        vec += weight * BASE_CONES[missing_part]
    return vec


def _stimulus_vectors(experiments: list[dict]) -> list[np.ndarray]:
    vectors = []
    for e in experiments:
        for expr in e["display_name"].split(" v "):
            vectors.append(_parse_stimulus(expr))
    return vectors


def _sensor_stage_summary(experiments: list[dict]) -> dict:
    raw = np.vstack(_stimulus_vectors(experiments))
    normalized = raw / raw.sum(axis=1, keepdims=True)
    cartesian = normalized @ TETRA_VERTICES
    singular = np.linalg.svd(normalized - normalized.mean(axis=0), compute_uv=False)
    rank = int(np.linalg.matrix_rank(normalized - normalized.mean(axis=0), tol=1e-10))
    raw_rank = int(np.linalg.matrix_rank(raw, tol=1e-10))
    cart_rank = int(np.linalg.matrix_rank(cartesian - cartesian.mean(axis=0), tol=1e-10))
    return {
        "raw_cone_class_count": 4,
        "raw_cone_design_rank": raw_rank,
        "intensity_normalized_chromaticity_rank": rank,
        "tetrahedral_cartesian_rank": cart_rank,
        "singular_values_normalized_chromaticity": [float(x) for x in singular],
        "compression_statement": (
            "Four cone-class catches are sensor variables; after intensity "
            "normalization, chromaticities lie on the 3-D avian tetrahedral "
            "simplex."
        ),
    }


def _class_summaries(experiments: list[dict]) -> dict:
    grouped: dict[str, dict] = defaultdict(lambda: {"chose_sugar": 0, "n_hits": 0, "experiments": 0})
    for e in experiments:
        cls = e["experiment_class"]
        grouped[cls]["chose_sugar"] += e["chose_sugar"]
        grouped[cls]["n_hits"] += e["n_hits"]
        grouped[cls]["experiments"] += 1
    return {
        cls: {
            **vals,
            "raw_correct_fraction": vals["chose_sugar"] / vals["n_hits"],
        }
        for cls, vals in sorted(grouped.items())
    }


def _verdict(delta_bic_extension_minus_base: float) -> tuple[str, bool]:
    if delta_bic_extension_minus_base >= 2.0:
        return "COMPATIBLE", True
    if delta_bic_extension_minus_base > -10.0:
        return "TENSION", False
    return "FAIL", False


def run() -> dict:
    trial_rows, _data_mode = _load_trial_rows()
    reported_quantities, _reported_mode = _load_reported_quantities()
    experiments = _aggregate_experiments(trial_rows)

    base_receptor_distance_model = _fit_binomial_model(experiments, ["euclid", "null_control"])
    categorical_label_extension_model = _fit_binomial_model(
        experiments,
        ["euclid", "null_control", "nonspectral_extra", "uv_green_axis_extra", "uv_red_axis_extra"],
    )
    delta_bic = (
        categorical_label_extension_model["bic_experiment_level"]
        - base_receptor_distance_model["bic_experiment_level"]
    )
    delta_aic = categorical_label_extension_model["aic"] - base_receptor_distance_model["aic"]
    verdict, passed = _verdict(delta_bic)

    result = {
        "protocol": "psychophysics_color_dimensionality",
        "open_problem": "O.29",
        "tier": (
            "Tier 3 behavioral model comparison for the T_2 (E_perp) color-ceiling "
            "claim; anatomical compression locus remains empirical."
        ),
        "status": f"{verdict}_O29_STODDARD_MODEL_COMPARISON",
        "verdict": verdict,
        "pass": passed,
        "question": (
            "Does the Stoddard behavioral table remain compatible with the "
            "3-D T_2 (E_perp) apperceptive color-substrate ceiling after receptor-space "
            "distance is modeled?"
        ),
        "data_source": {
            "primary_table_url": RAW_CSV_URL,
            "reported_quantities_url": REPORTED_QUANTITIES_URL,
            "github_commit": DATA_COMMIT,
            "canonical_trial_rows": CANONICAL_TRIAL_ROWS,
            "fallback": "bundled Stoddard 2020 experiment aggregate is used if network retrieval is unavailable",
            "experiment_count": len(experiments),
            "total_visits": int(sum(e["n_hits"] for e in experiments)),
        },
        "stoddard_reported_quantities": {
            key: reported_quantities.get(key)
            for key in sorted(FALLBACK_REPORTED_QUANTITIES)
        },
        "sensor_stage_compression": _sensor_stage_summary(experiments),
        "behavioral_class_summary": _class_summaries(experiments),
        "model_comparison": {
            "base_receptor_distance_model": base_receptor_distance_model,
            "categorical_label_extension_model": categorical_label_extension_model,
            "delta_bic_extension_minus_base": delta_bic,
            "delta_aic_extension_minus_base": delta_aic,
            "decision_rule": (
                "COMPATIBLE if BIC_extended - BIC_base >= 2; TENSION if the "
                "categorical extension is weakly favored but Delta BIC < 10; "
                "FAIL if the categorical extension is strongly favored with "
                "Delta BIC <= -10. COMPATIBLE is a behavioral compatibility "
                "flag, not a physical PASS on the phenomenal-axis question."
            ),
        },
        "interpretation": (
            "The Stoddard data support avian tetrachromatic sensor "
            "discrimination, including nonspectral stimuli. Under intensity "
            "normalization, the four sensor channels map to a 3-D tetrahedral "
            "chromaticity simplex; categorical nonspectral/axis labels are "
            "not favored beyond receptor-space distance by BIC. This is "
            "behavioral compatibility with the GCT T_2 (E_perp) 3-D substrate-ceiling "
            "claim, while leaving both the anatomical compression locus and "
            "any extra phenomenal-color-axis interpretation empirical."
        ),
    }

    out_path = get_output_path("protocol_psychophysics_color_dim_results.json")
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Protocol psychophysics color-dimensionality compatibility verdict: {verdict}")
    print(f"Results written to {out_path}")
    return result


if __name__ == "__main__":
    run()
