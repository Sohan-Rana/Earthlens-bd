from src.data_loader import load_data
from src.climate_analysis import annual_summary, linear_trend


def main():
    annual = annual_summary(load_data())
    print(f"{'Division':<12} {'Trend (C/year)':>15}")
    for division, group in annual.groupby("division"):
        slope, _ = linear_trend(group["year"], group["temperature"])
        print(f"{division:<12} {slope:>+15.4f}")


if __name__ == "__main__":
    main()
