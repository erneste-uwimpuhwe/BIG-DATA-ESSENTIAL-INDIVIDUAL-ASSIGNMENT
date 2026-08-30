#!/usr/bin/env python3
"""
Reducer for Revenue by Pickup Location (Assignment Section 8d)
Also serves as Job 1 of the compulsory Multi-Stage MapReduce (Section 9) -
its HDFS output is consumed directly by Job 2 (top10_revenue_job2.py mapper/reducer).

Input (sorted by key): <PULocationID>\t<fare>,<tip>,<total>,<distance>  per trip
Output: <PULocationID>\t<trip_count>\t<total_fare>\t<total_tip>\t<total_revenue>\t<avg_fare>\t<avg_distance>
"""
import sys

current_key = None
count = 0
sum_fare = 0.0
sum_tip = 0.0
sum_total = 0.0
sum_distance = 0.0

def flush(key, count, sum_fare, sum_tip, sum_total, sum_distance):
    avg_fare = sum_fare / count if count else 0
    avg_distance = sum_distance / count if count else 0
    print(f"{key}\t{count}\t{sum_fare:.2f}\t{sum_tip:.2f}\t{sum_total:.2f}\t{avg_fare:.2f}\t{avg_distance:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, values = line.split("\t")
    fare, tip, total, distance = (float(v) for v in values.split(","))

    if current_key == key:
        count += 1
        sum_fare += fare
        sum_tip += tip
        sum_total += total
        sum_distance += distance
    else:
        if current_key is not None:
            flush(current_key, count, sum_fare, sum_tip, sum_total, sum_distance)
        current_key = key
        count = 1
        sum_fare = fare
        sum_tip = tip
        sum_total = total
        sum_distance = distance

if current_key is not None:
    flush(current_key, count, sum_fare, sum_tip, sum_total, sum_distance)
