---
day: 1
phase: 1
title: "Count target values"
ids: []
kind: guided-assignment
plan_version: "v1.1.0"
parts: 0
generated: "2026-09-18"
status: planned
---

# Day 001

This hub links the Day 1 teaching documents and independent exercises. Assigned IDs:
DSA-01, SD-01, PY-01. Document authoring does not mark any study objective complete.

## Navigation — where to start

1. Choose a subject README below; each has its own complete reading order.
2. Learn its explanation, follow the trace, and check readiness before opening practice.
3. Complete your chosen exercise and record actual evidence using that subject's instructions.
4. On a later visit, open [DSA recall](../../docs/DSA_RECALL.md),
   [Python recall](../../docs/LANG_RECALL.md), or [system design recall](../../docs/SD_RECALL.md)
   for a summary without new practice.

| Subject | Budget | Open |
| --- | --- | --- |
| DSA | 60 minutes | [Count target values](dsa_count-target-values/README.md) |
| System design | 30 minutes | [Functional scope](sd_functional-scope/README.md) |
| Python | 15 minutes | [Identity and equality](lang_identity-and-equality/README.md) |

## Read, try, and explain

You may take these in separate sittings and progress at different speeds. Start with any track;
Python and system design do not depend on completing DSA first.

| Track | Teaching document | Your deliverable |
| --- | --- | --- |
| DSA | [Give each step of a scan a precise meaning](dsa_count-target-values/CONCEPTS.md) | One independent solution, correctness and cost arguments, tests, and a failure explanation |
| System design | [Turn a product request into observable behavior](sd_functional-scope/CONCEPTS.md) | Three user actions, two exclusions, one measurable criterion, and a request/failure trace |
| Python | [Separate an object's identity from its current value](lang_identity-and-equality/CONCEPTS.md) | Predictions, a list experiment, regression assertions, and an ownership explanation |

The DSA online route also includes [Reuse counts across many questions](dsa_count-target-values/FREQUENCY_COUNTS.md):
the frequency-table and cumulative-count mechanisms needed before the companion problem.
For the local route, that second part is optional depth.

Teaching demonstrations are provided separately from your unsolved exercises. Their recorded
outputs are author verification, not learner evidence. Deeper follow-ups are optional; they
use spare time or a later review session.

## Session order within each budget

- **DSA, 60 minutes:** 5 clarify your starting confidence; 10 read and trace; 30 independent
  attempt; 10 test and explain; 5 record. Choose the [LeetCode route](dsa_count-target-values/LEETCODE.md)
  or [local route](dsa_count-target-values/PRACTICE.md) as the main attempt.
- **System design, 30 minutes:** 5 state initial assumptions; 10 read the concept; 12 write
  [DESIGN.md](sd_functional-scope/DESIGN.md); 3 critique its measurable outcomes.
- **Python, 15 minutes:** 3 predict; 8 experiment in [lab.py](lang_identity-and-equality/lab.py);
  4 explain and record [NOTES.md](lang_identity-and-equality/NOTES.md).

## Run from the repository root

```powershell
python course.py start 1 --track dsa
python course.py start 1 --track sd
python course.py start 1 --track lang
```

These commands print the selected track's starting document. After your implementations:

```powershell
python course.py practice 1
python days/day-001-count-target-values/lang_identity-and-equality/lab.py
```

The DSA and Python starters intentionally raise `NotImplementedError` until you implement them.
An online-only DSA attempt instead needs actual submission evidence; the local command cannot
certify a LeetCode submission. System design has a written acceptance check, not a server to run.

## Finish with evidence

Use each subject README's acceptance criteria and the [daily checklist](CHECKLIST.md).
Record actual results, hints, unresolved questions, and the next step in the relevant subject's
evidence file. Follow [the study workflow](../../docs/STUDY_WORKFLOW.md) to append track status.
If time expires, record partial progress and continue that track later. Mark whole-day completion
only when all three tracks meet their criteria. Reading these documents alone does not close IDs.

[Master plan](../../docs/00_MASTER_PLAN.md) · [Independent progress](../../docs/TRACK_PROGRESS.csv)
