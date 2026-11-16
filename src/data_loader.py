from pathlib import Path

import pandas as pd

from .config import DATA_PATH, NDVI_PATH, REAL_DATA_PATH

REQUIRED_COLUMNS = {"date", "division", "temperature_c", "rainfall_mm", "ndvi"}


def default_path():
    return REAL_DATA_PATH if REAL_DATA_PATH.exists() else DATA_PATH


def ensure_data() -> None:
    """Create the synthetic sample dataset if no data file exists yet."""
    if DATA_PATH.exists() or REAL_DATA_PATH.exists():
        return
    from .sample_data import generate

    DATA_PATH.parent.mkdir(exist_ok=True)
    generate().to_csv(DATA_PATH, index=False)


def validate_data(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    numeric = list(REQUIRED_COLUMNS - {"date", "division"})
    if df[numeric].isna().any().any():
        raise ValueError("Dataset contains missing values")


def apply_real_ndvi(df: pd.DataFrame, ndvi_path=NDVI_PATH) -> pd.DataFrame:
    """Replace the ndvi column with real MODIS NDVI (wide CSV: date + one column per division).

    Months without a real observation (MODIS starts in Feb 2000) are dropped
    so the dashboard never mixes real and synthetic NDVI.
    """
    real = pd.read_csv(Path(ndvi_path), parse_dates=["date"])
    real = real.melt(id_vars="date", var_name="division", value_name="ndvi")
    real = real.dropna(subset=["ndvi"])
    return df.drop(columns="ndvi").merge(real, on=["date", "division"], how="inner")


def load_data(path=None) -> pd.DataFrame:
    use_real_ndvi = path is None and Path(NDVI_PATH).exists()
    if path is None:
        ensure_data()
        path = default_path()
    df = pd.read_csv(Path(path), parse_dates=["date"])
    if use_real_ndvi:
        df = apply_real_ndvi(df)
    validate_data(df)
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df


def filter_data(df: pd.DataFrame, divisions, year_range) -> pd.DataFrame:
    mask = df["division"].isin(divisions) & df["year"].between(*year_range)
    return df.loc[mask]
