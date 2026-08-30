"""
Performance Comparison: Python/Pandas vs Hadoop MapReduce
(Assignment Section 12 - Compulsory)

Runs the SAME analysis as mapper_hourly.py / reducer_hourly.py (hourly
trip demand) using plain Pandas, and reports timing + memory so you can
build the comparison table required by the assignment.

Run this on Windows with your cleaned CSVs:
    python performance_comparison.py
"""
import pandas as pd
import time
import os
import psutil

INPUT_DIR = r"C:\taxi_project\cleaned"
FILES = [
    "yellow_tripdata_2026-01_cleaned.csv",
    "yellow_tripdata_2026-02_cleaned.csv",
    "yellow_tripdata_2026-03_cleaned.csv",
]

process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / (1024 ** 2)  # MB

start = time.time()

total_size_bytes = 0
total_records = 0
hourly_counts = pd.Series(dtype=int)

for fname in FILES:
    path = os.path.join(INPUT_DIR, fname)
    total_size_bytes += os.path.getsize(path)
    df = pd.read_csv(path, usecols=["pickup_hour"])
    total_records += len(df)
    counts = df["pickup_hour"].value_counts()
    hourly_counts = hourly_counts.add(counts, fill_value=0)

hourly_counts = hourly_counts.astype(int).sort_index()

end = time.time()
mem_after = process.memory_info().rss / (1024 ** 2)  # MB

elapsed = end - start
total_size_mb = total_size_bytes / (1024 ** 2)

print("=== HOURLY DEMAND RESULTS (Pandas) ===")
print(hourly_counts.to_string())

print()
print("=== PERFORMANCE METRICS (for Section 12 comparison table) ===")
print(f"Dataset size:        {total_size_mb:,.1f} MB")
print(f"Number of records:   {total_records:,}")
print(f"Execution time:      {elapsed:.2f} seconds")
print(f"Memory used (delta): {mem_after - mem_before:.1f} MB")
print(f"Peak process memory: {mem_after:.1f} MB")
print()
print("Compare these numbers against your Hadoop job's YARN application")
print("page (Section 11) for: execution time (StartTime->FinishTime),")
print("mapper/reducer task counts, and output size (hdfs dfs -du -h).")
