# Reference design — Connection budgets

Author-written answer to the 200-requests/20-workers assignment. All limits beyond those supplied
in the task are stated planning assumptions. No connection counts or throughput were measured.
Keep your own artifact and evidence in [DESIGN.md](DESIGN.md).

## Assumptions and requirement

There are 20 application worker processes, each allowing 200 in-flight requests. Each process
owns its pools. For a conservative DB-demand scenario, all requests need one DB connection at
once, without parallel queries. Incoming connections use one active request per connection in
this simplified HTTP/1.1 model; idle keep-alive connections would be additional.

Assume a DB ceiling of 500 connections and reserve 100 for administration, other services, and
margin. The application allocation is 400. Plan for at most 25 simultaneous worker processes
during rolling replacement. A per-process pool of 16 with zero overflow fits that peak.

## Calculation and separate pools

| Quantity | Calculation | Interpretation |
| --- | --- | --- |
| In-flight requests | 200 requests/worker × 20 workers = 4,000 requests | Concurrency, not throughput |
| Unbounded DB demand | 4,000 requests × 1 DB connection/request = 4,000 connections | Worst-case simultaneous demand assumption |
| App DB allocation | 500 − 100 = 400 connections | Chosen total application cap |
| Pool at rollout ceiling | floor(400 / 25) = 16 connections/worker | No overflow allowed |
| Normal fleet DB maximum | 20 × 16 = 320 connections | 80 app-allocation slots remain for rollout |
| Rollout maximum | 25 × 16 = 400 connections | Fits the application allocation |

At a normal worker, 200 simultaneous DB requests exceed 16 active checkouts by 184. Choose an
illustrative waiting-queue cap of 40 and a 50 ms maximum checkout wait, bounded further by the
request's remaining deadline. With no completions during the arrival burst, 16 execute, 40 wait,
and 144 receive a declared temporary-overload response. Queue length and wait targets need load testing.

```text
Clients -> proxy/incoming socket limit -> worker request admission
                                          |-> HTTP pool per destination
                                          |-> DB pool (16, no overflow) -> shared DB
                                          |-> cache pool -> cache service
```

Incoming sockets, outbound sockets, DB sessions, and cache clients consume distinct pools.
HTTP/2 can multiplex request streams; it invalidates the one-request/connection assumption.
Fan-out to two simultaneous DB operations would double per-request DB demand in the conservative
scenario. Local OS file descriptors cover several of these resources together, so the separate
pool budgets also need a combined process-level check.

## Decision and alternative

Choose per-process caps based on the maximum rollout fleet, bounded waiting, and admission
rejection. This sacrifices some normal-fleet DB concurrency to preserve the shared limit during
replacement. It avoids assuming that more workers justify more DB sessions.

A connection proxy could multiplex client sessions over fewer database connections, but transaction
and session-state behavior must be compatible with its pooling mode. I would evaluate that if
process count becomes large or measured short transactions leave many direct sessions idle.
Increasing the DB ceiling alone is not evidence that memory or query throughput can support it.
[PostgreSQL's connection documentation](https://www.postgresql.org/docs/16/runtime-config-connection.html)
is the reference for server limits and reservations; 500 is our assumption, not a default claim.

## Failure walkthrough

An operator scales to 30 workers without revising the allocation. Thirty pools of 16 permit 480
connections, consuming reserved capacity and violating the application's 400-connection budget.
Gate the rollout at 25 or revise the allocation before admitting new workers. Existing sessions
do not disappear instantly when configuration changes; drain them deliberately.

A leaked checkout can leave every slot occupied and make all later requests wait. Release leases
on every exit path and monitor checkout wait separately from query execution. Pool timeout should
return a temporary failure within the request budget, rather than append to an unlimited queue.

## Self-review

The required demand estimate is 4,000 connections only under the one-simultaneous-DB-checkout
assumption. Independent pools, process count, overflow, rollout headroom, and rejection are explicit.
Next I would inventory actual pool ownership, protocol multiplexing, DB use fraction, transaction
duration, file-descriptor limits, and other clients. The 50 ms wait and 40-request queue are design
choices needing validation, not measured safe values.

[Concepts](CONCEPTS.md) · [Acceptance](README.md#acceptance-check) · [Personal practice](DESIGN.md)
