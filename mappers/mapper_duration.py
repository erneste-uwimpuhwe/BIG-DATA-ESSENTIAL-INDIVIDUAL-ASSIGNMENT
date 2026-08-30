#!/usr/bin/env python3
"""
Mapper for Trip Duration Analysis (Assignment Section 8h)
Input: cleaned CSV lines (from stdin)
Output: <duration_bucket>\t<fare_amount>,<trip_distance>,<tip_amount>

Duration buckets (minutes): 0-5, 5-10, 10-20, 20-30, 30-60, 60+
"""
import sys

DURATION_COL = 20
FARE_COL = 10
DISTANCE_COL = 4
TIP_COL = 13

def bucket_for(minutes):
    if minutes <= 5:
        return "0-5"
    elif minutes <= 10:
        return "5-10"
    elif minutes <= 20:
        return "10-20"
    elif minutes <= 30:
        return "20-30"
    elif minutes <= 60:
        return "30-60"
    else:
        return "60+"

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID,"):
        continue

    fields = line.split(",")
    if len(fields) <= DURATION_COL:
        continue

    try:
        duration = float(fields[DURATION_COL])
        fare = float(fields[FARE_COL])
        distance = float(fields[DISTANCE_COL])
        tip = float(fields[TIP_COL])
    except ValueError:
        continue

    if duration <= 0:
        continue

    bucket = bucket_for(duration)
    print(f"{bucket}\t{fare},{distance},{tip}")
