#!/usr/bin/env python3
"""
Reducer for Daily Taxi Demand (Assignment Section 8b)
Input (sorted by key thanks to Shuffle & Sort): <day>\t1 repeated per trip
Output: <day>\t<total_trip_count>

Note: Hadoop's default sort is alphabetical, so output order will be
Friday, Monday, Saturday, Sunday, Thursday, Tuesday, Wednesday - NOT
calendar order. Reorder in Excel/pandas when building your report chart.
"""
import sys

current_day = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    day, count = line.split("\t")
    count = int(count)

    if current_day == day:
        current_count += count
    else:
        if current_day is not None:
            print(f"{current_day}\t{current_count}")
        current_day = day
        current_count = count

if current_day is not None:
    print(f"{current_day}\t{current_count}")
