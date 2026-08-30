#!/usr/bin/env python3
"""
Reducer for Pickup Location Analysis (Assignment Section 8c)
Input (sorted by key): <PULocationID>\t1 repeated per trip
Output: <PULocationID>\t<total_trip_count>

Note: output is sorted by PULocationID (as text), NOT by trip count.
Use extract_top_bottom_locations.py afterward to get Top 10 / Bottom 10.
"""
import sys

current_zone = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    zone, count = line.split("\t")
    count = int(count)

    if current_zone == zone:
        current_count += count
    else:
        if current_zone is not None:
            print(f"{current_zone}\t{current_count}")
        current_zone = zone
        current_count = count

if current_zone is not None:
    print(f"{current_zone}\t{current_count}")
