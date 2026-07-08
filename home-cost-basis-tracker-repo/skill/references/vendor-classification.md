# Vendor & Keyword Classification Rules

This file is the living classification map for Samantha's Amex (`activity_1.csv`-style) and Chase (`Chase7861_Activity_20260702.csv`-style) exports. Update it whenever a new vendor is confirmed by Samantha so future runs classify it automatically without asking again.

## How to use this file
1. When scanning a new transaction export, check the vendor description against the tables below first (case-insensitive substring match — vendor names are inconsistently capitalized, especially in Chase).
2. If a vendor isn't listed, apply the general keyword rules, then the heuristic in `irs-cost-basis-guidance.md`.
3. If still ambiguous, put it in **Needs Review** — do not guess silently on anything over ~$100 or anything structural.
4. When Samantha confirms a classification for a new vendor, add it to the appropriate table below so it's remembered permanently.

## Chase "Home" category note
Chase pre-tags many relevant transactions with `Category = Home`. Always pull every row with that category as a candidate, even if the vendor name doesn't obviously match a keyword — this is the highest-recall signal in the Chase file. Not everything tagged `Home` belongs in the basis ledger (see furnishings exclusions below), but nothing tagged `Home` should be silently skipped without a classification decision.

## Confirmed vendors — Capital Improvement (adds to basis)
| Vendor (as it appears on statement) | Notes |
|---|---|
| THE HOME DEPOT | Building materials/fixtures retailer — classify per line item context if known, default improvement for renovation-scale purchases, flag small/ambiguous amounts (<$50) for review since Home Depot also sells consumables |
| LOWES / LOWE'S | Same treatment as Home Depot |
| BEDROSIANS TILE & STONE | Tile — improvement (flooring/wall tile install) |
| BEST TILE (RALEIGH) | Tile — improvement |
| IN *MARBLE BOTANICS / MARBLE BOTANICS LLC | Stone fabrication/countertops — improvement |
| BUILD.COM | Building/plumbing fixtures — improvement |
| KOHLER CO | Plumbing fixtures — improvement |
| GARAGE DOOR SPECIALIST | Garage door — improvement |
| LEGRAND | Electrical wiring devices/switches — improvement |
| IN *SOLUTIONS ELECTR(IC) | Electrician labor — improvement if new circuits/fixtures, review if simple repair call |
| ALTERNATIVE POWER (SOLAR) | Solar installation — improvement |
| POLYLOK INC | Septic system components — improvement |
| SP CONCRETE EXCHANGE | Concrete supplies — improvement (hardscape/foundation work) |
| VISUAL COMFORT | Lighting fixtures — improvement if hardwired/permanent fixture |
| RESTORATION HARDWARE (hardware/fixtures, not furniture) | Review case-by-case — this vendor sells both furniture (exclude) and hardware/fixtures (improvement); check line-item description or ask |

## Confirmed vendors — Repair / Maintenance (excluded from basis, but logged for reference)
| Vendor | Notes |
|---|---|
| LEAF & LIMB | Tree/landscaping service — maintenance unless a specific hardscape/structural quote is confirmed |
| NATURE FIRST LANDSCAPING | Landscaping — maintenance by default |
| LOGANS GARDEN SHOP | Plants/garden supplies — maintenance |
| ATLANTIC GARDENING | Plants/garden supplies — maintenance |
| FRANK'S PERENNIAL BORDER | Plants — maintenance |
| SP BOTANICAL INTERESTS / SP EAST FORK / SP VEGO GARDEN | Seeds/plants — maintenance |
| BIG BLOOMERS FLOWER FARM | Plants/flowers — maintenance |
| WWP*TRIANGLE PEST CO | Pest control — maintenance |
| PY *CLEARDEFENSE | Pest control — maintenance |
| SQ *CARAVAN RUGS CLEANING | Cleaning service — maintenance |
| BURKE BROTHERS HARDWARE | Small hardware store — maintenance by default for typical small-dollar purchases; flag for review if a single large purchase suggests a bigger project |
| PRISM PAINT & DESIGN | Painting — maintenance by default (repaint); reclassify as improvement only if confirmed part of a larger remodel scope |
| PINKS WINDOWS (RALEIGH) | Window **cleaning** service (confirmed by Samantha) — maintenance, excluded from basis. Do NOT confuse with window installation/replacement, which would be an improvement. |

## Confirmed vendors — Excluded (personal property / not home-related, not part of basis)
| Vendor | Notes |
|---|---|
| CRATE AND BARREL, WILLIAMS-SONOMA.COM, WF*WAYFAIR, Saatva, Nordic Knots Inc., TWOPAGESCURTAINS, MEG BROWN HOME FURNITURE, THE CONTAINER STORE, SP MAHONESWALLPAPER (review — wallpaper is arguable, default exclude/maintenance), SP PEPPER HOME, SP COLEY HOME, SP KASSATEX | Furniture, rugs, curtains, decor, storage — personal property, not part of home's cost basis. Logged in a separate "Furnishings (not basis)" tab if Samantha wants the record for insurance purposes, but never added to the capital improvement total. |
| FINE*GARDENING | Magazine subscription — not home-related spend |
| REJUVENATION | Lighting — usually decor-grade fixtures; treat as Needs Review (could be hardwired permanent fixture = improvement, could be a lamp = excluded) |

## General keyword rules (fallback when vendor isn't in the tables above)

**Likely capital improvement** — substrings: `tile`, `granite`, `marble`, `countertop`, `cabinet`, `hvac`, `roofing`, `roof`, `window`, `garage door`, `plumb`, `electric` (contractor context), `solar`, `septic`, `flooring`, `hardwood`, `remodel`, `renovat`, `construct`, `contractor`, `deck`, `patio` (hardscape), `fence` (permanent), `insulation`, `drywall` (if part of a project, not a small patch).

**Likely repair/maintenance** — substrings: `pest`, `lawn`, `landscap`, `garden` (routine), `clean`, `paint` (standalone), `hvac service`/`hvac repair`, `plumber` (single service call), `handyman` (single small job).

**Likely excluded (not home-related or personal property)** — substrings: `furniture`, `rug`, `curtain`, `decor`, `wayfair`, `pottery barn`, `crate and barrel`, `williams-sonoma`, restaurant/grocery/travel/entertainment keywords already excluded by category.

**When in doubt, flag "Needs Review."** False negatives (missing a real improvement) are much costlier at sale time than a slightly longer review list.
