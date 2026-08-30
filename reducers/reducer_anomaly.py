#!/usr/bin/env python3
"""
Reducer for Anomaly Detection (Assignment Section 8i)
Input (sorted by key): <anomaly_type>\t1  repeated
Output: <anomaly_type>\t<count>

Note: total_flagged_records is NOT the sum of the individual flag
categories, since one record can trigger more than one flag - it's
counted once per record as a distinct key, giving the true number of
records with at least one issue (needed for the "percentage of
records with potential anomalies" business question).
"""
import sys

current_key = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, count = line.split("\t")
    count = int(count)

    if current_key == key:
        current_count += count
    else:
        if current_key is not None:
            print(f"{current_key}\t{current_count}")
        current_key = key
        current_count = count

if current_key is not None:
    print(f"{current_key}\t{current_count}")
