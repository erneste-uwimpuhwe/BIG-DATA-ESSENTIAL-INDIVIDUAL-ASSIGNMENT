#!/usr/bin/env python3
"""
Mapper for Busiest Pickup-Drop-off Routes (Assignment Section 8g)
Input: cleaned CSV lines (from stdin)
Output: <PULocationID>-<DOLocationID>\t<total_amount>
"""
import sys

PULOCATION_COL = 7
DOLOCATION_COL = 8
TOTAL_COL = 16

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID,"):
        continue

    fields = line.split(",")
    if len(fields) <= TOTAL_COL:
        continue

    pu = fields[PULOCATION_COL].strip()
    do = fields[DOLOCATION_COL].strip()
    if not (pu.isdigit() and do.isdigit()):
        continue

    try:
        total = float(fields[TOTAL_COL])
    except ValueError:
        continue

    route_key = f"{pu}-{do}"
    print(f"{route_key}\t{total}")
