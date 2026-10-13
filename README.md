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
- NDVI is still synthetic until satellite data is added.

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
