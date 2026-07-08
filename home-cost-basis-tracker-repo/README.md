# Home Cost Basis Tracker

A personal, IRS-aware record of home-related spending, classified into what does and does not add to the home's cost basis — so the eventual adjusted-basis calculation at sale is backed by clean, contemporaneous records.

> ⚠️ **Keep this repository private.** It contains personal transaction detail (vendors, dates, amounts).

## What's here

```
.
├── README.md
├── .gitignore
├── ledger/
│   └── home_cost_basis_ledger.csv     ← the source of truth; every update is a commit
├── output/
│   └── Home_Cost_Basis_Ledger.xlsx    ← generated review workbook (optional, regenerable)
└── skill/
    ├── SKILL.md
    ├── references/
    │   ├── irs-cost-basis-guidance.md ← capital improvement vs. repair rules (Pub 523)
    │   └── vendor-classification.md   ← living vendor map; update as vendors are confirmed
    └── scripts/
        ├── build_ledger.py            ← parse new Amex/Chase exports → append to ledger
        └── export_review_workbook.py  ← ledger CSV → formatted Excel workbook
```

## Updating the ledger with new statement data

```bash
python skill/scripts/build_ledger.py \
  --amex path/to/new_amex.csv \
  --chase path/to/new_chase.csv \
  --ledger ledger/home_cost_basis_ledger.csv
```

Re-running against overlapping exports is safe — rows already in the ledger (matched on date + vendor + amount) are skipped automatically.

Then regenerate the review workbook:

```bash
python skill/scripts/export_review_workbook.py \
  --ledger ledger/home_cost_basis_ledger.csv \
  --out output/Home_Cost_Basis_Ledger.xlsx
```

Commit the updated ledger with a message noting the date range of new transactions, e.g.:

```bash
git add ledger/home_cost_basis_ledger.csv output/Home_Cost_Basis_Ledger.xlsx
git commit -m "Update home cost basis ledger — Jul 2026 statements"
```

## Classification categories

- **Capital Improvement** — adds to home basis
- **Needs Review** — ambiguous; requires a human decision before it counts
- **Repair/Maintenance (excluded)** — logged for reference, does not add to basis
- **Excluded - Personal Property** — furnishings/decor, not part of the home itself

This tracker is a disciplined first-pass system, not tax advice on any specific item. Confirm ambiguous or high-dollar classifications with a CPA before relying on them at sale.
