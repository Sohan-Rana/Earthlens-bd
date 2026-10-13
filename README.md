# EarthLens BD

Climate and environmental data explorer for Bangladesh, built with Python, Pandas, Plotly and Streamlit.

## Preview

![Temperature trend](assets/temperature_trend.png)
![Rainfall overview](assets/rainfall_overview.png)
![NDVI trend](assets/ndvi_trend.png)

## Features

- Temperature and rainfall trends by division
- Temperature anomaly against a 2000-2010 baseline
- NDVI green cover charts
- Monthly heatmap, division map and flood/drought risk indices
- Hottest years ranking and correlation heatmap
- Filtered CSV download

## Data

- By default the app uses synthetic sample data created by `scripts/generate_data.py`.
- Real monthly temperature and rainfall can be downloaded from NASA POWER with `scripts/fetch_power_data.py`.
- NDVI is still synthetic until satellite data is added.

## Quick start

    pip install -r requirements.txt
    python -m scripts.generate_data
    python -m scripts.export_charts
    python -m scripts.fetch_power_data   # optional, needs internet
    streamlit run app.py

## Tests

    python -m pytest

## Roadmap

- Real MODIS NDVI data
- District-level analysis with GeoPandas
- Deployment on Streamlit Community Cloud

## License

MIT
