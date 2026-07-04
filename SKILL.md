---
name: home-cost-basis-tracker
description: >-
  Track home renovation and improvement spending in a running cost-basis ledger, so
  homeowners have organized records when they eventually sell. Use this skill whenever
  the user mentions home renovations, remodeling, home improvement projects, capital
  improvements, house projects, tracking what they've spent on their home, "cost basis,"
  or wants home-related purchases pulled out of a credit card or bank statement. Also
  trigger when the user uploads a card/bank transaction export and asks about house
  spending, or asks whether a home expense "counts for taxes" — even if they never say
  the words "cost basis."
---

# Home Cost Basis Tracker

Help the user maintain a running, well-organized ledger of money spent improving their
home, classified the way the IRS thinks about it: **capital improvements** (which may
increase the home's cost basis) versus **repairs and maintenance** (which generally do
not).

## ⚠️ Read this first — and say it to the user

This skill is an **organizational tool, not tax advice**. Open every session that uses
this skill by reminding the user, in plain language:

> I can help you organize and classify your home spending, but I'm not a tax
> professional and this isn't tax advice. Classifications here are educated starting
> points — please review the ledger with your tax professional (CPA or enrolled agent)
> before relying on it, especially before selling your home.

Never present a classification as an authoritative tax determination. When an item is
ambiguous, say so and mark it for professional review rather than guessing confidently.

## Why this matters (explain to the user in plain English)

When someone sells their home, their taxable gain is roughly *sale price minus what the
home "cost" them* — and that cost (the "basis") includes not just the purchase price
but also qualifying improvements made over the years. In the U.S., single filers can
typically exclude up to $250,000 of gain ($500,000 for married filing jointly) on a
primary residence, but home values can outgrow that exclusion. Every documented
improvement raises the basis and can shrink the taxable gain. The IRS reference is
**Publication 523 (Selling Your Home)** — mention it so the user and their tax pro can
verify anything.

The catch: people rarely keep records. This skill exists so the records build up
painlessly over the years instead of being reconstructed in a panic at sale time.

## Workflow

1. **Find or create the ledger.** Look for an existing `home-cost-basis-ledger.md`
   (ask the user where they keep it if unclear). If none exists, create one using the
   template below and ask for the basics: purchase date, purchase price, and any major
   past projects they remember (mark reconstructed entries as "estimate — locate
   receipt").

2. **Gather candidate transactions.** If the user uploads a card or bank statement
   export, scan it for home-related merchants and amounts: contractors, hardware
   stores, appliance retailers, landscapers, plumbers, electricians, HVAC companies,
   flooring, roofing, window, and fencing vendors, permit fees, architect/design fees.
   List what you found before adding anything.

3. **Classify each item** using the guide below. When you can't tell from the merchant
   alone (a $4,000 plumber charge could be a repair or a repipe), ask the user what the
   work was.

4. **Record entries** in the ledger with date, vendor, amount, a plain description,
   the classification, and one line of reasoning. Update the running totals.

5. **Remind about receipts.** Documentation is what survives an audit. Nudge the user
   to keep invoices/receipts for anything classified as an improvement (a photo in a
   dedicated folder is fine).

## Classification guide

**Capital improvement** — adds value to the home, prolongs its useful life, or adapts
it to new uses. Typically: additions, full renovations (kitchen, bath), new roof, new
HVAC system, new water heater, new windows, new flooring, decks, fences, in-ground
landscaping structures, built-in appliances, new electrical panel, repiping, insulation
upgrades, permits and design fees tied to these projects.

**Repair / maintenance** — keeps the home in ordinary operating condition without
adding value or life. Typically: fixing a leak, patching drywall, repainting a room,
servicing the furnace, gutter cleaning, lawn care, pest control, replacing a broken
window pane.

**Gray areas to flag for the tax pro rather than decide:**
- Repairs done *as part of a larger remodel* (these can sometimes be included in the
  improvement).
- Partial replacements (half the fence, some of the windows).
- Items that were later replaced again (the earlier improvement may no longer count).
- Insurance-reimbursed work.

Classify these as **"Review with tax pro"** and note the question, don't force them
into a bucket.

## Ledger format

Use this exact structure so the file stays consistent across sessions:

```markdown
# Home Cost Basis Ledger
Property: [address or nickname — user's choice]
Purchased: [date] for $[amount]
Last updated: [date]

> This ledger is a personal recordkeeping aid, not tax advice.
> Review classifications with a tax professional. Reference: IRS Publication 523.

## Capital improvements (running total: $XX,XXX)
| Date | Vendor / Project | Amount | Description | Reasoning | Receipt? |
|------|------------------|--------|-------------|-----------|----------|

## Review with tax pro
| Date | Vendor / Project | Amount | Description | Open question |
|------|------------------|--------|-------------|---------------|

## Repairs & maintenance (not added to basis — kept for reference)
| Date | Vendor / Project | Amount | Description |
|------|------------------|--------|-------------|
```

## Tone

Assume the user is a smart layperson, not an accountant. Define any term of art the
first time it appears ("basis," "capital improvement"), keep explanations short, and
never bury the disclaimer.
