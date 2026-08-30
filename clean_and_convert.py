"""
Big Data Essentials Assignment - Data Cleaning & Conversion
Converts NYC TLC yellow taxi parquet files to cleaned CSV for HDFS ingestion.

Cleaning rules applied (documented for report Section 7 - Data Cleaning):
1. Drop rows with null passenger_count, RatecodeID, or store_and_fwd_flag
2. Drop rows with passenger_count == 0 (invalid - no passenger)
3. Drop rows with trip_distance <= 0 (invalid - no distance travelled)
4. Drop rows with fare_amount <= 0 or total_amount <= 0 (invalid/free trips, refunds)
5. Drop rows with trip duration <= 0 (dropoff before/at pickup - data error)
6. Drop rows with trip duration > 4 hours (14400s) - treated as outlier, flagged not just deleted
7. Drop exact duplicate rows
8. Keep passenger_count up to 6 (standard NYC taxi max); flag >6 as anomaly, don't drop
"""
import pandas as pd
import os

INPUT_DIR = r"C:\taxi_project\raw_parquet"
OUTPUT_DIR = r"C:\taxi_project\cleaned"
os.makedirs(OUTPUT_DIR, exist_ok=True)

months = ["2026-01", "2026-02", "2026-03"]
summary_rows = []

for month in months:
    path = f"{INPUT_DIR}\\yellow_tripdata_{month}.parquet"
    df = pd.read_parquet(path)
    original_count = len(df)

    counts = {"original": original_count}

    df = df.dropna(subset=["passenger_count", "RatecodeID", "store_and_fwd_flag"])
    counts["after_null_drop"] = len(df)

    df = df[df["passenger_count"] > 0]
    counts["after_passenger_filter"] = len(df)

    df = df[df["trip_distance"] > 0]
    counts["after_distance_filter"] = len(df)

    df = df[(df["fare_amount"] > 0) & (df["total_amount"] > 0)]
    counts["after_fare_filter"] = len(df)

    duration_sec = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds()
    df = df[duration_sec > 0]
    duration_sec = duration_sec[duration_sec > 0]
    df = df[duration_sec <= 14400]
    counts["after_duration_filter"] = len(df)

    df = df.drop_duplicates()
    counts["after_dedup"] = len(df)

    df["trip_duration_min"] = (
        (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60
    ).round(2)
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
    df["pickup_dow"] = df["tpep_pickup_datetime"].dt.day_name()
    df["pickup_date"] = df["tpep_pickup_datetime"].dt.date

    final_count = len(df)
    removed = original_count - final_count
    pct_removed = round(removed / original_count * 100, 2)

    out_path = f"{OUTPUT_DIR}\\yellow_tripdata_{month}_cleaned.csv"
    df.to_csv(out_path, index=False)

    summary_rows.append({
        "month": month,
        **counts,
        "final_count": final_count,
        "removed": removed,
        "pct_removed": pct_removed,
    })
    print(f"{month}: {original_count:,} -> {final_count:,} rows "
          f"({removed:,} removed, {pct_removed}%) -> {out_path}")

summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv(f"{OUTPUT_DIR}\\cleaning_summary.csv", index=False)
print("\n=== CLEANING SUMMARY (save this table for your report Section 7) ===")
print(summary_df.to_string(index=False))