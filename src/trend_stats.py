"""Trend significance: Mann-Kendall test and Sen's slope (no extra dependencies)."""
import math

import numpy as np
import pandas as pd

MIN_YEARS = 8


def mann_kendall(values, alpha: float = 0.05) -> dict:
    """Two-sided Mann-Kendall test with tie correction.

    Returns trend direction, p-value, Sen's slope (units per step) and whether
    the trend is significant at the given alpha.
    """
    x = np.asarray(values, dtype=float)
    n = len(x)
    if n < 3:
        raise ValueError("Need at least 3 values")

    s = 0
    for i in range(n - 1):
        s += int(np.sign(x[i + 1:] - x[i]).sum())

    _, counts = np.unique(x, return_counts=True)
    ties = float(sum(c * (c - 1) * (2 * c + 5) for c in counts if c > 1))
    var_s = (n * (n - 1) * (2 * n + 5) - ties) / 18.0

    if s > 0:
        z = (s - 1) / math.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / math.sqrt(var_s)
    else:
        z = 0.0
    p = math.erfc(abs(z) / math.sqrt(2))  # = 2 * (1 - Phi(|z|))

    slopes = [
        (x[j] - x[i]) / (j - i) for i in range(n - 1) for j in range(i + 1, n)
    ]
    slope = float(np.median(slopes))

    significant = p < alpha
    if not significant:
        trend = "no trend"
    else:
        trend = "increasing" if z > 0 else "decreasing"
    return {
        "trend": trend,
        "p_value": float(p),
        "sen_slope": slope,
        "significant": bool(significant),
    }


def trend_table(annual: pd.DataFrame, column: str, alpha: float = 0.05) -> pd.DataFrame:
    """One row per division with Mann-Kendall results for an annual column."""
    rows = []
    for division, group in annual.groupby("division"):
        series = group.sort_values("year")[column]
        if len(series) < MIN_YEARS:
            continue
        res = mann_kendall(series.values, alpha)
        rows.append({
            "division": division,
            "trend": res["trend"],
            "sen_slope_per_year": round(res["sen_slope"], 4),
            "total_change": round(res["sen_slope"] * (len(series) - 1), 3),
            "p_value": round(res["p_value"], 4),
            "significant": "Yes" if res["significant"] else "No",
        })
    return pd.DataFrame(
        rows,
        columns=["division", "trend", "sen_slope_per_year", "total_change",
                 "p_value", "significant"],
    )
