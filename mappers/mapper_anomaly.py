#!/usr/bin/env python3
"""
Mapper for Anomaly Detection (Assignment Section 8i)
Input: cleaned CSV lines (from stdin)
Output: <anomaly_type>\t1  for every suspicious record found

Note: our cleaning step (Section 7) already removed the most extreme
invalid records (zero/negative fare, zero distance, etc). This
anomaly detector looks for SUBTLER issues that survived cleaning -
statistically unusual but not technically invalid records, such as:
  - very high fare-per-mile (e.g. short trip, huge fare - possible
    meter tampering or data error)
  - very low fare-per-mile (e.g. long trip, tiny fare - possible
    promo/comp trip or data error)
  - passenger_count > 6 (exceeds standard NYC taxi capacity)
  - very high average speed implied by distance/duration (e.g. >80mph
    sustained - physically implausible in NYC traffic)
  - very short trips with unusually high fare (<0.3 mi but >$20)

A record can trigger multiple flags; we count each flag type
separately so the reducer can report a breakdown by anomaly category.
"""
import sys

DISTANCE_COL = 4
FARE_COL = 10
PASSENGER_COL = 3
DURATION_COL = 20

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID,"):
        continue

    fields = line.split(",")
    if len(fields) <= DURATION_COL:
        continue

    try:
        passenger_count = float(fields[PASSENGER_COL])
        distance = float(fields[DISTANCE_COL])
        fare = float(fields[FARE_COL])
        duration_min = float(fields[DURATION_COL])
    except ValueError:
        continue

    if distance <= 0 or duration_min <= 0:
        continue  # already filtered in cleaning, skip defensively

    fare_per_mile = fare / distance
    speed_mph = (distance / duration_min) * 60

    flags = []

    if fare_per_mile > 50:
        flags.append("high_fare_per_mile")
    if fare_per_mile < 0.5:
        flags.append("low_fare_per_mile")
    if passenger_count > 6:
        flags.append("excess_passengers")
    if speed_mph > 80:
        flags.append("implausible_speed")
    if distance < 0.3 and fare > 20:
        flags.append("short_trip_high_fare")

    for flag in flags:
        print(f"{flag}\t1")

    if flags:
        print("total_flagged_records\t1")
    else:
        print("total_clean_records\t1")
