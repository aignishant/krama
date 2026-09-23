---
day: 21
part: "2.1"
title: "Review ownership through a failed request"
ids: [SD-21]
level: working
prerequisites: ["Days 15–20 design decisions"]
failure: true
---

# Review ownership through a failed request

Start with the cold assignment in [README.md](README.md). Open this repair lesson only
after the attempt, or record the explanation as help.

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Revise one weak decision by following an acknowledged operation across failure and recovery.

## The story

Two workers make an application look resilient until a process restart erases a job the client was told had been accepted.

## The idea in plain language

Choose your weakest prior design using your own evidence before reading this repair.
Name a user-visible promise, trace how the existing decision can violate it, revise one
diagram or memo, and defend an alternative. This lesson's job-acceptance example is a
hypothetical review choice, not a diagnosis of your work. Ownership means identifying the
authoritative home of each fact: accepting process memory is different from durable storage.

## Why Krama needs it

This develops SD-21 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

This review reuses the original design lessons linked below and their sources. Its durable-job workflow is a stated design proposal, not a claim of an executed service.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

Use the original concepts for targeted repair:
[domain model](../../day-015-sorted-pair-existence/sd_domain-model/CONCEPTS.md),
[API contract](../../day-016-unique-triples/sd_api-contract/CONCEPTS.md),
[stateless workers](../../day-017-container-capacity/sd_stateless-workers/CONCEPTS.md),
[sync/async](../../day-018-fixed-window-maximum-sum/sd_sync-versus-async/CONCEPTS.md),
[compatibility](../../day-019-longest-distinct-substring/sd_compatibility/CONCEPTS.md), and
[module boundaries](../../day-020-minimum-positive-window/sd_modular-monolith/CONCEPTS.md).

Worked failure: a worker creates job j in a local dictionary, returns accepted, then crashes.
The next worker has no j and cannot return status. Adding more workers did not preserve
the accepted fact. Revision: commit the job to a shared durable store before replying;
workers claim pending jobs and write results there. A lost response still allows a retry,
so a request identity must map to one job. A worker crash after an effect but before its
completion record still requires idempotency or reconciliation.

The changed invariant is: every accepted job has an authoritative record available after
the modeled worker failure. Durability adds a storage dependency and write latency; it does
not prove zero data loss under every database failure. Keep 5 minutes cold recall, 10 minutes
failure/concept comparison, 12 minutes revision, and 3 minutes critique. Read the
[complete reference](REFERENCE_DESIGN.md) only after the cold attempt.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
worker_memory = {'j': 'pending'}
accepted = 'j'
worker_memory.clear()  # model a worker restart
print('local-only accepted job survives:', accepted in worker_memory)
durable_store = {'j': 'pending'}  # separate authority in this model
replacement_worker = {}
print('external authority retains:', durable_store[accepted])
assert accepted not in worker_memory
assert durable_store[accepted] == 'pending'
```

**Line by line:** Clearing one dictionary models loss of one process. Keeping the authority in a separate dictionary demonstrates the ownership distinction only; no persistence engine or crash recovery has been tested.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
local-only accepted job survives: False
external authority retains: pending
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

A useful defense names the residual failure and when its alternative wins. Synchronous
completion can simplify short operations; accepted asynchronous work fits long tasks only
when a real status and recovery contract exists. Do not replace one weak decision with a
full platform redesign or claim that a reference determines your personal weakest topic.

## Check yourself

### Readiness before practice

1. What user promise does the original failure violate?
2. Where does the revised design keep the authoritative acceptance fact?
3. What remains uncertain after the effect succeeds but status is not recorded?
4. What changes would make synchronous completion preferable?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
