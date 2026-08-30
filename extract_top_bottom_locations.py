"""
Extract Top 10 and Bottom 10 pickup zones from the location analysis
MapReduce output (Assignment Section 8c).

Run this AFTER the Hadoop job finishes and you've downloaded the output
from HDFS to your local machine.

Usage:
    python extract_top_bottom_locations.py <path_to_part_file(s)>

Example:
    python extract_top_bottom_locations.py C:\\taxi_project\\output_local\\location\\part-00000
"""
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_top_bottom_locations.py <part-file-path>")
        sys.exit(1)

    counts = {}
    for path in sys.argv[1:]:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                zone, count = line.split("\t")
                counts[zone] = counts.get(zone, 0) + int(count)

    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    print("=== TOP 10 PICKUP ZONES BY TRIP COUNT ===")
    print(f"{'Rank':<6}{'Zone ID':<10}{'Trip Count':>12}")
    for i, (zone, count) in enumerate(ranked[:10], 1):
        print(f"{i:<6}{zone:<10}{count:>12,}")

    print()
    print("=== BOTTOM 10 PICKUP ZONES BY TRIP COUNT ===")
    print(f"{'Rank':<6}{'Zone ID':<10}{'Trip Count':>12}")
    for i, (zone, count) in enumerate(ranked[-10:][::-1], 1):
        print(f"{i:<6}{zone:<10}{count:>12,}")

    total_zones = len(ranked)
    total_trips = sum(counts.values())
    print(f"\nTotal distinct pickup zones: {total_zones}")
    print(f"Total trips across all zones: {total_trips:,}")

if __name__ == "__main__":
    main()
