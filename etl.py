"""
Data cleaning pipeline.

Reads the raw DfT STATS19 collision CSV (accidents_raw.csv) and writes a
cleaned, analysis-ready parquet file to data/accidents_clean.parquet.

Source data:
    https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data
    (Open Government Licence v3.0)

Usage:
    python etl.py
"""
import pandas as pd

RAW_PATH = "accidents_raw.csv"
OUT_PATH = "data/accidents_clean.parquet"

SEVERITY_MAP = {1: "Fatal", 2: "Serious", 3: "Slight"}
DOW_MAP = {1: "Sunday", 2: "Monday", 3: "Tuesday", 4: "Wednesday",
           5: "Thursday", 6: "Friday", 7: "Saturday"}
WEATHER_MAP = {
    1: "Fine", 2: "Raining", 3: "Snowing", 4: "Fine + high winds",
    5: "Raining + high winds", 6: "Snowing + high winds",
    7: "Fog or mist", 8: "Other", 9: "Unknown",
}
AREA_MAP = {1: "Urban", 2: "Rural", 3: "Unallocated"}


def main():
    df = pd.read_csv(RAW_PATH, low_memory=False)

    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
    df["hour"] = pd.to_numeric(df["time"].astype(str).str.split(":").str[0], errors="coerce")

    df["severity"] = df["collision_severity"].map(SEVERITY_MAP)
    df["day_of_week_name"] = df["day_of_week"].map(DOW_MAP)
    df["weather"] = df["weather_conditions"].map(WEATHER_MAP)
    df["area"] = df["urban_or_rural_area"].map(AREA_MAP)

    keep_cols = [
        "latitude", "longitude", "date", "hour", "day_of_week_name",
        "severity", "weather", "area", "number_of_vehicles",
        "number_of_casualties", "speed_limit", "police_force",
    ]
    df = df[keep_cols].dropna(subset=[
        "latitude", "longitude", "date", "hour", "severity", "weather", "area"
    ])
    df = df[df["latitude"] != 0]

    df.to_parquet(OUT_PATH, index=False)
    print(f"Wrote {len(df):,} cleaned rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
