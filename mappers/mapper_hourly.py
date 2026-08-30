#!/usr/bin/env python3
"""
Mapper for Hourly Taxi Demand (Assignment Section 8a)
Input: cleaned CSV lines (from stdin, fed by Hadoop Streaming)
Output: <hour>\t1  for every valid trip

IMPORTANT: our cleaned CSVs (~300-400MB each) get split into multiple
InputSplits by Hadoop (default block size 128MB), so only ONE split per
file actually starts with the header row. We therefore use FIXED column
positions (based on the known cleaned-CSV schema) instead of reading the
header dynamically, and skip any header row wherever it appears by
matching the literal text "VendorID," which never occurs in real data.
"""
import sys

PICKUP_HOUR_COL = 21  # 0-indexed position of 'pickup_hour' column

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID,"):
        continue  # skip blank lines and any header row

    fields = line.split(",")
    if len(fields) <= PICKUP_HOUR_COL:
        continue  # malformed row, skip

    hour = fields[PICKUP_HOUR_COL].strip()
    if hour.isdigit():
        print(f"{hour}\t1")
