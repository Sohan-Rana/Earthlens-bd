"""Put real MODIS NDVI (from an AppEEARS download) into the dataset.

    python -m scripts.merge_modis_ndvi path/to/bd-ndvi-MOD13A3-061-results.csv

Writes data/modis_ndvi_monthly.csv (trimmed copy of the NDVI values) and
updates the ndvi column of data/climate_data_real.csv. MODIS starts in
February 2000, so January 2000 has no NDVI and is left empty.
"""
import sys

import pandas as pd

from src.config import DIVISIONS, MODIS_NDVI_PATH, REAL_DATA_PATH
from src.modis_ndvi import merge_ndvi, parse_appeears


def main(path):
    ndvi = parse_appeears(path)
    found = set(ndvi["division"])
    if found != set(DIVISIONS):
        raise SystemExit(f"Division mismatch. Missing: {sorted(set(DIVISIONS) - found)}")
    MODIS_NDVI_PATH.parent.mkdir(exist_ok=True)
    ndvi.to_csv(MODIS_NDVI_PATH, index=False)

    if not REAL_DATA_PATH.exists():
        raise SystemExit("Run scripts.fetch_power_data first (data/climate_data_real.csv is missing).")
    base = pd.read_csv(REAL_DATA_PATH, parse_dates=["date"])
    merged = merge_ndvi(base, ndvi)[list(base.columns)]
    merged.to_csv(REAL_DATA_PATH, index=False)
    print(f"Saved {len(ndvi)} NDVI rows to {MODIS_NDVI_PATH}")
    print(f"Updated {REAL_DATA_PATH}: {merged['ndvi'].notna().sum()} of {len(merged)} rows have NDVI")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
