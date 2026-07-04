---
name: delphi-auditor
description: >-
  Audit the oracle: review a firm's capital market assumptions (CMA) file against the
  published long-term capital market assumption (LTCMA) research it cites, verify the
  geometric-to-arithmetic return math, recompute blended portfolio figures, and flag
  stale dates and outliers. Use this skill whenever the user uploads or references a
  capital market assumptions file, expected-return table, or Monte Carlo input file —
  or asks to "check our CMAs," "verify these expected returns," "are these assumptions
  current," "proof this assumptions file," or uploads an LTCMA publication (JP Morgan,
  Vanguard, BlackRock, Morgan Stanley, etc.) alongside an internal assumptions document.
  Also trigger on any request to validate return, volatility, correlation, or inflation
  assumptions feeding a financial planning or simulation engine.
---

# Delphi Auditor

Every financial planning engine runs on a crystal ball: a file of long-term expected
returns, volatilities, and correlations. When that file is stale or its math is wrong,
every simulation downstream is wrong — confidently and invisibly. This skill audits
the crystal ball.

**Inputs:** an internal assumptions file (markdown, CSV, or spreadsheet), and ideally
the published LTCMA source documents it draws from (e.g., JP Morgan LTCMA, Vanguard
VCMM outlook, BlackRock CMAs). If the user provides only the internal file, run every
check that doesn't require the source, and clearly list which checks were skipped and
what to upload to complete them.

## Audit checks

Run all of these. Never silently correct anything — every change must appear in the
findings table with the math shown.

### 1. Freshness
- Identify every cited source and its edition/publication year. Flag any source that
  is not the most recent edition you can verify (search the web if needed; if you
  can't verify, flag as "unverified — confirm latest edition").
- Flag any "as of" date in the file older than ~12 months, and any internal
  inconsistency (e.g., the header says 2026 but a table cites a 2024 outlook).

### 2. Geometric ↔ arithmetic conversion
LTCMA publications typically report **geometric** (compound) returns; simulation
engines often need **arithmetic** means. Under the standard lognormal approximation:

```
arithmetic ≈ geometric + volatility² / 2
```

(with returns and volatility in decimal form). Recompute every conversion in the file.
Flag deviations beyond ±10 bps and show the recomputation:
`found 6.9%, expected 7.2% + (16%²)/2 = 8.48% → ERROR`. If the file uses a different
convention (e.g., exact lognormal), note it and apply that convention consistently
rather than forcing this approximation.

### 3. Blended portfolio math
For any blended/model portfolio rows: verify weights sum to 100%, then recompute the
blended return as the weighted sum of component returns. Blended **volatility** is NOT
a weighted sum — if the file computes it that way without correlations, flag it (a
weighted-average vol overstates risk of a diversified blend). Tolerance: ±5 bps on
returns.

### 4. Cross-source outliers
Compare each asset class assumption against the cited source(s). Default flag
thresholds (state them in the report so the user can adjust): deviations greater than
**±150 bps for equity classes**, **±75 bps for fixed income and cash**, **±50 bps for
inflation**. A deviation isn't automatically wrong — firms adjust published numbers —
but every deviation should be *deliberate and documented*. Flag undocumented ones.

### 5. Internal consistency
- Ordering sanity: cash return ≤ short-term bonds ≤ intermediate bonds (in expected
  return, absent a documented rationale); equity vol > investment-grade bond vol.
- Equity risk premium (equity return minus cash) in a plausible 2–7% band; outside it,
  flag for review.
- One inflation assumption used consistently everywhere it appears.
- Correlations within [-1, 1]; correlation matrix symmetric with 1.0 diagonal.
- No asset class present in one table but missing from another (return table vs.
  vol table vs. correlation matrix).

### 6. Housekeeping
Flag any unresolved TODO/FIXME/placeholder text, empty cells, or comments like
"update this" that suggest the file went to production half-finished.

## Report format

ALWAYS use this exact structure:

```markdown
# Delphi Audit: [filename]
Audited: [date] · Sources available: [list or "none provided"]
Checks skipped (missing sources): [list or "none"]

## Findings
| # | Severity | Location | Found | Expected | Basis |
|---|----------|----------|-------|----------|-------|

Severities: ERROR (math is wrong) · STALE (outdated source/date) ·
OUTLIER (deviates from source beyond threshold) · WARN (consistency/housekeeping)

## Corrected file
[Full corrected version, only if the user wants one — ask. Every change here
must correspond to a finding above.]

## Change summary
[One line per change: what, where, why]
```

## Judgment calls

- Show your arithmetic on every quantitative finding. The user must be able to check
  you the way you checked the file.
- If the file's numbers disagree with a source but a footnote explains why, that's not
  a finding — that's a documented adjustment. Read footnotes before flagging.
- This is an analytical aid for financial professionals. Note in the report footer
  that outputs should be reviewed by the firm's investment/compliance process before
  production use, and that nothing here is investment advice.
