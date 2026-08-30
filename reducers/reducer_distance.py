#!/usr/bin/env python3
"""
Reducer for Distance-Based Fare Analysis (Assignment Section 8f)
Input (sorted by key): <bucket>\t<fare>,<total>,<distance>  per trip
Output: <bucket>\t<trip_count>\t<avg_fare>\t<avg_total>\t<avg_distance>

Note: Hadoop's default alphabetical sort will order buckets as:
0-2, 10-20, 2-5, 20+, 5-10 (NOT numeric/logical order) - reorder in
Excel/pandas for your report chart.
"""
import sys

current_key = None
count = 0
sum_fare = 0.0
sum_total = 0.0
sum_distance = 0.0

def flush(key, count, sum_fare, sum_total, sum_distance):
    avg_fare = sum_fare / count if count else 0
    avg_total = sum_total / count if count else 0
    avg_distance = sum_distance / count if count else 0
    print(f"{key}\t{count}\t{avg_fare:.2f}\t{avg_total:.2f}\t{avg_distance:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, values = line.split("\t")
    fare, total, distance = (float(v) for v in values.split(","))

    if current_key == key:
        count += 1
        sum_fare += fare
        sum_total += total
        sum_distance += distance
    else:
        if current_key is not None:
            flush(current_key, count, sum_fare, sum_total, sum_distance)
        current_key = key
        count = 1
        sum_fare = fare
        sum_total = total
        sum_distance = distance

if current_key is not None:
    flush(current_key, count, sum_fare, sum_total, sum_distance)
