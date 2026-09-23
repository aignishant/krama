# Reference design — Traffic estimates

This finished reference answers [the assigned workload](README.md#assignment). The values
are hypothetical planning inputs. Your independent estimate and observations belong in
[DESIGN.md](DESIGN.md); no production traffic measurement is claimed here.

## Assumptions and requirement

- Given: 1,000,000 daily active users, each making 10 reads per day.
- Assume one incoming API request per read and a modeled 24-hour day of 86,400 seconds.
- Count shortener resolution requests at the API boundary. Destination-page requests are
  outside this count. Writes, retries, bots, and background jobs need separate workload terms.
- Peak scenario: assume 20% of daily reads occur in the busiest hour. This could represent
  users concentrated in one time zone; it is a scenario to validate, not measured behavior.

## Calculation with units

| Quantity | Calculation | Result |
| --- | --- | --- |
| Daily reads | 1,000,000 users/day × 10 reads/user | 10,000,000 reads/day |
| Average QPS | 10,000,000 reads/day ÷ 86,400 seconds/day | About 115.74 reads/second |
| Busy-hour volume | 20% × 10,000,000 | 2,000,000 reads/hour |
| Busy-hour QPS | 2,000,000 ÷ 3,600 | About 555.56 reads/second |
| Derived peak multiplier | (0.20 × 86,400) ÷ 3,600 | 4.8× the daily average |

The multiplier follows from the concentration assumption. It is not another factor to multiply
into 555.56 QPS. For planning discussion, round the two rates to roughly 116 and 556 QPS while
retaining the full inputs for later revision. The busy-hour average is not a maximum per-second rate.

```text
daily active users -> reads/user -> API requests/day -> divide by seconds -> average QPS
                                        |
                                        +-> busiest-hour share / 3,600 -> busy-hour QPS
```

## Sensitivity and decision

| Assumed share in the busiest hour | Busy-hour QPS | Multiplier |
| --- | --- | --- |
| 10% | About 277.78 | 2.4× |
| 20% | About 555.56 | 4.8× |
| 40% | About 1,111.11 | 9.6× |

Use 20% as the initial central scenario and test 40% as a more concentrated scenario. Keep the
range visible rather than turning the central case into a guarantee. A uniform-load alternative
would plan around 115.74 QPS; it is simpler but unsupported when user activity is concentrated.
Arrival measurements over the busiest intervals would determine whether either scenario is realistic.

Do not infer server count from these rates alone. First measure resource cost and achieved
latency for a representative request mix. A cached read and a storage miss can consume very
different resources. Database QPS would require separate cache-miss and operations-per-miss
assumptions; those are intentionally not invented for this assignment.

## Failure walkthrough

Assume a shared link causes 40% of the day's reads to arrive in one hour while the system was
planned around the 20% case. Hourly arrival rate doubles to about 1,111 QPS. If sustainable
capacity is below that arrival rate, queues grow and users wait or time out. Retrying can
increase work further. The estimate's average calculation remains correct; its concentration
assumption was inadequate.

Measure the actual arrival curve, queue delay, and hot-key distribution. Use bounded admission
and available capacity to limit overload while revising the plan. Any proposed cache or extra
worker capacity needs validation against the real limiting resource; this memo does not claim
that one particular remedy has already succeeded.

## Self-review

This answers average QPS and a separately justified peak multiplier. Uncertainty remains in
active-user definition, repeated reads, geography, burst intervals, and request cost. Next,
collect arrivals at minute and second granularity and measure latency under the proposed
request mix. A single busy-hour percentage is a useful starting model, not a deployment specification.

[Concept explanation](CONCEPTS.md) · [Your practice](DESIGN.md) · [Navigation](README.md)
