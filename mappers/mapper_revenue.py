#!/usr/bin/env python3
"""
Mapper for Revenue by Pickup Location (Assignment Section 8d)
Also serves as Job 1 of the compulsory Multi-Stage MapReduce (Section 9).
Input: cleaned CSV lines (from stdin)
Output: <PULocationID>\t<fare_amount>,<tip_amount>,<total_amount>,<trip_distance>
"""
import sys

PULOCATION_COL = 7
FARE_COL = 10
TIP_COL = 13
TOTAL_COL = 16
DISTANCE_COL = 4

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID,"):
        continue

    fields = line.split(",")
    if len(fields) <= TOTAL_COL:
        continue

    zone = fields[PULOCATION_COL].strip()
    if not zone.isdigit():
        continue

    try:
        fare = float(fields[FARE_COL])
        tip = float(fields[TIP_COL])
        total = float(fields[TOTAL_COL])
        distance = float(fields[DISTANCE_COL])
    except ValueError:
        continue

    print(f"{zone}\t{fare},{tip},{total},{distance}")
