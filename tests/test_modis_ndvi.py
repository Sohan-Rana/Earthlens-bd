import pandas as pd
import pytest

from src.data_loader import validate_data
from src.modis_ndvi import NDVI_COLUMN, merge_ndvi, parse_appeears


def make_appeears_csv(tmp_path):
    raw = pd.DataFrame({
        "Category": ["Division", "Division"],
        "ID": ["Dhaka", "Dhaka"],
        "Latitude": [23.81, 23.81],
        "Longitude": [90.41, 90.41],
        "Date": ["2000-02-01", "2000-03-01"],
        NDVI_COLUMN: [0.35, 0.41],
    })
    path = tmp_path / "results.csv"
    raw.to_csv(path, index=False)
    return path


def test_parse_appeears_returns_division_date_ndvi(tmp_path):
    out = parse_appeears(make_appeears_csv(tmp_path))
    assert out.columns.tolist() == ["division", "date", "ndvi", "quality"]
    assert out["division"].tolist() == ["Dhaka", "Dhaka"]
    assert out["date"].iloc[0] == pd.Timestamp("2000-02-01")


def test_parse_appeears_rejects_other_files(tmp_path):
    path = tmp_path / "other.csv"
    pd.DataFrame({"a": [1]}).to_csv(path, index=False)
    with pytest.raises(ValueError):
        parse_appeears(path)


def test_merge_replaces_ndvi_and_leaves_gaps_empty():
    base = pd.DataFrame({
        "date": pd.to_datetime(["2000-01-01", "2000-02-01"]),
        "division": ["Dhaka", "Dhaka"],
        "temperature_c": [18.0, 20.0],
        "rainfall_mm": [8.0, 26.0],
        "ndvi": [0.9, 0.9],  # synthetic values that must be replaced
    })
    ndvi = pd.DataFrame({
        "date": pd.to_datetime(["2000-02-01"]),
        "division": ["Dhaka"],
        "ndvi": [0.35],
    })
    out = merge_ndvi(base, ndvi)
    assert pd.isna(out.loc[0, "ndvi"])
    assert out.loc[1, "ndvi"] == 0.35
    validate_data(out)  # empty NDVI is allowed
