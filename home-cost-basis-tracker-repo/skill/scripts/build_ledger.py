#!/usr/bin/env python3
"""
Home Cost Basis Ledger Builder

Parses Amex-style and Chase-style transaction CSV exports, identifies
home-related spending, classifies it as Capital Improvement / Repair &
Maintenance / Excluded (personal property) / Needs Review per IRS Pub 523
guidance, and appends new, non-duplicate rows to a persistent ledger CSV.

Usage:
    python build_ledger.py --amex path/to/amex.csv --chase path/to/chase.csv \
        --ledger path/to/home_cost_basis_ledger.csv

Either --amex or --chase (or both) may be omitted if only one source has new data.
If --ledger points to an existing file, new rows are appended and duplicates
(matched on Date + normalized Description + Amount) are skipped automatically.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

CAPITAL_IMPROVEMENT = [
    "home depot", "lowes", "lowe's", "bedrosians tile", "best tile",
    "marble botanics", "build.com", "kohler co",
    "garage door specialist", "legrand", "solutions electr", "alternative power",
    "polylok", "concrete exchange", "visual comfort",
]

REPAIR_MAINTENANCE = [
    "leaf&limb", "leaf & limb", "nature first landsc", "logans garden shop",
    "atlantic gardening", "perennial border", "botanical interests",
    "east fork", "vego garden", "bloomers flower farm", "triangle pest",
    "cleardefense", "caravan rugs cleaning", "burke brothers hardware",
    "prism paint", "pinks windows",
]

EXCLUDED_PERSONAL_PROPERTY = [
    "crate and barrel", "williams-sonoma", "wayfair", "saatva", "nordic knots",
    "twopagescurtains", "meg brown home furni", "container store",
    "mahoneswallpaper", "pepper home", "coley home", "kassatex",
    "fine*gardening", "restoration hardware",
]

NEEDS_REVIEW_HINTS = ["rejuvenation"]

KEYWORD_CAPITAL = [
    "tile", "granite", "marble", "countertop", "cabinet", "hvac", "roofing",
    "roof", "window", "garage door", "plumb", "solar", "septic", "flooring",
    "hardwood", "remodel", "renovat", "construct", "contractor", "deck",
    "patio", "insulation", "drywall",
]
KEYWORD_REPAIR = [
    "pest", "lawn", "landscap", "garden", "clean", "paint", "handyman",
]
KEYWORD_EXCLUDE = [
    "furniture", "rug", "curtain", "decor", "pottery barn",
]

HOME_HINT_KEYWORDS = KEYWORD_CAPITAL + KEYWORD_REPAIR + KEYWORD_EXCLUDE + \
    CAPITAL_IMPROVEMENT + REPAIR_MAINTENANCE + EXCLUDED_PERSONAL_PROPERTY + NEEDS_REVIEW_HINTS

LEDGER_FIELDS = [
    "Date", "Source", "Vendor (raw)", "Amount", "Classification",
    "Project/Category", "Confirmed by Samantha", "Notes",
]


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


def classify(vendor_raw, category_hint=None):
    v = norm(vendor_raw)
    for kw in CAPITAL_IMPROVEMENT:
        if kw in v:
            return "Capital Improvement"
    for kw in REPAIR_MAINTENANCE:
        if kw in v:
            return "Repair/Maintenance (excluded)"
    for kw in EXCLUDED_PERSONAL_PROPERTY:
        if kw in v:
            return "Excluded - Personal Property"
    for kw in NEEDS_REVIEW_HINTS:
        if kw in v:
            return "Needs Review"
    for kw in KEYWORD_CAPITAL:
        if kw in v:
            return "Needs Review"  # keyword-only match, not vendor-confirmed -> review
    for kw in KEYWORD_REPAIR:
        if kw in v:
            return "Needs Review"
    for kw in KEYWORD_EXCLUDE:
        if kw in v:
            return "Needs Review"
    if category_hint and norm(category_hint) == "home":
        return "Needs Review"
    return None  # not home-related at all -> skip entirely


def looks_home_related(vendor_raw, category_hint=None):
    v = norm(vendor_raw)
    if category_hint and norm(category_hint) == "home":
        return True
    return any(kw in v for kw in HOME_HINT_KEYWORDS)


def parse_amex(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            desc = r.get("Description", "")
            amt_raw = r.get("Amount", "0").strip()
            try:
                amt = float(amt_raw)
            except ValueError:
                continue
            # Amex exports charges as positive, credits/payments as negative.
            if amt <= 0:
                continue
            if not looks_home_related(desc):
                continue
            rows.append({
                "Date": r.get("Date", "").strip(),
                "Source": "Amex",
                "Vendor (raw)": re.sub(r"\s+", " ", desc).strip(),
                "Amount": f"{amt:.2f}",
                "Classification": classify(desc),
            })
    return rows


def parse_chase(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            desc = r.get("Description", "")
            category = r.get("Category", "")
            txn_type = r.get("Type", "")
            amt_raw = r.get("Amount", "0").strip()
            try:
                amt = float(amt_raw)
            except ValueError:
                continue
            if txn_type.strip().lower() == "return":
                continue  # returns handled as informational, not netted automatically
            if amt >= 0:
                continue  # Chase shows charges as negative
            amt = abs(amt)
            if not looks_home_related(desc, category):
                continue
            rows.append({
                "Date": r.get("Transaction Date", "").strip(),
                "Source": "Chase",
                "Vendor (raw)": re.sub(r"\s+", " ", desc).strip(),
                "Amount": f"{amt:.2f}",
                "Classification": classify(desc, category),
            })
    return rows


def dedup_key(row):
    return (row["Date"], norm(row["Vendor (raw)"]), row["Amount"])


def load_existing_ledger(path):
    existing = []
    keys = set()
    if path.exists():
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing.append(r)
                keys.add((r.get("Date", ""), norm(r.get("Vendor (raw)", "")), r.get("Amount", "")))
    return existing, keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--amex")
    ap.add_argument("--chase")
    ap.add_argument("--ledger", required=True)
    args = ap.parse_args()

    ledger_path = Path(args.ledger)
    existing_rows, existing_keys = load_existing_ledger(ledger_path)

    new_candidates = []
    if args.amex:
        new_candidates += parse_amex(args.amex)
    if args.chase:
        new_candidates += parse_chase(args.chase)

    added, skipped_dupe = 0, 0
    for row in new_candidates:
        if row["Classification"] is None:
            continue
        for f in LEDGER_FIELDS:
            row.setdefault(f, "")
        key = dedup_key(row)
        if key in existing_keys:
            skipped_dupe += 1
            continue
        existing_keys.add(key)
        existing_rows.append(row)
        added += 1

    existing_rows.sort(key=lambda r: r.get("Date", ""))

    with open(ledger_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
        writer.writeheader()
        for r in existing_rows:
            writer.writerow({k: r.get(k, "") for k in LEDGER_FIELDS})

    print(f"Added {added} new rows, skipped {skipped_dupe} duplicates. "
          f"Ledger now has {len(existing_rows)} rows -> {ledger_path}")


if __name__ == "__main__":
    sys.exit(main())
