---
day: 19
part: "2.1"
title: "Evolve responses without changing old meanings"
ids: [SD-19]
level: working
prerequisites: ["Day 16 API contract; absent versus explicit values"]
failure: true
---

# Evolve responses without changing old meanings

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

An optional field is compatible only when old clients tolerate it and existing fields and behavior retain their meanings.

## The story

A server adds an expiration timestamp. One old client ignores it, another rejects unknown
keys, and a third assumed links never expire. The JSON change is small; their outcomes differ.

## The idea in plain language

Compatibility has several dimensions: parsers must accept the shape, compiled or generated
interfaces must still work, and behavior must meet earlier expectations. Adding a response
field is not enough evidence for all three. Read the original [API contract](../../day-016-unique-triples/sd_api-contract/CONCEPTS.md)
and identify concrete clients before promising a safe rollout.

Absence, null, and a timestamp can carry three different meanings. Choose those meanings
explicitly and test a client/server matrix, including new clients talking to old servers.
This exercise evolves a read response that previously omitted expiry; it does not change
Day 16's create contract, where expires_at is a required input.

## Why Krama needs it

This develops SD-19 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[AIP-180 — Backwards compatibility](https://google.aip.dev/180) separates source, wire,
and semantic compatibility and warns against changing established behavior. The example
field policy and rollout choices here are authored for this hypothetical service. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

For this read API choose: absent means expiry information is not supplied, null means
explicitly no scheduled expiry, and an offset-qualified timestamp means a scheduled expiry.
New clients display unknown for absent, never infer permanence, and let the server decide
whether redirecting is currently allowed. For links created under Day 16, the new server
supplies a timestamp; null is reserved for legacy permanent records if those exist.

| Client / server | Old server omits field | New server supplies optional field |
| --- | --- | --- |
| Old tolerant reader | Existing behavior | Ignores new key; existing behavior |
| Old strict reader | Existing behavior | May fail; test before rollout |
| New reader | Shows expiry unknown | Handles absent, null, and timestamp |

This matrix defines both deployment and rollback obligations. Deploy tolerant new clients
before relying on the new field; use a compatible versioned representation for strict legacy
clients if they cannot be upgraded. Keep all old required fields, types, and values intact.
Adding metadata about already-existing expiry is different from introducing expiry to links
that were promised to be permanent.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.
For SD, it is a local model of a failure, not a running service or a production measurement.

```python
old = {"id": "L1", "short_url": "https://s.example/c1"}
new = dict(old, expires_at="2026-09-23T00:00:00Z")
def strict_reader(payload):
    if set(payload) != {"id", "short_url"}:
        raise ValueError("unexpected response field")
    return payload["short_url"]
print("old response:", strict_reader(old))
try:
    strict_reader(new)
except ValueError as error:
    print(f"ValueError: {error}")
def tolerant_reader(payload):
    return payload["short_url"]
assert tolerant_reader(new) == tolerant_reader(old)
missing = object()
assert old.get("expires_at", missing) is missing
assert {"expires_at": None}.get("expires_at", missing) is None
print("repair:", tolerant_reader(new), "absence differs from null")
```

**Line by line:** The strict reader rejects the additional key even though old keys remain unchanged.
The tolerant reader reads only its required field. A distinct sentinel distinguishes absence
from explicit null; using get without a sentinel would collapse these two states.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
old response: https://s.example/c1
ValueError: unexpected response field
repair: https://s.example/c1 absence differs from null
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

Test representative released clients and generated decoders with fixtures for every
presence state, then canary server emission with client-error telemetry and a rollback switch.
Optional does not mean clients may ignore a field that changes authorization or accounting.
If a field affects cache representations, include representation selection in cache keys.
Avoid field renames disguised as additions followed immediately by deleting the old field.

## Check yourself

### Readiness before practice

1. Which old client in the matrix breaks on an added key?
2. Why must a new client tolerate a missing field during rollback?
3. What is the difference between unknown expiry and no scheduled expiry?
4. Would expiring formerly permanent links be only a schema change?

Compare the [complete reference answer](REFERENCE_DESIGN.md) before guided practice or after your own attempt.

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
