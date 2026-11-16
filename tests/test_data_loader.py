import pandas as pd

from src.data_loader import load_data, filter_data


def make_csv(tmp_path):
    df = pd.DataFrame({
        "date": ["2000-01-01", "2001-01-01", "2002-01-01"],
        "division": ["Dhaka", "Dhaka", "Sylhet"],
        "temperature_c": [20.0, 21.0, 22.0],
        "rainfall_mm": [10.0, 20.0, 30.0],
        "ndvi": [0.4, 0.5, 0.6],
    })
    path = tmp_path / "data.csv"
    df.to_csv(path, index=False)
    return path


def test_load_data_adds_year_and_month(tmp_path):
    df = load_data(make_csv(tmp_path))
    assert {"year", "month"}.issubset(df.columns)
    assert df["year"].tolist() == [2000, 2001, 2002]


def test_filter_data_by_division_and_year(tmp_path):
    df = load_data(make_csv(tmp_path))
    out = filter_data(df, ["Dhaka"], (2000, 2000))
    assert len(out) == 1
