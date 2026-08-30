#!/usr/bin/env python3
"""
JOB 2 Reducer - Multi-Stage MapReduce, Stage 2 (Assignment Section 9 - Compulsory)

Since every record from the mapper carries the same key "ALL", this
single reducer instance receives every zone's revenue total and can
therefore sort ALL of them together and output the true Top 10 -
something a single reducer call normally can't do across different
keys in one-stage MapReduce. This is the whole point of the two-stage
design: Job 1 aggregates per zone (parallel, many reducers possible),
Job 2 ranks globally (necessarily a single reducer / single point of
comparison).

Output: rank\tPULocationID\ttotal_revenue  (top 10 only)
"""
import sys

records = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, value = line.split("\t")
    zone, revenue = value.split(",")
    records.append((zone, float(revenue)))

records.sort(key=lambda x: x[1], reverse=True)

for rank, (zone, revenue) in enumerate(records[:10], 1):
    print(f"{rank}\t{zone}\t{revenue:.2f}")
