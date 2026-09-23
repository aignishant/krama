# Reference design — Storage estimates

This is a complete worked answer to [the daily assignment](README.md#assignment). All
overheads and capacity choices are explicit assumptions. Read or compare this answer; keep
your own calculations and evidence in [DESIGN.md](DESIGN.md).

## Assumptions and requirement

Given 100,000 new links per day and 500 bytes per record, calculate one-year raw storage,
then account separately for indexes and replication.

Assume a 365-day year, no initial backlog, constant daily creation, no deletion during that
year, and no compression. The 500 bytes represents logical record data, excluding indexes,
logs, and storage-engine overhead. Use decimal GB, where 1 GB is 1,000,000,000 bytes.

For an illustrative capacity decision, assume indexes consume 30% of raw bytes, every live
copy stores both data and indexes, and the replication factor is three total copies. Assume
the live data/index footprint should occupy at most 70% of provisioned capacity. These values
are planning choices, not measured properties of a selected database.

## Calculation with units

| Layer | Calculation | Result |
| --- | --- | --- |
| Records after one year | 100,000 records/day × 365 days | 36,500,000 records |
| Raw logical storage | 36,500,000 × 500 bytes | 18,250,000,000 bytes = **18.25 GB** |
| Assumed index storage per copy | 18.25 GB × 0.30 | **5.475 GB** |
| Data plus indexes, one copy | 18.25 + 5.475 | **23.725 GB** |
| Three total live copies | 23.725 × 3 | **71.175 GB** |
| Capacity at 70% use | 71.175 ÷ 0.70 | About **101.68 GB** total |

For the replication breakdown, data accounts for 54.75 GB and indexes for 16.425 GB across
the three copies. The two additional copies add 47.45 GB beyond the original data/index copy.
Replication factor three means the original plus two others, not four copies.

The 101.68 GB figure is an aggregate live-data/index planning floor under these assumptions.
If stored as three full copies on three equally sized nodes, it corresponds to about 33.89 GB
per node before accounting for omitted categories. It is not a finalized disk purchase recommendation.

```text
new records/day × retained days × bytes/record -> raw bytes
raw bytes + per-copy indexes -> one-copy footprint
one-copy footprint × total copies -> occupied live storage
occupied live storage / target utilization -> modeled capacity
```

## Decision and alternative

Keep raw data, indexes, and replicas as separate terms so actual measurements can replace
one estimate without rewriting the model. Maintain headroom instead of provisioning exactly
the occupied footprint. Backups, transaction logs, temporary rewrites, metadata, and old row
versions still need explicit estimates; unspecified headroom does not demonstrate they fit.

An alternative 90-day retention policy would retain 9,000,000 records and 4.5 GB raw under
steady creation and prompt reclamation. At the same illustrative index and copy factors it
would occupy 17.55 GB. This saves space but expires older links or requires a separate archive.
Choose it only if the product accepts that changed lifetime; the assigned one-year estimate
continues to use 365 days.

## Failure walkthrough

Suppose a one-year retention policy is adopted, but expiry cleanup stops for 30 additional
days after reaching steady state. Another 3,000,000 records accumulate: 1.5 GB raw, or 5.85 GB
including the assumed 30% indexes and three copies. Logical deletion without physical space
reclamation can produce a similar capacity surprise.

If remaining space is exhausted, new link creation can fail even while many reads continue.
Monitor growth and reclamation, restore cleanup, and provide safe working capacity before
attempting a large rewrite. A cleanup repair needs verification that space is actually reclaimed;
marking records expired is not that verification. This is a hypothetical failure analysis.

## Self-review

The answer supplies the raw one-year result and a transparent overhead breakdown. Next, measure
serialized and on-disk record sizes, actual index sizes, log growth, and reclamation delay.
Verify recovery storage and replica placement separately. Replicas can repeat an accidental
deletion, so their capacity alone does not establish backup or recovery capability.

[Concept explanation](CONCEPTS.md) · [Your practice](DESIGN.md) · [Navigation](README.md)
