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

## Data

- By default the app uses synthetic sample data, created automatically on first run.
- Real monthly temperature and rainfall can be downloaded from NASA POWER with `scripts/fetch_power_data.py`.
- **NDVI is real NASA data.** `data/bd_ndvi_modis.csv` holds monthly 1 km NDVI (MODIS Terra
  MOD13A3.061, Feb 2000 - Dec 2023) sampled at one point per division, requested through
  [NASA AppEEARS](https://appeears.earthdatacloud.nasa.gov/). When this file is present the app
  uses it automatically; months without a real observation (Jan 2000) are dropped.
- Temperature and rainfall are still synthetic unless you fetch the NASA POWER data.
- Caveat: each value is a single 1 km pixel at the division's coordinates, so coastal or river
  pixels can read lower than the division as a whole. It is not a division-wide average.

## Quick start

    pip install -r requirements.txt
    streamlit run app.py

## Tests

    python -m pytest

## Roadmap

- Division-wide NDVI averages (zonal statistics) instead of single points
- District-level analysis with GeoPandas

## License

MIT
