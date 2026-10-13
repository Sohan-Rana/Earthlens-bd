import pandas as pd

from .config import DATA_PATH, REAL_DATA_PATH

REQUIRED_COLUMNS = {"date", "division", "temperature_c", "rainfall_mm", "ndvi"}


def default_path():
    return REAL_DATA_PATH if REAL_DATA_PATH.exists() else DATA_PATH


def validate_data(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    numeric = list(REQUIRED_COLUMNS - {"date", "division"})
    if df[numeric].isna().any().any():
        raise ValueError("Dataset contains missing values")


def load_data(path=None) -> pd.DataFrame:
    df = pd.read_csv(path or default_path(), parse_dates=["date"])
    validate_data(df)
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df


def filter_data(df: pd.DataFrame, divisions, year_range) -> pd.DataFrame:
    mask = df["division"].isin(divisions) & df["year"].between(*year_range)
    return df.loc[mask]
