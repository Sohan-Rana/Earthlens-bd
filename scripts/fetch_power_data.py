"""Download real monthly temperature and rainfall from NASA POWER.

Run from the repository root:

    python -m scripts.fetch_power_data

Writes data/climate_data_real.csv. The app uses this file automatically when it
exists. Commit the file so the deployed app uses real data too.
"""
from src.config import REAL_DATA_PATH, START_YEAR, END_YEAR
from src.modis_ndvi import has_modis, load_monthly
from src.nasa_power import fetch_all
from src.sample_data import generate


def main():
    real = fetch_all(START_YEAR, END_YEAR)
    # NASA POWER has no NDVI. Use real MODIS NDVI (data/modis_ndvi_monthly.csv) when
    # it exists, otherwise fall back to synthetic NDVI.
    if has_modis():
        merged = real.merge(
            load_monthly()[["date", "division", "ndvi"]], on=["date", "division"], how="left"
        )
    else:
        ndvi = generate()[["date", "division", "ndvi"]]
        merged = real.merge(ndvi, on=["date", "division"], how="left")
        if merged["ndvi"].isna().any():
            raise SystemExit("NDVI merge failed: check START_YEAR/END_YEAR in config.py")
    REAL_DATA_PATH.parent.mkdir(exist_ok=True)
    merged.to_csv(REAL_DATA_PATH, index=False)
    print(f"Saved {len(merged)} rows to {REAL_DATA_PATH}")


if __name__ == "__main__":
    main()
