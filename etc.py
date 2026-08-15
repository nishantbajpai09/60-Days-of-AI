"""
etl.py — Road Accident Insight Explorer
Cleans the raw UK STATS19 collision CSV into an analysis-ready Parquet file.

Run this once (or whenever accidents_raw.csv changes):
    python etl.py
"""

import pandas as pd
import os

RAW_PATH = "accidents_raw.csv"
OUTPUT_DIR = "data"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "accidents_clean.parquet")

# --- Official STATS19 code lookups (from DfT data guide) ---

SEVERITY_MAP = {
    1: "Fatal",
    2: "Serious",
    3: "Slight",
}

WEATHER_MAP = {
    1: "Fine, no high winds",
    2: "Raining, no high winds",
    3: "Snowing, no high winds",
    4: "Fine + high winds",
    5: "Raining + high winds",
    6: "Snowing + high winds",
    7: "Fog or mist",
    8: "Other",
    9: "Unknown",
    -1: "Data missing",
}

LIGHT_MAP = {
    1: "Daylight",
    4: "Darkness - lights lit",
    5: "Darkness - lights unlit",
    6: "Darkness - no lighting",
    7: "Darkness - lighting unknown",
    -1: "Data missing",
}

ROAD_SURFACE_MAP = {
    1: "Dry",
    2: "Wet or damp",
    3: "Snow",
    4: "Frost or ice",
    5: "Flood over 3cm deep",
    6: "Oil or diesel",
    7: "Mud",
    -1: "Data missing",
}

DAY_MAP = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    7: "Saturday",
}


def load_raw(path: str) -> pd.DataFrame:
    print(f"Reading {path} ...")
    df = pd.read_csv(path, low_memory=False)
    print(f"  Loaded {len(df):,} raw rows, {len(df.columns)} columns")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    start_count = len(df)

    # Normalise column names (some yearly files vary slightly in casing)
    df.columns = [c.strip().lower() for c in df.columns]

    required = [
        "accident_severity", "latitude", "longitude", "date", "time",
        "weather_conditions", "light_conditions", "road_surface_conditions",
        "day_of_week", "number_of_casualties", "number_of_vehicles",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Expected columns missing from raw CSV: {missing}. "
            "Check that this is a STATS19 collision-level file."
        )

    # Drop rows with missing/invalid coordinates — can't map them
    df = df.dropna(subset=["latitude", "longitude"])
    df = df[(df["latitude"] != -1) & (df["longitude"] != -1)]

    # Decode coded fields into readable labels
    df["accident_severity"] = df["accident_severity"].map(SEVERITY_MAP).fillna("Unknown")
    df["weather_conditions"] = df["weather_conditions"].map(WEATHER_MAP).fillna("Unknown")
    df["light_conditions"] = df["light_conditions"].map(LIGHT_MAP).fillna("Unknown")
    df["road_surface_conditions"] = df["road_surface_conditions"].map(ROAD_SURFACE_MAP).fillna("Unknown")
    df["day_of_week"] = df["day_of_week"].map(DAY_MAP).fillna("Unknown")

    # Parse date + time, derive hour/month/year fields
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date"])

    df["time"] = df["time"].astype(str).str.strip()
    df["hour"] = pd.to_datetime(df["time"], format="%H:%M", errors="coerce").dt.hour
    df["hour"] = df["hour"].fillna(-1).astype(int)

    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")
    df["year"] = df["date"].dt.year

    # Keep only the columns the app actually needs — smaller, faster file
    keep_cols = [
        "accident_severity", "latitude", "longitude", "date", "hour",
        "day_of_week", "month", "month_name", "year",
        "weather_conditions", "light_conditions", "road_surface_conditions",
        "number_of_casualties", "number_of_vehicles",
    ]
    df = df[keep_cols].reset_index(drop=True)

    end_count = len(df)
    retention = (end_count / start_count) * 100 if start_count else 0
    print(f"  Retained {end_count:,} / {start_count:,} rows ({retention:.2f}%)")
    print(f"  Nulls remaining: {int(df.isnull().sum().sum())}")

    return df


def main():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(
            f"'{RAW_PATH}' not found. Place the downloaded STATS19 collision "
            f"CSV in this folder and name it '{RAW_PATH}'."
        )

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    raw = load_raw(RAW_PATH)
    cleaned = clean(raw)
    cleaned.to_parquet(OUTPUT_PATH, index=False)

    print(f"\nDone. Clean dataset saved to: {OUTPUT_PATH}")
    print(f"Final shape: {cleaned.shape[0]:,} rows x {cleaned.shape[1]} columns")


if __name__ == "__main__":
    main()
