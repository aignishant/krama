# Reference design — Storage decision memo

This is the assistant's completed answer to the [assignment](README.md#assignment).
[DESIGN.md](DESIGN.md) remains your personal practice. Assumed scenarios are not production observations.

## Requirements and assumptions

Choose a storage baseline for a redirect service that currently fits one database primary.
No measured throughput or latency is available. The three access patterns are (1) lookup by
unique code, (2) create a link with an owner-scoped retry token, and (3) list one owner's newest
links using a timestamp/id cursor. Analytics are outside this memo and can have a separate model.

Two failure requirements govern the choice. First, a lost response after a committed create
must let a retry recover the same link, not create another. Second, cleanup delay must never
make an expired link eligible for a redirect. Do not interpret a database outage as a missing
code. Durable success means the selected database durability policy has completed before success;
actual failover data-loss tolerance still needs an explicit deployment decision.

## Proposed artifact and decision

Choose a relational primary with these logical structures:

| Structure | Enforcement or query |
| --- | --- |
| links: id, code, owner_id, destination, created_at, expires_at, active, version | authoritative link state |
| unique(code) | one stored mapping per code |
| create_requests: unique(owner_id, request_id), payload_fingerprint, link_id | retry identity and original result |
| index(owner_id, created_at DESC, id DESC) | deterministic newest-owner listing |

Create the request record and link in one transaction. A concurrent request-token conflict
must recover the committed link and compare the payload fingerprint; a changed payload under
the same token is a conflict, not a new create. Retry records must survive the documented retry
window, or older retries must be explicitly rejected. A random code collision retries code
allocation under its own uniqueness constraint; it must not silently reuse another owner's link.

Redirect reads fetch by code and evaluate active and expiry. Owner listings derive owner from
authorization and use (created_at,id) for tie-breaking. Version-checked edits prevent silent
lost updates when editing is added. This single transaction domain is a simpler initial fit for
the three patterns than maintaining separate eventually consistent lookup representations.

## Credible key-value alternative

Use code-keyed link items, a retry-token mapping, and an owner-ordered secondary access path.
Conditional writes enforce uniqueness, but retry mapping and link creation need a transaction
or another explicit recovery protocol. A projection for owner listing has a freshness and
rebuild contract. This alternative may fit a measured keyed workload exceeding the relational
baseline, but it is not automatically more available, durable, or free of hot keys. Compare
the specific product's guarantees and total maintenance work before switching.

## Failure walkthrough

Request r creates code c and commits its retry record, but the response is lost. The client
retries r. The unique retry key resolves to c; matching payload returns the same result. A
different payload returns conflict. Later c expires while cleanup is down. Redirect evaluation
returns absence at or after the deadline even though c remains stored. If storage times out,
return a retryable service error; do not persist a false not-found conclusion in a cache.

## Self-review and change criteria

The choice covers all three patterns and names enforcement for both failure requirements.
Next measure peak keyed reads, owner-list skew, write contention, data growth, and recovery.
Reconsider if measured workload exceeds the tuned baseline or required distribution cannot be
met within its operational budget. The artifact is a proposal, not executed SQL, a benchmark,
or a claim that a specific key-value service lacks transactions.


## Sources and comparison

[PostgreSQL Multicolumn Indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html) and [partition-key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) support the access-path tradeoffs. The recommendation is conditional on the stated workload.
Checked 2026-09-23. See [the concept lesson](CONCEPTS.md) for the worked mechanism and
executed teaching model, and [the source ledger](../../../docs/SOURCES.md) for provenance.
