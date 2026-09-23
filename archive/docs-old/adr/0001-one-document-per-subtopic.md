# ADR 0001 — One document per subtopic, not one lesson per day

**Status:** accepted · 2026-08-23

## Context

The obvious structure for a daily curriculum is one `LESSON.md` per day. It is easy to write,
easy to navigate, and it is what almost every such repository does.

It fails for a specific reason. A single file has one budget of attention, and the writer spends
it on the first idea. The second and third ideas of the day get progressively thinner treatment —
not because they are easier, but because the file is already long. Readers experience this as
"the lesson tailed off", and the ideas at the end of a day are systematically the least
understood.

Worse: a single file cannot be *checked*. There is no mechanical way to ask "did this day treat
all three of its concepts to the same depth" when all three live in one document.

## Decision

A day is a folder. One document per subtopic, numbered `<section>.<subtopic>`, each carrying the
full ten-section depth contract. The hub is a map, not a summary.

## Consequences

- Every idea gets its own story, its own derived cost, its own failure mode. The third idea of a
  day is treated exactly like the first.
- The contract becomes enforceable: `scripts/depth_check.py` can verify per-document.
- Days become longer to write. This is accepted; the plan explicitly has no time budget.
- Navigation costs more clicks. Mitigated by the hub's §2 map, which states the reading order.
- Splitting an existing shallow page into shallower pages does **not** satisfy this ADR. Days are
  written fresh against the contract.
