import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.config import ASSETS_DIR
from src.data_loader import load_data
from src.climate_analysis import annual_summary


def main():
    ASSETS_DIR.mkdir(exist_ok=True)
    annual = annual_summary(load_data())

    fig, ax = plt.subplots(figsize=(10, 5))
    for division, group in annual.groupby("division"):
        ax.plot(group["year"], group["temperature"], label=division)
    ax.set_title("Average Annual Temperature in Bangladesh")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (°C)")
    ax.legend(ncol=4, fontsize=8)
    fig.tight_layout()
    fig.savefig(ASSETS_DIR / "temperature_trend.png", dpi=150)

    fig, ax = plt.subplots(figsize=(10, 5))
    national = annual.groupby("year")["rainfall"].mean()
    ax.bar(national.index, national.values, color="#2a9d8f")
    ax.set_title("Mean Annual Rainfall Across Divisions")
    ax.set_xlabel("Year")
    ax.set_ylabel("Rainfall (mm)")
    fig.tight_layout()
    fig.savefig(ASSETS_DIR / "rainfall_overview.png", dpi=150)

    fig, ax = plt.subplots(figsize=(10, 5))
    ndvi = annual.groupby("year")["ndvi"].mean()
    ax.plot(ndvi.index, ndvi.values, color="#588157", marker="o")
    ax.set_title("Mean Vegetation Index (NDVI)")
    ax.set_xlabel("Year")
    ax.set_ylabel("NDVI")
    fig.tight_layout()
    fig.savefig(ASSETS_DIR / "ndvi_trend.png", dpi=150)

    print("Charts saved to", ASSETS_DIR)


if __name__ == "__main__":
    main()
