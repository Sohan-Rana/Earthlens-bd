import pandas as pd

from src.climate_analysis import annual_summary, linear_trend, temperature_anomaly


def test_annual_summary_sums_rainfall():
    df = pd.DataFrame({
        "division": ["Dhaka", "Dhaka"],
        "year": [2000, 2000],
        "temperature_c": [20.0, 30.0],
        "rainfall_mm": [100.0, 50.0],
        "ndvi": [0.4, 0.6],
    })
    out = annual_summary(df)
    assert out.loc[0, "rainfall"] == 150.0
    assert out.loc[0, "temperature"] == 25.0


def test_linear_trend_slope():
    slope, intercept = linear_trend([0, 1, 2], [1, 3, 5])
    assert round(slope, 6) == 2.0
    assert round(intercept, 6) == 1.0


def test_temperature_anomaly_baseline():
    annual = pd.DataFrame({
        "division": ["Dhaka", "Dhaka"],
        "year": [2000, 2001],
        "temperature": [10.0, 12.0],
    })
    out = temperature_anomaly(annual)
    assert out["anomaly"].tolist() == [-1.0, 1.0]
