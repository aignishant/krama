# ADR-0002 — Topic-named folders and LeetCode interview practice

- Date: 2026-09-19
- Status: accepted, explicitly requested by the user
- Amends: v1.0.0 → v1.1.0, master plan sections 1, 4, 9 and 11
- Related: [initial layout decision](ADR-0001-the-plan-as-adopted.md)

## Context

The user is preparing for product-company interviews, including Google, and requested LeetCode
problems and titles in each daily subject folder. The current course uses bare dsa/sd/lang
folders across 168 days. Learner code, test cases and notes may already contain work.

## Decision

Rename each subject folder to its track prefix plus its full topic slug, for example
`dsa_pair-sum-indices`, `sd_idempotency-semantics`, `lang_nonlocal-state`. Keep day numbers,
objective IDs and CLI track names stable. Store actual folder names in the session manifest.
Move existing folders intact, verify protected file hashes, update links and regenerate indexes.

Add a LeetCode assignment to every DSA day and a central index. Topic days have one companion;
review days reuse two earlier companions. Explicitly describe differing contracts. Use one
main attempt in the existing 60-minute session, not a second mandatory problem. Premium tasks
have a complete local alternative. Teach clarification, proof, communication, tests and follow-ups;
do not claim that these are Google's current or guaranteed interview questions.

## Options considered

| Option | Reason |
| --- | --- |
| Keep bare folder names | Does not satisfy the requested visible content titles. |
| Rebuild the course from scratch | Could overwrite learner work and break evidence history. |
| Rename in place and record the mapping | Preserves existing work and supports stable CLI aliases. |
| Add a second daily LeetCode quota | Exceeds the user's one-hour DSA budget. |

## Consequences

Paths become longer and old IDE tabs must reopen their files. All 504 subject directories move;
no day is reordered. `docs/folder_renames.json` resolves historical paths, including append-only
ledger evidence. Existing learner files remain byte-identical. The checker and tests must resolve
paths through the manifest. Upstream granth.py remains unchanged. The original build script is
an archived v1.0 scaffolder and must not be used to rebuild an active course.
