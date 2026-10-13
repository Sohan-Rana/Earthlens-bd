import plotly.express as px

from .config import DIVISION_COORDS


def temperature_chart(annual):
    return px.line(
        annual, x="year", y="temperature", color="division",
        title="Average Annual Temperature (°C)",
    )


def rainfall_chart(annual):
    return px.bar(
        annual, x="year", y="rainfall", color="division", barmode="group",
        title="Total Annual Rainfall (mm)",
    )


def ndvi_chart(annual):
    return px.line(
        annual, x="year", y="ndvi", color="division",
        title="Vegetation Health (Mean NDVI)",
    )


def anomaly_chart(anomaly_df):
    return px.bar(
        anomaly_df, x="year", y="anomaly", color="division",
        title="Temperature Anomaly vs 2000-2010 Baseline (°C)",
    )


def monthly_heatmap(df, column="rainfall_mm"):
    pivot = df.pivot_table(index="division", columns="month", values=column, aggfunc="mean")
    return px.imshow(
        pivot, aspect="auto", color_continuous_scale="Viridis",
        title=f"Monthly Average: {column}",
    )


def division_map(annual, column="temperature"):
    latest = annual[annual["year"] == annual["year"].max()].copy()
    latest["lat"] = latest["division"].map(lambda d: DIVISION_COORDS[d][0])
    latest["lon"] = latest["division"].map(lambda d: DIVISION_COORDS[d][1])
    return px.scatter_map(
        latest, lat="lat", lon="lon", size=column, color=column,
        hover_name="division", zoom=5.6, size_max=30,
        map_style="open-street-map",
        title=f"{column.title()} by Division (latest year)",
    )


def risk_chart(risk_df):
    melted = risk_df.melt(
        id_vars=["division", "year"],
        value_vars=["flood_risk", "drought_risk"],
        var_name="risk", value_name="score",
    )
    return px.line(
        melted, x="year", y="score", color="division", facet_col="risk",
        title="Flood and Drought Risk Index (0 = low, 1 = high)",
    )


def correlation_chart(corr):
    return px.imshow(
        corr, text_auto=True, zmin=-1, zmax=1,
        color_continuous_scale="RdBu_r",
        title="Correlation Between Climate Variables",
    )
