# Reference design — Latency budgets

This worked answer addresses [the 200 ms assignment](README.md#assignment). Every allocation
is hypothetical; no service has been benchmarked here. Use it as guidance and keep your own
attempt, critique, and observations in [DESIGN.md](DESIGN.md).

## Assumptions and requirement

Assume a link-resolution interaction with an end-to-end p95 target of 200 ms. Measure from
the client starting a short-link request to receiving the complete redirect response. Fetching
the destination page is outside this boundary. Assume one serial storage lookup, no retry,
and no parallel dependency in this first model.

The population is successful eligible resolution requests over an assumed rolling 30-day
window, measured from a representative client sample. Report errors and timeouts separately
so excluding them from successful-request latency cannot conceal a failing service.

## Proposed allocation

| Component | Assumed allocation | Included work |
| --- | --- | --- |
| Client | 20 ms | Request preparation and response handling, excluding time waiting on the network |
| Network | 40 ms | Total outbound and return transit, with setup behavior represented by the assumed workload |
| App | 50 ms | App queueing, code lookup preparation, response construction; excludes storage wait |
| Storage | 60 ms | Storage request queueing and lookup through response |
| Shared margin | 30 ms | Slack for variation and smaller costs needing later measurement |
| Total | **200 ms** | End-to-end modeled budget |

These are allocations toward a target, not claims that the four components achieve these p95
values. Margin is reserved room, not another operation the request executes.

```text
client prepare -> outbound network -> app work -> storage -> app work -> return network -> client handle
|------------------------------------ end-to-end -----------------------------------------------|
```

For one synthetic request, assume client=15, network=32, app=38, and storage=55 ms. Its total
is 140 ms, leaving 60 ms under the target. This checks one path's arithmetic, not its p95.
If an app span includes the storage call, adding that inclusive span to storage again would
double count. Use nonoverlapping durations or measure the outer interaction directly.

## Why summing component p95 values is only a rough budget

A component's 95th-percentile observation need not belong to the same request as another
component's. Consider 20 synthetic paired requests: app takes 10 ms on 19 and 100 ms on one;
storage does the same, but on a different request. Under the nearest-rank rule, each component
p95 is 10 ms. Eighteen totals are 20 ms and two are 110 ms, so end-to-end p95 is 110 ms,
not the sum of component p95 values, 20 ms.

This counterexample is executed in [the concept lesson](CONCEPTS.md#when-it-breaks). Component
targets help assign responsibility, but only paired request totals or direct end-to-end
observations can verify the stated end-to-end distribution. Parallel calls would require
tracing dependencies rather than adding every span.

## Decision and alternative

Use one simple lookup path with explicit app/storage boundaries and 30 ms shared margin.
Measure queueing and the complete client journey before reallocating the budget. An alternative
is a cache for frequently resolved codes; it can reduce storage-path work but introduces a
freshness decision for created or disabled links. Prefer it only after measurements show a
useful hit rate and the product accepts or addresses stale status reads.

Another valid allocation could give more time to network travel for distant clients. That
would require reducing other allocations, changing placement, or revisiting the target; it
cannot be obtained by renaming the same total.

## Failure walkthrough

Assume storage queueing raises storage duration to 110 ms while client, network, and app use
their full 20, 40, and 50 ms allocations. The total is 220 ms: 20 ms above the target, after
consuming the 30 ms margin. This request is slow, but one such event alone does not prove a
p95 violation; its frequency matters.

Trace the queue rather than blaming only query execution. Evaluate admission limits, query
cost, or measured cache benefit against the bottleneck. Propagate the remaining deadline when
implementing timeouts; giving each stage a new 200 ms timeout does not preserve a 200 ms
end-to-end limit. Test the selected remedy and measure the resulting full-path distribution.

## Self-review

The allocation sums to 200 ms and its measurement boundary is explicit. Uncertainties include
client geography, connection reuse, storage hit/miss mix, and queueing under bursts. Next,
collect paired traces and a representative end-to-end latency distribution, alongside errors
and timeouts. The design is a complete proposal; target attainment remains unmeasured.

[Concept explanation](CONCEPTS.md) · [Your practice](DESIGN.md) · [Navigation](README.md)
