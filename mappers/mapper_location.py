#!/usr/bin/env python3
"""
Mapper for Pickup Location Analysis (Assignment Section 8c)
Input: cleaned CSV lines (from stdin)
Output: <PULocationID>\t1  for every valid trip
"""
import sys

PULOCATION_COL = 7  # 0-indexed position of 'PULocationID' column

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID,"):
        continue

    fields = line.split(",")
    if len(fields) <= PULOCATION_COL:
        continue

    zone = fields[PULOCATION_COL].strip()
    if zone.isdigit():
        print(f"{zone}\t1")
