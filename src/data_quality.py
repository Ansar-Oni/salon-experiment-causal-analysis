"""Data-quality helpers. Adapt column names to the supplied source files."""
from __future__ import annotations

import pandas as pd
from rapidfuzz import process, fuzz

def sample_ratio_mismatch(assignment: pd.DataFrame, treatment_col: str = "treatment"):
    """Return observed counts, ratio and chi-square SRM test for a 1:1 design."""
    from scipy.stats import chisquare

    counts = assignment[treatment_col].value_counts().reindex([0, 1], fill_value=0)
    observed = counts.to_numpy(dtype=int)
    total = int(observed.sum())
    if total == 0:
        raise ValueError("Assignment table is empty.")
    expected = [total / 2, total / 2]
    statistic, p_value = chisquare(observed, f_exp=expected)
    return {
        "control_n": int(observed[0]),
        "treatment_n": int(observed[1]),
        "treatment_share": float(observed[1] / total),
        "chi2": float(statistic),
        "p_value": float(p_value),
    }

def standardised_mean_difference(treatment, control):
    """Compute SMD using the pooled within-arm standard deviation."""
    import numpy as np
    treatment = pd.Series(treatment).dropna().astype(float)
    control = pd.Series(control).dropna().astype(float)
    pooled_sd = (((treatment.var(ddof=1) + control.var(ddof=1)) / 2) ** 0.5)
    if pooled_sd == 0 or pd.isna(pooled_sd):
        return 0.0 if treatment.mean() == control.mean() else float("inf")
    return float((treatment.mean() - control.mean()) / pooled_sd)

def map_service_name(raw_name: str, canonical_names: list[str]):
    """Return best canonical match and score; score bands follow project specification."""
    if not canonical_names or not isinstance(raw_name, str):
        return {"match": None, "score": 0, "status": "unmapped"}
    match = process.extractOne(raw_name, canonical_names, scorer=fuzz.token_set_ratio)
    name, score, _ = match
    if score >= 90:
        status = "auto_mapped"
    elif score >= 70:
        status = "manual_review"
    else:
        status = "unmapped"
    return {"match": name if status != "unmapped" else None, "score": float(score), "status": status}
