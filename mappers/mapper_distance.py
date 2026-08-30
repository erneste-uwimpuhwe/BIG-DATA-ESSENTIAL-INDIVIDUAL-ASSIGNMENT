#!/usr/bin/env python3
"""
Mapper for Distance-Based Fare Analysis (Assignment Section 8f)
Input: cleaned CSV lines (from stdin)
Output: <distance_bucket>\t<fare_amount>,<total_amount>,<trip_distance>

Buckets: 0-2, 2-5, 5-10, 10-20, 20+ miles (as specified in the assignment)
"""
import sys

DISTANCE_COL = 4
FARE_COL = 10
TOTAL_COL = 16

def bucket_for(distance):
    if distance <= 2:
        return "0-2"
    elif distance <= 5:
        return "2-5"
    elif distance <= 10:
        return "5-10"
    elif distance <= 20:
        return "10-20"
    else:
        return "20+"

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID,"):
        continue

    fields = line.split(",")
    if len(fields) <= TOTAL_COL:
        continue

    try:
        distance = float(fields[DISTANCE_COL])
        fare = float(fields[FARE_COL])
        total = float(fields[TOTAL_COL])
    except ValueError:
        continue

    if distance <= 0:
        continue

    bucket = bucket_for(distance)
    print(f"{bucket}\t{fare},{total},{distance}")
