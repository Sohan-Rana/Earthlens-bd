"""Real NDVI from NASA MODIS MOD13A3 (1 km, monthly), downloaded with AppEEARS."""
import pandas as pd

from .config import MODIS_NDVI_PATH

NDVI_COLUMN = "MOD13A3_061__1_km_monthly_NDVI"
QUALITY_COLUMN = "MOD13A3_061__1_km_monthly_VI_Quality_MODLAND_Description"


def parse_appeears(path) -> pd.DataFrame:
    """Read an AppEEARS point-sample results CSV into division, date, ndvi, quality."""
    raw = pd.read_csv(path)
    missing = {"ID", "Date", NDVI_COLUMN} - set(raw.columns)
    if missing:
        raise ValueError(f"Not an AppEEARS MOD13A3 results file, missing: {sorted(missing)}")
    out = pd.DataFrame({
        "division": raw["ID"],
        "date": pd.to_datetime(raw["Date"]),
        "ndvi": raw[NDVI_COLUMN].round(4),
        "quality": raw.get(QUALITY_COLUMN, pd.Series([""] * len(raw))),
    })
    return out.sort_values(["division", "date"]).reset_index(drop=True)


def load_monthly() -> pd.DataFrame:
    return pd.read_csv(MODIS_NDVI_PATH, parse_dates=["date"])


def has_modis() -> bool:
    return MODIS_NDVI_PATH.exists()


def merge_ndvi(base: pd.DataFrame, ndvi: pd.DataFrame) -> pd.DataFrame:
    """Replace the ndvi column of base with MODIS values (NaN where MODIS has none)."""
    keep = ndvi[["date", "division", "ndvi"]]
    return base.drop(columns="ndvi", errors="ignore").merge(
        keep, on=["date", "division"], how="left"
    )
