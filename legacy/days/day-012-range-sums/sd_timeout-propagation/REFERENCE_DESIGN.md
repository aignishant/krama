# Reference design — Timeout propagation

This author-written answer supplies the three-hop diagram, one overall deadline, per-hop limits,
and cancellation behavior. The timeline is a design example, not measured execution. Use
[DESIGN.md](DESIGN.md) for your independent version and evidence.

## Assumptions and requirement

The three request hops are client → gateway A → application B → dependency C. The client's
overall lifetime is 500 ms measured from request start, including outbound and return travel.
All timestamps below use one conceptual elapsed timeline for illustration; they are not wall-clock
timestamps transmitted between hosts. Client and infrastructure support cancellation propagation.
C may consult a database internally; that operation remains under C's inherited deadline.

## Budget and call artifact

| Boundary | Dispatch time | Parent deadline | Response reserve | Local cap | Effective child deadline |
| --- | --- | --- | --- | --- | --- |
| Client → A | t=0 | t=500 | Included in end-to-end policy | 500 ms | t=500 |
| A → B | t=40 | t=500 | 40 ms for A's return work/travel | 350 ms | t=40 + min(350, 500−40−40) = 390 |
| B → C | t=100 | t=390 | 30 ms for B's return work/travel | 220 ms | t=100 + min(220, 390−100−30) = 320 |

The initial 40 ms includes client-to-A transit, admission, and A's local work in this example.
B's child dispatch occurs 60 ms later, including A-to-B transit, B queueing, and B local work.
The reserves and caps are proposed allocations needing measurement; unused slack remains with
the parent. If actual dispatch is later, recompute using the actual remaining budget.

```text
Client (expires t=500)
  -> A (t=0 request begins; downstream dispatch t=40)
       -> B (must answer A by t=390; downstream dispatch t=100)
            -> C (must answer B by t=320)
                 -> DB/pool work bounded by C's remaining time
            <- result or cancellation/failure
       <- B returns within its inherited budget
  <- A reserves time to finish the client response
```

C includes pool checkout and query execution in its remaining budget and stops launching work
when that budget is exhausted. Every caller checks remaining time before a retry; no retry gets
a fresh 500 ms. The deadlines are nested. Summing 500+350+220 is not a valid latency calculation.

## Decision and alternative

Choose inherited remaining time plus local caps and return reserves. This constrains total work
while allowing a fast hop to leave slack for later work. Independent fixed timeouts are simpler
to configure, but they allow an inner call to outlive its caller and waste scarce connections.
I would keep a local timeout only as a tighter bound within the remaining request lifetime.

Use the transport's supported propagation mechanism and local monotonic timers. The gRPC
[deadline guide](https://grpc.io/docs/guides/deadlines/) describes remaining-time propagation;
language support must be checked for the chosen implementation. An ordinary HTTP chain needs
an explicit trusted contract and middleware rather than assuming that a timeout header is universal.

## Cancellation and failure walkthrough

Suppose the client cancels at t=250 while C waits for a DB connection. A cancels its B call; B
cancels C; C removes its queued checkout and avoids issuing a query. Each layer releases resources
it owns. In-flight query cancellation depends on the driver/server; a handler must cooperate and
must not return a still-busy connection for unrelated reuse. Signal propagation is not instantaneous.

If the client remains connected but C reaches t=320 without a result, B stops waiting and cancels
C's remaining work. B maps the dependency timeout to its declared failure, and A can return a
gateway timeout response while overall time remains. Cleanup should not require another unbounded wait.
The [cancellation guide](https://grpc.io/docs/guides/cancellation/) explains why handler work may
need explicit cancellation checks even after an RPC is cancelled.

If C committed a write at t=245 before cancellation at t=250, the write stays committed. The caller
has an uncertain outcome, not proof of rollback. Retry with the same operation identity and
reconcile using [Day 10's design](../../day-010-pair-sum-indices/sd_idempotency-semantics/REFERENCE_DESIGN.md).

## Self-review

The three hops, single lifetime, smaller nested budgets, and downstream cancellation are explicit.
The model assumes cancellation-aware infrastructure and cannot guarantee exact timer firing or
that a remote query terminates immediately. Next I would inject delay separately into admission,
pool wait, connect, and execution; verify cancellation reaches each layer; and check that connection
leases return without corrupting their protocol state. Measure return-path latency before adopting
the 40/30 ms reserves. The teaching arithmetic is not a network or cancellation integration test.

[Concepts](CONCEPTS.md) · [Acceptance](README.md#acceptance-check) · [Personal practice](DESIGN.md)
