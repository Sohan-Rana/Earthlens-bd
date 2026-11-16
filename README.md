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
| NDVI | Synthetic | Real MODIS NDVI is planned |

- By default the app uses synthetic sample data, created automatically on first run. A banner in the app shows which data is in use.
- To use real NASA POWER data, run the command below, then commit `data/climate_data_real.csv`. The app switches to it automatically.

      python -m scripts.fetch_power_data

- NASA POWER is gridded data. Each division is represented by one point near its main city, not a division-wide average.
- Rainfall is converted from mm/day to monthly totals.

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

- Real MODIS NDVI data
- District-level analysis with GeoPandas
- Deployment on Streamlit Community Cloud

## License

MIT
