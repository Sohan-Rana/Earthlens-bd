# EarthLens BD

Climate and environmental data explorer for Bangladesh, built with Python, Pandas, Plotly and Streamlit.

## Features
**Live demo:** https://earthlens-bd-jdsc6rgqc6uazwhhvy9nyh.streamlit.app/
- Temperature and rainfall trends by division
- Temperature anomaly against a 2000-2010 baseline
- NDVI green cover charts
- Monthly heatmap, division map and flood/drought risk indices
- Hottest years ranking and correlation heatmap
- Filtered CSV download
- Significance tab: Mann-Kendall trend test and Sen's slope per division, with p-values

## Data

| Variable | Source | Status |
|---|---|---|
| Temperature (T2M) | NASA POWER | Real after running the fetch script; synthetic sample by default |
| Rainfall (PRECTOTCORR) | NASA POWER | Real after running the fetch script; synthetic sample by default |
| NDVI | NASA MODIS MOD13A3 (1 km, monthly) via AppEEARS | Real. January 2000 is empty because MODIS starts in February 2000 |

- By default the app uses synthetic sample data, created automatically on first run. A banner in the app shows which data is in use.
- To use real NASA POWER data, run the command below, then commit `data/climate_data_real.csv`. The app switches to it automatically.

      python -m scripts.fetch_power_data

- NASA POWER is gridded data. Each division is represented by one point near its main city, not a division-wide average.
- Rainfall is converted from mm/day to monthly totals.
- NASA POWER rainfall shows an abrupt jump after 2015 in several divisions (for example Chattogram 7,374 mm in 2017). Treat rainfall trends with caution until checked against another source.

### NDVI (MODIS)

NDVI comes from MOD13A3 v061, sampled at one point per division (the same points as NASA POWER) with NASA AppEEARS and stored in `data/modis_ndvi_monthly.csv`. To rebuild it, request the `_1_km_monthly_NDVI` layer in AppEEARS (point sample, 2000-02-01 to 2023-12-31, upload the 8 division points), then run:

    python -m scripts.merge_modis_ndvi path/to/bd-ndvi-MOD13A3-061-results.csv

Limitations: about 17% of values are flagged "most probably cloudy" and 23% "check other QA" by MODIS (all values are kept), and several division points fall on coastal or river pixels where water lowers NDVI.

## Trend significance

The Significance tab runs a two-sided Mann-Kendall test (alpha = 0.05) on annual
values for each division and reports Sen's slope (median yearly change), the
total change over the period and the p-value. The implementation is in
`src/trend_stats.py` and is tested against `pymannkendall`.

## Quick start

    pip install -r requirements.txt
    streamlit run app.py

## Tests

    python -m pytest

## Roadmap

- District-level analysis with GeoPandas
- Deployment on Streamlit Community Cloud

## License

MIT
