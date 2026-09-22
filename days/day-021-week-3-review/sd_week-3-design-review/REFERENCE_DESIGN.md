# Week 3 reference review — accepted jobs survive a worker restart

Read after your cold attempt. This is an author-selected example of a weak decision from
Days 15–20, not a claim about your personal work. [CONCEPTS.md](CONCEPTS.md) teaches the review;
[DESIGN.md](DESIGN.md) remains your evidence file.

## Assumptions and requirement

Consider a hypothetical link-export service. An authenticated owner requests an export, receives
a job ID, and polls its status. Acceptance promises that the job can still be found after an
application worker restarts; it does not promise immediate success. Storage durability and
availability are explicit service dependencies. Export completion latency and workload are
unmeasured; this memo requires no invented traffic or timing targets.

## Weak decision and revised artifact

The old worker puts the job in its local map and replies accepted. That violates the promise
if the next status request reaches another worker or the original process crashes.

```text
Owner -> API worker -> shared jobs table: commit pending job + request identity
Owner <- API worker: accepted(job_id), only after commit
Job worker -> shared jobs table: claim pending work with recoverable lease
Job worker -> export storage: publish result under stable job identity
Job worker -> shared jobs table: record success + result location
Owner -> any API worker -> shared jobs table: authorize and read status
```

The job module owns job state; the link module supplies authorized export data through its
interface. A row includes job_id, owner_id, request_key, request_fingerprint, status,
lease_expiry, and result_location. Uniqueness of (owner_id,request_key) makes a matching retry
return the same job; a changed fingerprint is a conflict. Keep the record and request identity
in one transaction. The export input consistency policy must also be stated: this proposal
exports data visible when execution starts, not a snapshot at acceptance.

States are pending → running → succeeded or failed. A recoverable lease permits running →
pending when a worker disappears. Lease duration would be chosen from measured task and
heartbeat behavior; no universal duration is asserted. Terminal states remain queryable for
an explicit retention period set by the product before implementation.

## Decision and alternative

Choose asynchronous durable jobs because this hypothetical export can outlast a request.
The cost is a jobs store, status API, recovery logic, and delayed visibility. Synchronous
generation is a credible alternative for bounded small exports that fit the measured request
budget; it reduces state and operational complexity. A separate message broker is another
possible execution path, but adding it would require a transaction-safe handoff. It is not
necessary to demonstrate this revision.

## Failure walkthrough

1. The API commits job j but loses the response. The caller retries the same identity and
   payload; the durable record yields j again rather than a second export.
2. A worker claims j and crashes. The record survives. After the claim expires, recovery
   permits another attempt; duplicate execution must be tolerated.
3. If the crash follows writing the result but precedes the success update, retry uses the
   same result identity and checks/reconciles it. Conflicting output must not be published as
   a second independent user result. This is not a claim of exactly-once execution.
4. If the jobs store is unavailable before commit, the API cannot honestly return acceptance.
   An ambiguous commit requires retry/reconciliation using request identity.

## Self-review

The revised ownership preserves accepted state across the modeled worker failure. It leaves
database disaster recovery, lease timing, export consistency, and retention as explicit limits.
Next validation would kill a worker after commit and after result publication, retry through
another API instance, and verify one job identity and a recoverable status. Those are proposed
tests, not observed results. The Python model in the concepts lesson tests only ownership.
The [Day 18 reference](../../day-018-fixed-window-maximum-sum/sd_sync-versus-async/REFERENCE_DESIGN.md)
provides related handoff reasoning. This completes the assigned revision, alternative defense,
and failure walkthrough without recording learner completion.
