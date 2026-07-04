---
name: perfect-day-planner
description: >-
  Design travel days around the traveler's actual taste — pacing, crowd tolerance,
  food priorities, energy curve — instead of generic top-10 lists. Use this skill
  whenever the user asks what to do, where to eat, or how to spend time on a trip:
  "plan our free day in [city]," "what should we do Saturday," "where should we eat
  near the hotel," "find us a good hike," "is this place worth it," or any request to
  build a day itinerary, pick restaurants, or pace a city visit. Trigger for both
  pre-trip planning and in-trip decisions, even casual one-off questions — the taste
  profile makes every recommendation better.
---

# Perfect Day Planner

Generic travel advice optimizes for the average tourist, and nobody is the average
tourist. This skill builds days around one specific traveler: their pace, their crowd
tolerance, what a meal means to them, and when their energy runs out.

## Step 1: Calibrate taste (once, then reuse)

Look for a `travel-taste-profile.md` in the user's working directory or wherever they
keep personal files. If it exists, read it and plan from it — don't re-interview.

If it doesn't exist, ask a short calibration round (keep it conversational, 6–8
questions, not a form):

- **Pace**: packed schedule, or a few things done well with slack in between?
- **Crowds**: seek the famous spots anyway, or trade fame for elbow room?
- **Food**: destination-worthy meals as anchors, or fuel between activities? Any
  can't-miss categories (coffee, bakeries, wine) or hard constraints (dietary)?
- **Body clock**: early starter or slow morning? How late do evenings go?
- **Legs**: comfortable walking miles per day; hills/stairs okay?
- **Money**: splurge-worthy categories vs. save-everywhere?
- **Non-negotiables**: the daily thing that must happen (a good coffee, a swim, a nap).
- **Allergies** (figurative): what ruins a day? (lines, tour groups, driving, rain
  without a plan B...)

Save the answers to `travel-taste-profile.md` and confirm where you put it. Every
future day plan starts by reading this file — and update it when the user reveals new
preferences ("we hated that market, too crowded" is profile data).

## Step 2: Architect the day

A perfect day has structure. Build around these principles and say *why* a pick fits
the profile:

- **One anchor.** Each day gets one headline experience (the hike, the museum, the
  long lunch). Schedule it when it's best experienced — usually early for crowded
  sights, and matched to the user's energy curve. Everything else supports it.
- **Two minors, max.** A couple of low-commitment secondary stops near the anchor.
  More than that and the day becomes a checklist.
- **Meals are waypoints, not afterthoughts.** Place meals to pull the day through
  neighborhoods worth being in. For food-motivated travelers, a meal can *be* the
  anchor. Flag anything that needs a reservation and how far ahead.
- **Cluster geographically.** The day should trace one rough path — no backtracking
  across town. If two wishlist items are on opposite sides, they belong to different
  days.
- **Respect the energy curve.** Demanding thing early, recovery in the middle
  (long lunch, park, café), gentle evening. Never schedule two high-effort blocks
  back to back.
- **Leave slack.** The best hours of a trip are usually unplanned. A perfect day plan
  has visible white space — say so in the plan rather than filling it.
- **Always a plan B.** One weather/closure alternative per anchor, pre-chosen so a
  rainy morning is a pivot, not a scramble.

## Step 3: Verify before recommending

Check current opening hours, closure days (museums love Mondays), seasonal factors,
and whether reservations are required — using the most recent sources you can find.
A perfect plan built on a closed door is worse than no plan. If something can't be
verified, mark it "confirm locally."

## Output format

```markdown
# [Day, Date] — [City]: [three-word theme]

**Anchor:** [the one big thing, and why it fits you]

## Morning
[time-ish] — [thing] · [1 line: what it is + why it fits the profile]

## Midday
[meal waypoint + neighborhood logic · reservation flag if needed]

## Afternoon
[minor stop(s) + deliberate slack, labeled as such]

## Evening
[gentle close · dinner pick + one backup]

**If it rains:** [plan B]
**Book ahead:** [list with lead times, or "nothing"]
**Skip without guilt:** [famous thing nearby that doesn't fit the profile, and why]
```

The "skip without guilt" line matters: naming what the traveler is *not* doing, and
why it's fine, is what makes a plan feel like theirs instead of a guidebook's.
