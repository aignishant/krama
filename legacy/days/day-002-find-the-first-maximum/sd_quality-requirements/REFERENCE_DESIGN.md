# Reference design — Quality requirements

An author-written response to [the assignment](README.md#assignment). Every numerical target
below is an **assumption for discussion**, not a benchmark or achieved guarantee. Read this
for guidance; put your own reasoning and evidence in [DESIGN.md](DESIGN.md).

## Assumptions and requirement

Use [Day 1's shortener scope](../../day-001-count-target-values/sd_functional-scope/REFERENCE_DESIGN.md):
create a mapping, resolve an active link, and let its owner disable it. Initially assume one
serving region and no client-side offline operation. Define separate indicators for resolution
and creation so a large read volume cannot hide failing writes.

## Proposed targets and measurement boundaries

| Property | Assumed target | Population, boundary, and interpretation |
| --- | --- | --- |
| Availability | At least 99.9% good outcomes over a rolling 30-day window, separately for creates and resolutions | Eligible syntactically valid requests reaching the service gateway; expected unknown/disabled-link responses count as correct resolutions; internal errors and service timeouts count as failures |
| Latency | Successful resolution p95 at most 200 ms over the same window | A sampled client population, from request initiation to complete redirect response; excludes fetching the destination page; successful requests only, with failure/timeout rates reported alongside |
| Durability | Zero acknowledged mapping losses in the assumed single-server failure model over the 30-day window | Acknowledged creates must remain recoverable after recovery from one server loss; attempted but unacknowledged creates are tracked separately |
| Freshness | At least 99.9% of acknowledged creates/disables visible to resolution reads within 2 seconds over the window | Measure from update acknowledgement to observed visibility at serving readers; a disable affects new resolutions, not responses already delivered |

All counts, windows, and thresholds in this table are hypothetical design inputs. The
availability boundary omits failures before a request reaches the gateway; client-side probes
are needed to detect that blind spot. Do not label this gateway indicator whole-internet availability.

## Measurement trace

```text
client starts request -> gateway accepts -> lookup -> redirect bytes received by client
|--------------------------- resolution latency --------------------------|

owner update -> stored change -> acknowledgement -> reads observe new state
                                 |----------- freshness delay -----------|
```

For an illustrative availability calculation, assume 100,000 eligible resolution attempts
in a window and 70 internal errors/timeouts. There are 99,930 good outcomes:
`99,930 / 100,000 = 99.93%`, which passes the assumed 99.9% gateway target. These are synthetic
counts. They neither establish the latency target nor prove that every location was reachable.

Durability has a different check: acknowledge a set of mappings, simulate the stated server
loss, recover, and compare recovered records with that acknowledged set. No such experiment
has been performed here. A successful HTTP response alone is not durability evidence.

## Decision and alternative

Choose a small bounded freshness delay rather than promising immediate global visibility.
This leaves room for read-path optimization, but stale reads after a disable can still redirect
briefly. If links must be withdrawn immediately for the product's use case, strengthen the
requirement and require a read path that checks authoritative status before redirecting.

For durability, acknowledgement must depend on storage surviving the stated failure model.
A cheaper local-only acknowledgement policy could lose accepted mappings on server loss;
that alternative is incompatible with the proposed target. Storage mechanisms will be chosen
in later sessions rather than assumed proven by this memo.

## Failure walkthrough

An owner disables a link. The update succeeds, but a serving reader still sees an old active
mapping three seconds later. The redirect can be fast and the request can receive a response,
yet the two-second freshness target is missed. Preserve the disable in authoritative state,
repair or bypass stale readers, and measure visibility delay. Compare against the freshness
target instead of calling a fast response healthy. Three seconds is an illustrative scenario.

## Self-review

The largest uncertainties are client geography, the cost of stronger acknowledgement, and
whether delayed disable visibility is acceptable. Next, agree on those product choices, collect
request and visibility distributions, and test the explicit failure model. The targets are
defined; achievement remains unmeasured. Other values can be defensible with stated reasons.

[Concept explanation](CONCEPTS.md) · [Your practice](DESIGN.md) · [Navigation](README.md)
