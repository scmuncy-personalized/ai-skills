# ai-skills

A personal collection of [Claude skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) —
reusable instruction sets that teach Claude a repeatable workflow. These are generalized
versions of skills I built for my own daily use and
personal life, rewritten for anyone to use. No personal or proprietary data is included.

## The skills

| Skill | What it does |
|-------|--------------|
| [home-cost-basis-tracker](skills/home-cost-basis-tracker/SKILL.md) | Maintains a running ledger of home improvement spending, classified as capital improvements vs. repairs, so the records exist when you sell. Plain-English, layperson-friendly. |
| [delphi-auditor](skills/delphi-auditor/SKILL.md) | Audits capital market assumption files against published LTCMA research: verifies geometric→arithmetic return math, recomputes blended portfolios, flags stale sources and outliers. |
| [perfect-day-planner](skills/perfect-day-planner/SKILL.md) | Plans travel days around *your* taste — pacing, crowds, food, energy curve — via a reusable taste profile, instead of generic top-10 lists. |
| [quant-smell-test](skills/quant-smell-test/SKILL.md) | Recomputes the math in financial documents (returns, fees, totals, risk metrics) and flags what doesn't add up. Recompute, don't trust. |

## Installation

**Claude Code (CLI / desktop):** copy a skill folder into your skills directory:

```bash
git clone https://github.com/scmuncy-personalized/ai-skills.git
cp -r ai-skills/skills/quant-smell-test ~/.claude/skills/
```

**Claude.ai / Cowork:** upload the skill's `SKILL.md` (or a zipped skill folder) via
Settings → Capabilities → Skills, or ask Claude to install it from the file.

Each skill is self-contained — take only the ones you want.

## Important disclaimers

- **None of this is advice.** The financial skills (home-cost-basis-tracker,
  delphi-auditor, quant-smell-test) are organizational and analytical aids. They do not
  provide tax, investment, legal, or accounting advice. Work with your tax professional
  and your firm's compliance process before relying on any output.
- Skills instruct an AI model; outputs can be wrong. The skills are deliberately
  designed to show their work — check it.

## License

MIT — see [LICENSE](LICENSE). Use, adapt, and share freely.
