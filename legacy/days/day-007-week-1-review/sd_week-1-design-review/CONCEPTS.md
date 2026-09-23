---
day: 7
part: "2.1"
title: "Revise a design by challenging its weakest assumption"
ids: [SD-07]
level: working
prerequisites: ["Days 1–6 design memos"]
failure: true
---

# Revise a design by challenging its weakest assumption

**Cold assessment first:** select and defend your weakest earlier decision before reading this
lesson or [REFERENCE_DESIGN.md](REFERENCE_DESIGN.md). They are repair and comparison material.

## One-line answer

A useful review changes a decision because a named requirement, calculation, or failure trace challenged it.

## The story

A shop has room for today's orders but promises to keep every order for a year. The shelf
fits today's notebook; the promise concerns many notebooks. Reviewing only today's fit misses
the reason the design will fail.

## The idea in plain language

A design defense connects a user promise to assumptions, an artifact, and a way to falsify the
decision. An assumption is an input you chose; an observation is evidence you actually collected.
A sensitivity check changes one assumption and asks whether the decision still holds.

Recognize weak designs by unsupported numbers, undefined success, an unnamed source of truth,
or a failure path that says only “retry.” Choose one weak decision to revise. A review is not
an invitation to replace the whole system with more components.

## Why Krama needs it

[Day 8's journey](../../day-008-first-repeated-value/sd_request-journey/CONCEPTS.md) adds timing
boundaries outside the app. A defensible requirement tells you which of those delays belongs
to the promise and which belongs to a separate dependency.

## The source behind it

This review uses the earlier course lessons as its teaching sources. [Handling Overload](https://sre.google/sre-book/handling-overload/)
(`spec:sre-overload`, rechecked 2026-09-22) supports treating capacity as workload-dependent.
The review arithmetic and proposed thresholds below are hypothetical, not benchmark results.

## The mechanism

### Worked trace

| Earlier lesson | Review question |
| --- | --- |
| [Scope](../../day-001-count-target-values/sd_functional-scope/CONCEPTS.md) | What observable outcome does the user receive? |
| [Quality](../../day-002-find-the-first-maximum/sd_quality-requirements/CONCEPTS.md) | What population, boundary, and target define success? |
| [Traffic](../../day-003-stable-compaction/sd_traffic-estimates/CONCEPTS.md) | Did daily totals become rates with explicit peak assumptions? |
| [Storage](../../day-004-reverse-a-segment/sd_storage-estimates/CONCEPTS.md) | Do retention and overhead fit, not just one day? |
| [Latency](../../day-005-merge-sorted-arrays/sd_latency-budgets/CONCEPTS.md) | Is the budget distinct from a measured percentile? |
| [Baseline](../../day-006-best-single-trade/sd_single-node-baseline/CONCEPTS.md) | Which component owns the fact and which limit will you measure? |

Suppose a draft allocates 20 decimal GB for mappings. Its assumptions are 100,000 new mappings/day,
500 bytes/mapping, and 365 days' retention. Raw annual storage is
`100,000 × 500 × 365 = 18,250,000,000 bytes = 18.25 GB`.
The draft says “fits” because 18.25 is below 20. A proposed 2× factor for indexes and other
on-disk overhead changes the estimate to 36.5 GB, before logs, backups, and operating-system space.
That factor is a planning assumption requiring measurement, not a database guarantee.

The revision can reserve a larger explicit storage budget or negotiate shorter retention.
If the retention promise stays fixed, deleting older mappings is not an equivalent solution.
The reasoning works because every multiplier has units and a stated scope; another reviewer
can change a multiplier and reproduce the consequence. Next verify actual bytes per stored
record and usable free space instead of turning the estimate into a claimed observation.

## When it breaks

```python
raw_gb = 100_000 * 500 * 365 / 1_000_000_000
provisioned_gb = 20
modeled_gb = raw_gb * 2
print(f"raw={raw_gb:.2f} GB; modeled with overhead={modeled_gb:.2f} GB")
try:
    assert modeled_gb <= provisioned_gb, "the draft omitted storage overhead"
except AssertionError as error:
    print(f"AssertionError: {error}")
revised_budget_gb = 50
assert modeled_gb < revised_budget_gb
print(f"revised mapping budget={revised_budget_gb} GB; validate overhead separately")
```

**Line by line:** multiplication derives raw retained bytes; decimal conversion defines GB.
The factor models extra mapping-related storage. The assertion rejects the draft under that
assumption. The revised number leaves 13.5 GB in the mapping budget, but does not silently
provide backup or operating-system space. This is a calculation check, not a disk experiment.

Author verification on Python 3.12.10, 2026-09-22:

```text
raw=18.25 GB; modeled with overhead=36.50 GB
AssertionError: the draft omitted storage overhead
revised mapping budget=50 GB; validate overhead separately
```

## In production

Write the rejected premise and revised decision together so future reviewers know why the
change happened. Track decision thresholds: retained bytes, peak demand, error rate, or restore
time. Run a failure walkthrough before adding availability claims. Backups need tested restores;
spare capacity does not prevent host failure. Changing architecture has operational cost, so
compare a simpler alternative and state what evidence would make it preferable.

## Check yourself

### Readiness after repair

1. Which number in the worked trace is measured? Why does that matter?
2. Does buying storage fix lost acknowledgments or host unavailability?
3. What requirement changes if you choose shorter retention?

Run the arithmetic after your attempt and defend one decision aloud. Your [DESIGN.md](DESIGN.md)
must show the original weakness, revised artifact, alternative, and a concrete failure path.
Compare the [reference](REFERENCE_DESIGN.md) afterwards. Score requirements, data/API, scale,
and failure tradeoffs 0–2 each; pass at 6/8 with no unexplained source of truth. Keep 5 minutes
cold recall, 12 revision, 10 comparison/repair, and 3 critique within the existing 30 minutes.

[Navigation](README.md) · [Quick recall](../../../docs/SD_RECALL.md#day-007-week-1-design-review)
