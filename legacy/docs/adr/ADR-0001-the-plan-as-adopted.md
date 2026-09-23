# ADR-0001 — Separate tracks with a fixed daily budget

- Date: 2026-09-18
- Status: accepted for the initial course; duration is an author assumption
- Related: [master plan](../00_MASTER_PLAN.md)

## Context

The user requested DSA, system design and Python in exactly three subject folders per day,
with 60, 30 and 15 minutes respectively. Python experience is five years. The supplied
Granth skill normally forbids clocks, uses shared parts/source/lab folders, and guards all
subjects with one progress ledger. Those defaults conflict with the user's explicit needs.
The working tree also contains pre-existing tracked deletions; no restore or commit is authorized.

## Decision

Use 168 study days grouped into 24 weeks, with six topic days and a seventh review day.
Every day has dsa/, sd/ and lang/. Each contains an immediately usable guided assignment.
Full Granth eleven-section teaching chapters are a separate, on-demand expansion, not claimed
to be written by these assignment briefs. Preserve granth.py verbatim for plan indexing;
course.py validates the adapted format and runs practice. Keep independent track progress.
All source code exercises remain unsolved. Timing is a cap, not a mastery guarantee.

## Options considered

| Option | Decision |
| --- | --- |
| Unmodified Granth layout and no clocks | Reject: contradicts the requested daily budget and folders. |
| One combined daily lesson and progress flag | Reject: prevents independent study of the three tracks. |
| Short topic list | Reject: omits practice contracts, revision and daily deliverables. |
| 168-day guided course with optional deep chapters | Adopt: broad coverage with explicit scope and manageable daily tasks. |

## Consequences

The three tracks can progress at different speeds. Scope is 144 new DSA problems and 24 review
sessions, not a promise of mastery of every algorithm. Hard problems can require additional
study days. The custom checker is necessary because upstream depth checks require a different
layout and forbid clocks. Passing structural checks does not certify learning or deep prose.
The upstream done command stages and commits all changes, so it is excluded from the study workflow.
Revisit the duration after week 2 using actual solve rate; append a new decision before renumbering.
