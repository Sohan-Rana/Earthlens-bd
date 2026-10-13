import calendar
import time

import pandas as pd
import requests

from .config import DIVISION_COORDS
from .logger import get_logger

log = get_logger(__name__)

API_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"
MISSING = -999


def _get_with_retry(params: dict, attempts: int = 3) -> requests.Response:
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(API_URL, params=params, timeout=60)
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            log.warning("Attempt %d failed: %s", attempt, exc)
            if attempt == attempts:
                raise
            time.sleep(2 * attempt)


def fetch_point(lat: float, lon: float, start: int, end: int) -> pd.DataFrame:
    params = {
        "parameters": "T2M,PRECTOTCORR",
        "community": "AG",
        "latitude": lat,
        "longitude": lon,
        "start": start,
        "end": end,
        "format": "JSON",
    }
    response = _get_with_retry(params)
    data = response.json()["properties"]["parameter"]

    rows = []
    for key, temp in data["T2M"].items():
        year, month = int(key[:4]), int(key[4:])
        if month > 12:  # month 13 is the annual summary
            continue
        rain_per_day = data["PRECTOTCORR"][key]
        if temp == MISSING or rain_per_day == MISSING:
            continue
        days = calendar.monthrange(year, month)[1]
        rows.append({
            "date": pd.Timestamp(year=year, month=month, day=1),
            "temperature_c": round(temp, 2),
            "rainfall_mm": round(rain_per_day * days, 1),
        })
    return pd.DataFrame(rows)


def fetch_all(start: int, end: int) -> pd.DataFrame:
    frames = []
    for division, (lat, lon) in DIVISION_COORDS.items():
        log.info("Fetching NASA POWER data for %s", division)
        frame = fetch_point(lat, lon, start, end)
        frame.insert(1, "division", division)
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)
