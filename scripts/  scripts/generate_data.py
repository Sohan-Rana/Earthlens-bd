import numpy as np
import pandas as pd

from src.config import DATA_PATH, DIVISIONS, START_YEAR, END_YEAR


def generate(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for i, division in enumerate(DIVISIONS):
        base_temp = 25 + (i % 3) * 0.4
        base_rain = 120 + i * 12
        for year in range(START_YEAR, END_YEAR + 1):
            for month in range(1, 13):
                season = np.sin((month - 4) / 12 * 2 * np.pi)
                monsoon = 1 + 0.9 * np.sin((month - 3) / 12 * 2 * np.pi)
                temp = base_temp + 5 * season + 0.04 * (year - START_YEAR) + rng.normal(0, 0.6)
                rain = max(0.0, base_rain * monsoon * rng.uniform(0.6, 1.4))
                ndvi = float(np.clip(
                    0.45 + 0.2 * np.sin((month - 5) / 12 * 2 * np.pi) + rng.normal(0, 0.03), 0, 1
                ))
                rows.append({
                    "date": pd.Timestamp(year=year, month=month, day=1),
                    "division": division,
                    "temperature_c": round(temp, 2),
                    "rainfall_mm": round(rain, 1),
                    "ndvi": round(ndvi, 3),
                })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate()
    DATA_PATH.parent.mkdir(exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"Saved {len(df)} rows to {DATA_PATH}")
