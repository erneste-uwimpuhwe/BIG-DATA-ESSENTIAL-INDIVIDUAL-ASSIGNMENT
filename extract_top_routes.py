"""
Extract Top 20 routes by TRIP COUNT and Top 20 by REVENUE from the
route analysis MapReduce output (Assignment Section 8g).

Run this AFTER downloading the Hadoop job output to your local machine.

Usage:
    python extract_top_routes.py <path_to_part_file>
"""
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_top_routes.py <part-file-path>")
        sys.exit(1)

    routes = []  # (route, count, revenue)
    for path in sys.argv[1:]:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                route, count, revenue = line.split("\t")
                routes.append((route, int(count), float(revenue)))

    print("=== TOP 20 ROUTES BY TRIP COUNT ===")
    print(f"{'Rank':<6}{'Route (PU-DO)':<20}{'Trip Count':>12}{'Revenue':>15}")
    by_count = sorted(routes, key=lambda x: x[1], reverse=True)
    for i, (route, count, revenue) in enumerate(by_count[:20], 1):
        print(f"{i:<6}{route:<20}{count:>12,}{revenue:>15,.2f}")

    print()
    print("=== TOP 20 ROUTES BY REVENUE ===")
    print(f"{'Rank':<6}{'Route (PU-DO)':<20}{'Trip Count':>12}{'Revenue':>15}")
    by_revenue = sorted(routes, key=lambda x: x[2], reverse=True)
    for i, (route, count, revenue) in enumerate(by_revenue[:20], 1):
        print(f"{i:<6}{route:<20}{count:>12,}{revenue:>15,.2f}")

    top_count_set = {r[0] for r in by_count[:20]}
    top_revenue_set = {r[0] for r in by_revenue[:20]}
    overlap = top_count_set & top_revenue_set
    print(f"\nRoutes appearing in BOTH top-20-by-count and top-20-by-revenue: {len(overlap)} of 20")
    print("(This directly answers Business Question (i): are the most frequent routes also the most profitable?)")

if __name__ == "__main__":
    main()
