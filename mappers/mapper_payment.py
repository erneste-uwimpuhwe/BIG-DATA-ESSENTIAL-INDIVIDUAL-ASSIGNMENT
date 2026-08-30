#!/usr/bin/env python3
"""
Mapper for Payment Method Analysis (Assignment Section 8e)
Input: cleaned CSV lines (from stdin)
Output: <payment_type>\t<fare_amount>,<tip_amount>,<total_amount>

payment_type codes (per TLC data dictionary):
1=Credit card, 2=Cash, 3=No charge, 4=Dispute, 5=Unknown, 6=Voided trip
We pass the raw code through; human-readable labels are applied later
in the reducer output stage / report, since mapping happens once not
per-record (keeps the mapper fast).
"""
import sys

PAYMENT_COL = 9
FARE_COL = 10
TIP_COL = 13
TOTAL_COL = 16

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID,"):
        continue

    fields = line.split(",")
    if len(fields) <= TOTAL_COL:
        continue

    payment_type = fields[PAYMENT_COL].strip()
    if not payment_type.isdigit():
        continue

    try:
        fare = float(fields[FARE_COL])
        tip = float(fields[TIP_COL])
        total = float(fields[TOTAL_COL])
    except ValueError:
        continue

    print(f"{payment_type}\t{fare},{tip},{total}")
