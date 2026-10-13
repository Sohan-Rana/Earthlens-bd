import pandas as pd

from src.climate_analysis import hottest_years, wettest_months


def test_hottest_years_orders_descending():
    annual = pd.DataFrame({
        "division": ["Dhaka"] * 3,
        "year": [2000, 2001, 2002],
        "temperature": [24.0, 26.0, 25.0],
    })
    out = hottest_years(annual, n=2)
    assert out["year"].tolist() == [2001, 2002]


def test_wettest_months_orders_descending():
    df = pd.DataFrame({
        "month": [1, 7, 7],
        "rainfall_mm": [10.0, 300.0, 100.0],
    })
    out = wettest_months(df)
    assert out.iloc[0]["month"] == 7
