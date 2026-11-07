"""Difference-in-Differences helpers. Requires a validated outlet-month panel."""
from __future__ import annotations

import statsmodels.formula.api as smf

def fit_twfe_did(panel, outcome, outlet="outlet_id", month="month", treated="treated_outlet", post="post"):
    """Fit outlet and month fixed effects with the treatment x post interaction.

    Cluster standard errors at the treatment-assignment level. The caller must
    confirm that the number of clusters supports the chosen inference method.
    """
    data = panel.copy()
    data["did"] = data[treated].astype(int) * data[post].astype(int)
    formula = f"{outcome} ~ did + C({outlet}) + C({month})"
    model = smf.ols(formula, data=data).fit(cov_type="cluster", cov_kwds={"groups": data[outlet]})
    return model
