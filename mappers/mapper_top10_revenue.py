#!/usr/bin/env python3
"""
JOB 2 Mapper - Multi-Stage MapReduce, Stage 2 (Assignment Section 9 - Compulsory)

This job reads Job 1's HDFS OUTPUT directly (not the raw cleaned CSV) -
that is: /taxi_project/output/revenue/part-00000, which contains lines like:
    <PULocationID>\t<trip_count>\t<total_fare>\t<total_tip>\t<total_revenue>\t<avg_fare>\t<avg_distance>

We re-key every record to a single constant key "ALL" so that every
zone's revenue total lands in ONE reducer, which can then hold all
zones in memory and sort them to find the true Top 10. This is the
standard "funnel everything to one reducer" pattern for global top-N
in MapReduce, since a normal reducer only sees one key group at a time
and can't compare across different pickup zones otherwise.

Output: ALL\t<PULocationID>,<total_revenue>
"""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split("\t")
    if len(fields) < 5:
        continue  # malformed row from Job 1's output, skip

    zone = fields[0]
    total_revenue = fields[4]  # 5th column = total_revenue from Job 1's reducer

    try:
        float(total_revenue)
    except ValueError:
        continue

    print(f"ALL\t{zone},{total_revenue}")
