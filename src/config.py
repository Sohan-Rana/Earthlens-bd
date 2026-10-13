from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "climate_data.csv"
REAL_DATA_PATH = ROOT / "data" / "climate_data_real.csv"
ASSETS_DIR = ROOT / "assets"

DIVISIONS = [
    "Dhaka", "Chattogram", "Rajshahi", "Khulna",
    "Barishal", "Sylhet", "Rangpur", "Mymensingh",
]
START_YEAR, END_YEAR = 2000, 2023

DIVISION_COORDS = {
    "Dhaka": (23.81, 90.41),
    "Chattogram": (22.36, 91.78),
    "Rajshahi": (24.37, 88.60),
    "Khulna": (22.82, 89.55),
    "Barishal": (22.70, 90.37),
    "Sylhet": (24.90, 91.87),
    "Rangpur": (25.74, 89.28),
    "Mymensingh": (24.75, 90.40),
}

METRIC_LABELS = {
    "temperature": "Temperature (°C)",
    "rainfall": "Rainfall (mm)",
    "ndvi": "NDVI",
}
