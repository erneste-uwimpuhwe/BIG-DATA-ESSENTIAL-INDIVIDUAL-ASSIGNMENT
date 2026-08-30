#!/usr/bin/env python3
"""
Reducer for Payment Method Analysis (Assignment Section 8e)
Input (sorted by key): <payment_type>\t<fare>,<tip>,<total>  per trip
Output: <payment_type>\t<trip_count>\t<total_revenue>\t<avg_fare>\t<avg_tip>

Aggregates three running sums (fare, tip, total) plus a count per key,
then computes averages once the key group is complete - same
single-pass streaming pattern as the other reducers, just tracking
more than one running total this time.
"""
import sys

PAYMENT_LABELS = {
    "1": "Credit card",
    "2": "Cash",
    "3": "No charge",
    "4": "Dispute",
    "5": "Unknown",
    "6": "Voided trip",
}

current_key = None
count = 0
sum_fare = 0.0
sum_tip = 0.0
sum_total = 0.0

def flush(key, count, sum_fare, sum_tip, sum_total):
    label = PAYMENT_LABELS.get(key, f"Type {key}")
    avg_fare = sum_fare / count if count else 0
    avg_tip = sum_tip / count if count else 0
    print(f"{key}\t{label}\t{count}\t{sum_total:.2f}\t{avg_fare:.2f}\t{avg_tip:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, values = line.split("\t")
    fare, tip, total = (float(v) for v in values.split(","))

    if current_key == key:
        count += 1
        sum_fare += fare
        sum_tip += tip
        sum_total += total
    else:
        if current_key is not None:
            flush(current_key, count, sum_fare, sum_tip, sum_total)
        current_key = key
        count = 1
        sum_fare = fare
        sum_tip = tip
        sum_total = total

if current_key is not None:
    flush(current_key, count, sum_fare, sum_tip, sum_total)
