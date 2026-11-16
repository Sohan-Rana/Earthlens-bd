import streamlit as st

from src.data_loader import load_data, filter_data, data_source
from src.climate_analysis import (
    annual_summary, temperature_anomaly, linear_trend, risk_scores,
    hottest_years, correlation_matrix,
)
from src import charts
from src.trend_stats import trend_table

st.set_page_config(page_title="EarthLens BD", page_icon="🌍", layout="wide")
st.title("🌍 EarthLens BD")
st.caption("Climate & Environmental Data Explorer for Bangladesh")

if data_source() == "real":
    st.success("Temperature and rainfall: real NASA POWER data. "
               "NDVI: synthetic sample (MODIS NDVI planned).")
else:
    st.warning("Demo mode: all data is synthetic sample data. "
               "Run `python -m scripts.fetch_power_data` to use real NASA POWER data.")


@st.cache_data
def get_data():
    return load_data()


df = get_data()

st.sidebar.header("Filters")
divisions = st.sidebar.multiselect(
    "Divisions", sorted(df["division"].unique()), default=["Dhaka", "Sylhet"]
)
year_range = st.sidebar.slider(
    "Year range", int(df["year"].min()), int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max())),
)

filtered = filter_data(df, divisions, year_range)
if filtered.empty:
    st.warning("Select at least one division.")
    st.stop()

st.sidebar.download_button(
    "Download filtered data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="earthlens_bd_filtered.csv",
    mime="text/csv",
)

annual = annual_summary(filtered)

c1, c2, c3 = st.columns(3)
c1.metric("Avg temperature", f"{annual['temperature'].mean():.2f} °C")
c2.metric("Avg annual rainfall", f"{annual['rainfall'].mean():.0f} mm")
slope, _ = linear_trend(annual["year"], annual["temperature"])
c3.metric("Temperature trend", f"{slope:+.3f} °C/year")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    ["Temperature", "Rainfall", "Green cover", "Monthly heatmap",
     "Map", "Risk", "Insights", "Significance"]
)
with tab1:
    st.plotly_chart(charts.temperature_chart(annual), use_container_width=True)
    st.plotly_chart(charts.anomaly_chart(temperature_anomaly(annual)), use_container_width=True)
with tab2:
    st.plotly_chart(charts.rainfall_chart(annual), use_container_width=True)
with tab3:
    st.plotly_chart(charts.ndvi_chart(annual), use_container_width=True)
with tab4:
    st.plotly_chart(charts.monthly_heatmap(filtered), use_container_width=True)
with tab5:
    metric = st.selectbox("Map metric", ["temperature", "rainfall", "ndvi"])
    st.plotly_chart(charts.division_map(annual, metric), use_container_width=True)
with tab6:
    risk = risk_scores(filtered)
    st.plotly_chart(charts.risk_chart(risk), use_container_width=True)
    st.caption("Indices are simple min-max scores, not official forecasts.")
with tab7:
    st.subheader("Hottest years")
    st.dataframe(hottest_years(annual), hide_index=True)
    st.subheader("Correlations")
    st.plotly_chart(
        charts.correlation_chart(correlation_matrix(filtered)),
        use_container_width=True,
    )
with tab8:
    st.subheader("Is the change statistically significant?")
    variable = st.radio(
        "Variable", ["temperature", "rainfall"], horizontal=True,
        format_func=lambda v: {"temperature": "Temperature (°C)",
                               "rainfall": "Annual rainfall (mm)"}[v],
    )
    table = trend_table(annual, variable)
    if table.empty:
        st.info("Select a longer year range (at least 8 years) to run the test.")
    else:
        st.dataframe(table, hide_index=True, use_container_width=True)
    if variable == "rainfall" and data_source() == "real":
        st.warning(
            "Data-quality note: NASA POWER rainfall for several divisions rises "
            "abruptly after 2015 (some monthly totals exceed 1,500 mm). The "
            "rainfall trends above may reflect this jump in the source data and "
            "not a real climate change. Check against another rainfall source "
            "before drawing conclusions."
        )
    st.caption(
        "Mann-Kendall test (two-sided, alpha = 0.05) on annual values per division. "
        "Sen's slope is the median yearly change. 'Significant = Yes' means the "
        "trend is unlikely to be random (p < 0.05). With synthetic sample data "
        "these results are for demonstration only."
    )
