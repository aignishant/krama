# ADR-0003 — Separate system-design reference answers from personal practice

- Date: 2026-09-22
- Status: accepted; the learner selected this workflow
- Related: [master plan](../00_MASTER_PLAN.md), [teaching workflow](../TEACHING_WORKFLOW.md)

## Context

Expanded SD days explain concepts but leave `TODO(me)` sections in `DESIGN.md`. The learner
asked who fills them and requested a complete reference design while retaining their own
practice file. Concept examples alone do not show a finished response to the day's actual task.

## Decision

Every expanded SD day has three distinct documents:

| Document | Owner | Purpose |
| --- | --- | --- |
| `CONCEPTS.md` | Course author/assistant | Explain the decision method and reasoning |
| `REFERENCE_DESIGN.md` | Course author/assistant | Give a complete worked response to the actual assignment |
| `DESIGN.md` | Learner | Capture an independent attempt, critique, observations, and remaining questions |

The assistant writes reference answers as part of expanding a day. The learner fills `TODO(me)`
in their practice file. Reference answers include explicit assumptions, the requested artifact
or calculation, a justified decision, an alternative, a failure walkthrough, and an honest
self-review. They contain no unfinished exercise placeholders and make no claim of measured
production behavior without evidence. They are one defensible answer, not a unique correct design.

Offer a guided route that reads the reference before practice and an independent route that
compares after an attempt. Reading is allowed without completing practice; it does not satisfy
the existing assessment. Weekly cold reviews still begin without the reference.

## Consequences

Backfill Days 001–005 now. Future expansions, including review-day expansions, add their own
reference; planned briefs do not falsely claim one exists. Preserve all existing `DESIGN.md`
content and progress records. Keep the 30-minute budget by using the existing reference and
critique windows, continuing later if needed. No extra daily design is assigned.

This adds a file inside the existing SD subject folder. The v1.1.0 folder layout, manifest,
IDs, CLI aliases, and assessment criteria remain compatible; no bulk version migration is needed.
