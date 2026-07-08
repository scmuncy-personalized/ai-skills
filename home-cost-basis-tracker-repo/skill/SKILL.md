---
name: home-cost-basis-tracker
description: >
  Samantha's home renovation cost-basis tracking skill. Use this whenever she uploads or references Amex (activity_1.csv-style) or Chase (Chase7861_Activity_20260702.csv-style) transaction exports and wants home-related spending pulled out for cost basis purposes, or when she asks to "update the cost basis ledger," "log renovation spending," "what counts as a capital improvement," "track my house expenses," "add this to the home basis record," or anything about capital improvements vs. repairs for tax purposes. Always run this — instead of a generic spending summary — whenever renovation, remodeling, home improvement, or house-related transactions come up, since this skill maintains a running, IRS-aware ledger rather than a one-off summary. Trigger even if she just uploads a new statement CSV without explicit instructions — check it for home-related spend automatically.
---

# Home Cost Basis Tracker

Maintains Samantha's running record of home-related spending, classified per IRS guidance into what does and doesn't add to her home's cost basis — so that whenever she eventually sells, the adjusted basis calculation is backed by clean, contemporaneous records instead of a scramble through years of statements.

This is a **living ledger skill**: every time new transaction data shows up, add to the existing record rather than starting over. Read `references/irs-cost-basis-guidance.md` for the substantive tax rules and `references/vendor-classification.md` for the vendor/keyword rules learned from Samantha's actual accounts — update the latter whenever she confirms a new vendor's classification.

## The ledger

The persistent record lives in a CSV called `home_cost_basis_ledger.csv` with these columns:

`Date, Source, Vendor (raw), Amount, Classification, Project/Category, Confirmed by Samantha, Notes`

Classification is always one of:
- **Capital Improvement** — adds to home basis
- **Needs Review** — ambiguous, Samantha needs to weigh in
- **Repair/Maintenance (excluded)** — logged for her own records, but does not add to basis
- **Excluded - Personal Property** — furnishings/decor, not part of the home itself

**Where the ledger file lives**: ask Samantha where she wants the canonical copy kept — her preference is her own GitHub repo (see "GitHub sync" below), but it can also live as a project file or Google Drive file. Whatever the location, always treat it as the single source of truth: read the existing copy before adding anything new, and write back to the same location so nothing forks into duplicate versions.

## Workflow: processing new transaction data

1. **Locate the current ledger.** If Samantha hasn't said where it lives, ask once, then remember for future sessions (or check the GitHub repo / Drive folder if one's already been set up).
2. **Run the parser** on any newly provided Amex/Chase CSV(s):
   ```bash
   python scripts/build_ledger.py --amex <amex.csv> --chase <chase.csv> --ledger <path/to/home_cost_basis_ledger.csv>
   ```
   This appends new rows and automatically skips anything already in the ledger (matched on date + vendor + amount), so it's safe to re-run against overlapping statement exports.
3. **Classify.** The script applies the vendor table first, then keyword fallbacks, then flags true ambiguity as Needs Review. It only pulls in transactions that look home-related at all (via Chase's `Home` category tag or keyword match) — everything else is left out of the ledger entirely rather than cluttering it.
4. **Surface "Needs Review" items to Samantha** with enough context to decide (vendor, amount, date) and a one-line prompt on what would tip the classification (e.g., "was this part of the kitchen project, or a standalone repair?"). Update `references/vendor-classification.md` with her answer so the same vendor auto-classifies correctly next time.
5. **Generate the review workbook** for anything she wants to see formatted rather than raw CSV:
   ```bash
   python scripts/export_review_workbook.py --ledger <path/to/home_cost_basis_ledger.csv> --out Home_Cost_Basis_Ledger.xlsx
   ```
   Recalculate with `python /mnt/skills/public/xlsx/scripts/recalc.py Home_Cost_Basis_Ledger.xlsx` before presenting (per xlsx skill requirements) and confirm zero formula errors.
6. **Report back concisely**: running Capital Improvement total, count/dollar amount pending in Needs Review, and anything unusual (a big jump, a new recurring vendor, a possible duplicate that didn't auto-dedupe because the description text varied).

## Classification confidence and judgment calls

- Default to caution: **never silently classify anything over ~$100 or anything structural** without either a vendor-table match or a clear keyword match — send it to Needs Review instead.
- A vendor selling both improvement-grade and personal-property items (Restoration Hardware, Rejuvenation) should stay in Needs Review until Samantha specifies which line items were which.
- Returns/credits are excluded from automatic totals by the parser (Chase `Type = Return` rows are skipped) — mention them to Samantha if they relate to a previously logged improvement so she can net them manually.
- If a repair-looking item (paint, small hardware) is called out as part of a larger renovation project, reclassify it as Capital Improvement and note the project name in `Project/Category` — this is exactly the "repair becomes improvement when bundled into a remodel" nuance from the IRS guidance file.

## GitHub sync (if Samantha wants the ledger version-controlled in her own repo)

Claude does not have stored GitHub credentials and will never push to a repository without being told exactly which repo and how to authenticate. When she wants this synced to GitHub:
1. Ask for the repo (owner/name or full URL) if not already known.
2. Ask how she wants to authenticate for pushes from this environment (e.g., a personal access token she pastes for that session, or she prefers to `git pull`/`git push` herself using the diffed files Claude prepares).
3. Stage the ledger CSV, the workbook, and this skill folder as a commit with a clear message (e.g., `Update home cost basis ledger — <date range of new transactions>`).
4. Always show her the diff/summary of what's being committed before pushing, and confirm before any push (pushing is a public/shared-repo action requiring explicit per-session confirmation, even if she's set this up before).

## Reference files

- `references/irs-cost-basis-guidance.md` — substantive capital improvement vs. repair rules, record-keeping requirements, why this matters even under the §121 home sale exclusion
- `references/vendor-classification.md` — the living vendor/keyword classification map; update this file, not just the ledger, whenever a new vendor is confirmed

## Tone

Samantha is a CFP candidate and financial professional — no need to explain basic tax concepts back to her. Be precise about what's confirmed vs. still ambiguous, and don't round up Needs Review items into the confirmed total just to show a bigger number.
