import pandas as pd
import pytest

from src.data_loader import validate_data


def test_validate_data_rejects_missing_columns():
    with pytest.raises(ValueError):
        validate_data(pd.DataFrame({"date": [1]}))


def test_validate_data_rejects_nan_values():
    df = pd.DataFrame({
        "date": ["2000-01-01"],
        "division": ["Dhaka"],
        "temperature_c": [None],
        "rainfall_mm": [1.0],
        "ndvi": [0.5],
    })
    with pytest.raises(ValueError):
        validate_data(df)
