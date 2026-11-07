"""CUPED adjustment using pre-randomisation covariates only."""
from __future__ import annotations

import numpy as np
import pandas as pd

def apply_cuped(data: pd.DataFrame, outcome: str, pre_covariate: str):
    """Return a copy with CUPED-adjusted outcome and estimated variance reduction.

    The pre_covariate must be measured before randomisation and must not be
    affected by treatment.
    """
    d = data.copy()
    y = d[outcome].astype(float)
    x = d[pre_covariate].astype(float)
    theta = np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1)
    d[f"{outcome}_cuped"] = y - theta * (x - x.mean())
    rho = np.corrcoef(y, x)[0, 1]
    return d, {"theta": float(theta), "rho": float(rho), "rho_squared": float(rho**2),
               "approx_sample_fraction_remaining": float(1-rho**2)}
