#!/usr/bin/env python3
"""
Reducer for Trip Duration Analysis (Assignment Section 8h)
Input (sorted by key): <bucket>\t<fare>,<distance>,<tip>  per trip
Output: <bucket>\t<trip_count>\t<avg_fare>\t<avg_distance>\t<avg_tip>
"""
import sys

current_key = None
count = 0
sum_fare = 0.0
sum_distance = 0.0
sum_tip = 0.0

def flush(key, count, sum_fare, sum_distance, sum_tip):
    avg_fare = sum_fare / count if count else 0
    avg_distance = sum_distance / count if count else 0
    avg_tip = sum_tip / count if count else 0
    print(f"{key}\t{count}\t{avg_fare:.2f}\t{avg_distance:.2f}\t{avg_tip:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, values = line.split("\t")
    fare, distance, tip = (float(v) for v in values.split(","))

    if current_key == key:
        count += 1
        sum_fare += fare
        sum_distance += distance
        sum_tip += tip
    else:
        if current_key is not None:
            flush(current_key, count, sum_fare, sum_distance, sum_tip)
        current_key = key
        count = 1
        sum_fare = fare
        sum_distance = distance
        sum_tip = tip

if current_key is not None:
    flush(current_key, count, sum_fare, sum_distance, sum_tip)
