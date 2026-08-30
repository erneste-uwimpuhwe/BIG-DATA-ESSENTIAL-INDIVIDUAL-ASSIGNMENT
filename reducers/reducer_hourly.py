#!/usr/bin/env python3
"""
Reducer for Hourly Taxi Demand (Assignment Section 8a)
Input (from stdin, sorted by key thanks to Hadoop's Shuffle & Sort stage):
    <hour>\t1
    <hour>\t1
    ...
Output: <hour>\t<total_trip_count>

Because Hadoop guarantees all lines with the same key arrive consecutively
after Shuffle & Sort, we can sum with a single running total per key and
flush it to output as soon as the key changes - no need to hold all data
in memory.
"""
import sys

current_hour = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    hour, count = line.split("\t")
    count = int(count)

    if current_hour == hour:
        current_count += count
    else:
        if current_hour is not None:
            print(f"{current_hour}\t{current_count}")
        current_hour = hour
        current_count = count

# flush the last group
if current_hour is not None:
    print(f"{current_hour}\t{current_count}")
