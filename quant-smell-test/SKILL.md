---
name: quant-smell-test
description: >-
  Quant-literate sanity checks for financial numbers: recompute the math in returns
  data, performance reports, fund fact sheets, portfolio statements, and financial
  models, and flag anything that doesn't add up. Use this skill whenever the user asks
  to "sanity check," "smell test," "verify," or "check the math" on anything financial —
  or shares performance figures, a returns series, a fee schedule, a fact sheet, or a
  financial model and asks "does this look right?" Also trigger when the user is
  skeptical of a number ("this return seems too good," "these totals seem off") or is
  reviewing a document from a third party (fund manager, vendor, counterparty) before
  trusting or forwarding it.
---

# Quant Smell Test

Financial documents are full of numbers that were computed once, pasted many times,
and never re-checked. This skill's stance: **recompute, don't trust.** Every stated
figure that can be derived from other figures in the document gets re-derived, and
the work is shown so the user can check the checker.

## ⚠️ Scope disclaimer (state it in every report)

This is an analytical aid, not an audit, and nothing in it is investment, tax, or
legal advice. A FLAG means "investigate," not "fraud." Errors found here should be
confirmed against source data before anyone acts on them.

## The check library

Run every check that the document's contents make possible. For each, report the
stated value, your recomputed value, and a verdict. Skip a check only if the inputs
genuinely aren't present — and say which checks were skipped and why.

### Returns math
- **Compounding**: period returns must *geometrically link* to the stated cumulative
  figure: `(1+r₁)(1+r₂)...(1+rₙ) − 1`. A cumulative number that matches the arithmetic
  *sum* of periods instead is a classic error — flag it.
- **Annualization**: multi-year returns annualize as `(1 + cumulative)^(1/years) − 1`
  (CAGR). Flag arithmetic averages presented as annualized returns — the gap widens
  with volatility.
- **Volatility scaling**: monthly vol annualizes as `σ × √12` (daily: `√252`). Flag
  linear (×12) scaling.
- **Risk metrics**: recompute Sharpe `(return − risk-free) / vol` and any stated
  alpha/beta relationships if the components are given. Check the risk-free rate used
  is stated and plausible for the period.

### Accounting identities
- **Totals**: every subtotal and total re-added; allocation weights sum to 100%
  (watch for 99.9%/100.1% rounding vs. real gaps).
- **Weighted averages**: stated portfolio-level yield, duration, expense ratio, etc.
  must equal the weighted average of the holdings shown.
- **Fees**: gross return − net return ≈ stated fee (compounding makes this
  approximate; flag gaps well beyond the fee).
- **Units**: hunt for bps/percent confusion (a "0.25%" fee stated as "25%" or vice
  versa), monthly/annual mismatches, and thousands/millions inconsistencies between
  tables.

### Plausibility (the actual smell test)
- **Too good**: returns far above the asset class's plausible range, Sharpe ratios
  sustained above ~2, or a long series with almost no negative periods. Suspiciously
  *smooth* return streams deserve extra skepticism — smoothness is how both stale
  pricing and fabricated track records look.
- **Internal contradictions**: risk ranked "conservative" atop an 80% equity
  allocation; a "5-year track record" whose table has 42 months; yield and price
  moving the same direction between periods without explanation.
- **Period alignment**: fund and benchmark measured over identical date ranges;
  "as of" dates consistent across pages; calendar vs. fiscal year mixups.
- **Survivorship tells**: a composite whose membership count shrinks over time, or
  "selected" accounts, without disclosure.

## Report format

ALWAYS use this exact structure:

```markdown
# Quant Smell Test: [document name]
Checked: [date] · Checks run: [n] · Skipped: [list + why, or "none"]

## Verdict summary
[1–3 sentences: overall, does this document hold together?]

## Findings
| # | Check | Stated | Recomputed | Verdict | Severity |
|---|-------|--------|------------|---------|----------|

Verdicts: PASS · FLAG (doesn't reconcile — investigate) · FAIL (demonstrably wrong)
Severity: how much the error would change a decision, not how big the number is.

## Work shown
[For every FLAG/FAIL: the arithmetic, step by step.]

## What I couldn't check
[Figures that can't be derived from the document alone, and what source data
would allow verification.]

---
*Analytical aid, not an audit or advice. Confirm findings against source data.*
```

## Judgment calls

- Rounding is not a finding. Use tolerances proportional to the document's stated
  precision (a table shown to one decimal place can be off by 5 bps legitimately).
  State the tolerance you applied.
- One error repeated by propagation (a bad subtotal flowing into a grand total) is
  ONE finding with its downstream effects listed — don't inflate the count.
- The absence of findings is a real result. "All 14 checks pass" builds warranted
  confidence; say it plainly rather than hunting for something to flag.
