#!/usr/bin/env python3
"""
Reducer for Busiest Pickup-Drop-off Routes (Assignment Section 8g)
Input (sorted by key): <PULocationID-DOLocationID>\t<total_amount>  per trip
Output: <route>\t<trip_count>\t<total_revenue>

After running, use extract_top_routes.py to get Top 20 by trip count
AND Top 20 by revenue separately (two different rankings), as required
by the assignment.
"""
import sys

current_key = None
count = 0
sum_total = 0.0

def flush(key, count, sum_total):
    print(f"{key}\t{count}\t{sum_total:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, total = line.split("\t")
    total = float(total)

    if current_key == key:
        count += 1
        sum_total += total
    else:
        if current_key is not None:
            flush(current_key, count, sum_total)
        current_key = key
        count = 1
        sum_total = total

if current_key is not None:
    flush(current_key, count, sum_total)
