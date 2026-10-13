import numpy as np
import pandas as pd


def annual_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["division", "year"])
        .agg(
            temperature=("temperature_c", "mean"),
            rainfall=("rainfall_mm", "sum"),
            ndvi=("ndvi", "mean"),
        )
        .reset_index()
    )


def linear_trend(years, values):
    """Return (slope per year, intercept) of a least-squares line."""
    slope, intercept = np.polyfit(years, values, 1)
    return float(slope), float(intercept)


def temperature_anomaly(annual: pd.DataFrame, base=(2000, 2010)) -> pd.DataFrame:
    base_mean = (
        annual[annual["year"].between(*base)]
        .groupby("division")["temperature"]
        .mean()
    )
    out = annual.copy()
    out["anomaly"] = out["temperature"] - out["division"].map(base_mean)
    return out


def _minmax(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    if span == 0:
        return series * 0.0
    return (series - series.min()) / span


def risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Simple 0-1 flood and drought indices per division and year."""
    grouped = df.groupby(["division", "year"]).agg(
        annual_rain=("rainfall_mm", "sum"),
        peak_rain=("rainfall_mm", "max"),
        temperature=("temperature_c", "mean"),
    ).reset_index()
    grouped["flood_risk"] = _minmax(grouped["peak_rain"])
    grouped["drought_risk"] = (
        0.6 * (1 - _minmax(grouped["annual_rain"]))
        + 0.4 * _minmax(grouped["temperature"])
    )
    return grouped[["division", "year", "flood_risk", "drought_risk"]]


def hottest_years(annual: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    national = annual.groupby("year", as_index=False)["temperature"].mean()
    return national.sort_values("temperature", ascending=False).head(n)


def wettest_months(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("month", as_index=False)["rainfall_mm"]
        .mean()
        .sort_values("rainfall_mm", ascending=False)
    )


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return df[["temperature_c", "rainfall_mm", "ndvi"]].corr().round(3)
