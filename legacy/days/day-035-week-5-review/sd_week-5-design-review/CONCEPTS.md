---
day: 35
part: "2.1"
title: "Week 5 design review"
ids: [SD-35]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Week 5 design review

Cold review: attempt [the assignment](README.md) first. Use this lesson afterwards for repair; record any help.

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

A design review repairs one weak decision by connecting an observable invariant to its enforcement and failure path.

## The story

A diagram labels the system “balanced,” but one viral link still overloads its owner. The review must change a decision, not add another box with no effect on that request.

## The idea in plain language

Attempt your weakest Days 29–34 design decision cold, then read this repair lesson.
The relevant tools are [tree indexes](../../day-029-stable-record-sorting/sd_tree-indexes/CONCEPTS.md), [log-structured storage](../../day-030-merge-overlapping-intervals/sd_log-structured-storage/CONCEPTS.md),
[access patterns](../../day-031-insert-an-interval/sd_access-pattern-modeling/CONCEPTS.md), [hot partitions](../../day-032-minimum-meeting-rooms/sd_hot-partitions/CONCEPTS.md),
[expiration](../../day-033-kth-smallest/sd_ttl-and-deletion/CONCEPTS.md), and [the storage memo](../../day-034-count-inversions/sd_storage-decision-memo/CONCEPTS.md).
An invariant states what must remain true. An enforcement point names the read, write, or
recovery step that preserves it. A diagram without that connection cannot defend correctness.

## Why Krama needs it

This develops SD-35. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

The primary references for repair are [partition-key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) and [expired-item behavior](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ttl-expired-items.html).
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Within 30 minutes, use the first 5 for cold recall and the 12-minute design block for your
own revision before consulting repair material. Spend the 10-minute concept/reference window
afterwards, then 3 minutes critiquing. Choose one weak decision; do not redo all six assignments.

For an illustrative expiry gap, the old claim is “cleanup removes expired records.” The
counterexample is a read after the deadline but before cleanup. The revised artifact adds an
eligibility predicate to database and cache read paths, while cleanup remains asynchronous.
The alternative is synchronous removal at the deadline, which still needs failure handling
and does not automatically remove every cached copy. The invariant is no redirect with
observed time>=expires_at; clock authority and stale-copy rules are explicit assumptions.

Audit the revision with one normal request, one failure timeline, one alternative, and one
next verification. Other valid choices include compaction backlog, replayed aggregate events,
and partition overload. Score requirements, data/API, scale, and failure tradeoffs 0–2 each;
the design gate needs 6/8 with no unexplained source of truth. The reference is a completed
example choice, not a claim to know your personal weakest area.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
expiry, cleanup, read = 100, 150, 120
old_rule_serves = read < cleanup
revised_rule_serves = read < expiry
print('old cleanup rule serves:', old_rule_serves)
print('revised deadline rule serves:', revised_rule_serves)
assert old_rule_serves and not revised_rule_serves
assert 99 < expiry and not (100 < expiry)
```

**Line by line:** One schedule separates cleanup time from serving eligibility. The two boundary assertions make equality part of the contract, so the repair is falsifiable rather than a vague instruction to clean up faster.

Observed author output on Python 3.12.10, 2026-09-23:

```text
old cleanup rule serves: True
revised deadline rule serves: False
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Retain the original decision and why it failed, then state the smallest change addressing
that failure. A review should expose unsupported capacity claims and untested recovery paths.
Do not turn an illustrative Python schedule into a production incident report. Optional
depth: turn the next verification into a controlled integration experiment in a later session.

## Check yourself

### Readiness before practice

After attempting: which invariant was missing, where is it now enforced, and what failure could still violate it? What alternative did you reject under the same assumptions?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.

Compare [the complete reference](REFERENCE_DESIGN.md); [DESIGN.md](DESIGN.md) is your own practice.
