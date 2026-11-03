"""Fit host patching into a maintenance window, reboot hosts first.

Usage: python3 main.py hosts.csv --window-minutes 120
CSV columns: host,critical_patches,reboot_required (yes/no)
Each host costs 5 minutes plus 2 minutes per critical patch. Hosts
needing a reboot go first; hosts that do not fit are listed as overflow.
"""
import argparse, csv, sys


def plan(rows, window_minutes):
    def cost(row):
        return 5 + 2 * int(row["critical_patches"])

    ordered = sorted(rows, key=lambda r: (r["reboot_required"].strip().lower() != "yes", -int(r["critical_patches"])))
    scheduled, overflow, used = [], [], 0
    for row in ordered:
        if used + cost(row) <= window_minutes:
            scheduled.append(row["host"])
            used += cost(row)
        else:
            overflow.append(row["host"])
    return scheduled, overflow, used


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--window-minutes", type=int, default=120)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        scheduled, overflow, used = plan(list(csv.DictReader(f)), args.window_minutes)
    print(f"Scheduled ({used} min): {', '.join(scheduled) if scheduled else 'none'}")
    print(f"Overflow: {', '.join(overflow) if overflow else 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
