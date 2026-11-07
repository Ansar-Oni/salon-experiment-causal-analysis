"""Experiment effect estimation helpers."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportion_confint

def retention_difference_ci(data, outcome="retained_90d", treatment="treatment", alpha=0.05):
    """Unadjusted treatment-minus-control difference in proportions with a Wald CI."""
    d = data[[outcome, treatment]].dropna()
    t = d.loc[d[treatment] == 1, outcome].astype(int)
    c = d.loc[d[treatment] == 0, outcome].astype(int)
    if len(t) == 0 or len(c) == 0:
        raise ValueError("Both treatment and control arms must contain observations.")
    p_t, p_c = t.mean(), c.mean()
    diff = p_t - p_c
    se = np.sqrt(p_t * (1-p_t) / len(t) + p_c * (1-p_c) / len(c))
    z = stats.norm.ppf(1-alpha/2)
    return {
        "control_rate": float(p_c), "treatment_rate": float(p_t),
        "effect": float(diff), "ci_low": float(diff-z*se), "ci_high": float(diff+z*se),
        "n_control": int(len(c)), "n_treatment": int(len(t)),
    }

def welch_revenue_test(data, outcome="revenue_per_visit", treatment="treatment"):
    """Welch t-test for difference in client-level mean revenue."""
    d = data[[outcome, treatment]].dropna()
    t = d.loc[d[treatment] == 1, outcome].astype(float)
    c = d.loc[d[treatment] == 0, outcome].astype(float)
    test = stats.ttest_ind(t, c, equal_var=False)
    diff = t.mean() - c.mean()
    se = np.sqrt(t.var(ddof=1)/len(t) + c.var(ddof=1)/len(c))
    df_num = (t.var(ddof=1)/len(t) + c.var(ddof=1)/len(c))**2
    df_den = (t.var(ddof=1)/len(t))**2/(len(t)-1) + (c.var(ddof=1)/len(c))**2/(len(c)-1)
    df = df_num/df_den
    crit = stats.t.ppf(0.975, df)
    return {"effect": float(diff), "ci_low": float(diff-crit*se), "ci_high": float(diff+crit*se),
            "p_value": float(test.pvalue), "n_control": len(c), "n_treatment": len(t)}

def client_bootstrap_mean_difference(data, outcome, treatment="treatment", n_boot=10000, seed=2026):
    """Bootstrap treatment-control mean difference by client-level rows."""
    rng = np.random.default_rng(seed)
    t = data.loc[data[treatment] == 1, outcome].dropna().to_numpy()
    c = data.loc[data[treatment] == 0, outcome].dropna().to_numpy()
    if len(t) == 0 or len(c) == 0:
        raise ValueError("Both arms need observations.")
    draws = np.empty(n_boot)
    for i in range(n_boot):
        draws[i] = rng.choice(t, len(t), replace=True).mean() - rng.choice(c, len(c), replace=True).mean()
    return {"effect": float(t.mean()-c.mean()),
            "ci_low": float(np.quantile(draws, 0.025)),
            "ci_high": float(np.quantile(draws, 0.975)),
            "bootstrap_draws": int(n_boot)}
