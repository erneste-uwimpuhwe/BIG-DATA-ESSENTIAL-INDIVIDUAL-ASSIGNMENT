#!/usr/bin/env python3
"""
Mapper for Daily Taxi Demand (Assignment Section 8b)
Input: cleaned CSV lines (from stdin)
Output: <day_of_week>\t1  for every valid trip

Uses fixed column position (pickup_dow, index 22) - same safe approach
as mapper_hourly.py, since large files are split across multiple mappers
and only one split per file contains the header row.
"""
import sys

PICKUP_DOW_COL = 22  # 0-indexed position of 'pickup_dow' column

VALID_DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID,"):
        continue  # skip blank lines and any header row

    fields = line.split(",")
    if len(fields) <= PICKUP_DOW_COL:
        continue  # malformed row, skip

    day = fields[PICKUP_DOW_COL].strip()
    if day in VALID_DAYS:
        print(f"{day}\t1")
