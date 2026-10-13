import pandas as pd

from src.config import DATA_PATH, REAL_DATA_PATH, START_YEAR, END_YEAR
from src.nasa_power import fetch_all


def main():
    real = fetch_all(START_YEAR, END_YEAR)
    # NASA POWER has no NDVI, so keep the synthetic NDVI until MODIS data is added.
    sample = pd.read_csv(DATA_PATH, parse_dates=["date"])[["date", "division", "ndvi"]]
    merged = real.merge(sample, on=["date", "division"], how="left")
    merged.to_csv(REAL_DATA_PATH, index=False)
    print(f"Saved {len(merged)} rows to {REAL_DATA_PATH}")


if __name__ == "__main__":
    main()
