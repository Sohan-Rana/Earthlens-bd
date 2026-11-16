import pandas as pd

from src.config import DIVISIONS, NDVI_PATH
from src.data_loader import apply_real_ndvi, load_data


def _base():
    return pd.DataFrame({
        "date": pd.to_datetime(["2000-01-01", "2000-02-01"] * 2),
        "division": ["Dhaka", "Dhaka", "Sylhet", "Sylhet"],
        "temperature_c": [20.0, 22.0, 19.0, 21.0],
        "rainfall_mm": [5.0, 10.0, 6.0, 12.0],
        "ndvi": [0.9, 0.9, 0.9, 0.9],
    })


def test_apply_real_ndvi_replaces_values_and_drops_unmatched_months(tmp_path):
    f = tmp_path / "ndvi.csv"
    f.write_text("date,Dhaka,Sylhet\n2000-02-01,0.33,0.39\n")
    out = apply_real_ndvi(_base(), f)
    assert len(out) == 2  # January has no real NDVI
    assert set(out["ndvi"]) == {0.33, 0.39}
    assert (out["date"] == pd.Timestamp("2000-02-01")).all()


def test_bundled_ndvi_file_is_complete_and_in_range():
    wide = pd.read_csv(NDVI_PATH, parse_dates=["date"])
    assert list(wide.columns[1:]) == DIVISIONS
    assert len(wide) == 287  # Feb 2000 - Dec 2023
    assert not wide.isna().any().any()
    assert wide[DIVISIONS].stack().between(-0.2, 1.0).all()


def test_load_data_uses_real_ndvi_by_default():
    df = load_data()
    assert df["date"].min() == pd.Timestamp("2000-02-01")
    assert df["ndvi"].between(0.1, 0.9).all()
