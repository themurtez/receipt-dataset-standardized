#!/usr/bin/env python3
"""
Compute missing / unknown field statistics for receipt annotations.

Counts:
- empty strings ""
- placeholder values (YYYY-MM-DD / HH:MM:SS)
- null values
"""

import json
import os
from collections import Counter, defaultdict

ANNOTATIONS_DIR = "annotations"

PLACEHOLDER_DATES = {"YYYY-MM-DD"}
PLACEHOLDER_TIMES = {"HH:MM:SS"}

def is_missing(value):
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return False

def main():
    files = [f for f in os.listdir(ANNOTATIONS_DIR) if f.endswith(".json")]
    total = len(files)

    if total == 0:
        print("No annotation files found.")
        return

    stats = defaultdict(Counter)

    for fname in files:
        path = os.path.join(ANNOTATIONS_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        merchant = data.get("merchant", {})
        transaction = data.get("transaction", {})

        # Merchant fields
        for field in ["name", "address", "phone", "tax_id", "website"]:
            val = merchant.get(field)
            if is_missing(val):
                stats["merchant"][field] += 1

        # Transaction fields
        date = transaction.get("date")
        time = transaction.get("time")

        if is_missing(date) or date in PLACEHOLDER_DATES:
            stats["transaction"]["date"] += 1

        if is_missing(time) or time in PLACEHOLDER_TIMES:
            stats["transaction"]["time"] += 1

        if is_missing(transaction.get("payment_method")):
            stats["transaction"]["payment_method"] += 1

    # Print report
    print(f"Total samples: {total}\n")

    print("Merchant missingness:")
    for field, count in stats["merchant"].items():
        pct = (count / total) * 100
        print(f"  {field:10s}: {count:4d} ({pct:.1f}%)")

    print("\nTransaction missingness:")
    for field, count in stats["transaction"].items():
        pct = (count / total) * 100
        print(f"  {field:14s}: {count:4d} ({pct:.1f}%)")

if __name__ == "__main__":
    main()
