import pandas as pd
import pytest

from src.trend_stats import mann_kendall, trend_table


def test_increasing_series_is_significant():
    res = mann_kendall(list(range(20)))
    assert res["trend"] == "increasing"
    assert res["significant"] is True
    assert res["p_value"] < 0.001
    assert res["sen_slope"] == pytest.approx(1.0)


def test_decreasing_series_is_significant():
    res = mann_kendall([20 - i for i in range(20)])
    assert res["trend"] == "decreasing"
    assert res["sen_slope"] == pytest.approx(-1.0)


def test_flat_series_has_no_trend():
    res = mann_kendall([5.0] * 12)
    assert res["trend"] == "no trend"
    assert res["significant"] is False
    assert res["p_value"] == pytest.approx(1.0)


def test_known_value_matches_reference():
    # Reference values from pymannkendall.original_test on this series.
    res = mann_kendall([1, 3, 2, 5, 4, 7, 6, 9, 8, 10])
    assert res["trend"] == "increasing"
    assert res["sen_slope"] == pytest.approx(1.0)


def test_too_few_values_raises():
    with pytest.raises(ValueError):
        mann_kendall([1, 2])


def test_trend_table_skips_short_series_and_labels_divisions():
    long = pd.DataFrame({
        "division": ["Dhaka"] * 12,
        "year": list(range(2000, 2012)),
        "temperature": [25 + 0.1 * i for i in range(12)],
    })
    short = pd.DataFrame({
        "division": ["Sylhet"] * 3,
        "year": [2000, 2001, 2002],
        "temperature": [24.0, 24.1, 24.2],
    })
    out = trend_table(pd.concat([long, short]), "temperature")
    assert out["division"].tolist() == ["Dhaka"]
    assert out.loc[0, "significant"] == "Yes"
    assert out.loc[0, "sen_slope_per_year"] == pytest.approx(0.1, abs=1e-4)
