---
day: 15
part: "2.1"
title: "Model identity and relationships before tables grow"
ids: [SD-15]
level: working
prerequisites: ["Entities", "Uniqueness"]
failure: true
---

# Model identity and relationships before tables grow

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

Separate an owner, a link, and a click occurrence by their identities, cardinalities, and lifecycle rules.

## The story

Two people save the same destination and one person clicks twice. A design using the destination as the record identity merges records that need to remain separate.

## The idea in plain language

An entity is a thing whose identity persists even if its attributes change. A key names it
uniquely; a foreign key points to another entity. Cardinality describes how many records can
participate in a relationship. One owner can have many links; one link can have many click
events. A destination URL is an attribute shared by many links, not necessarily a unique key.
An event represents an occurrence, so two real clicks need separate event IDs even when every
other attribute matches. Begin with questions about ownership, edits, and deletion before
choosing tables or services.

## Why Krama needs it

[Day 16 API contract](../../day-016-unique-triples/sd_api-contract/CONCEPTS.md) needs an unambiguous link identity, owner, and expiry rule.

## The source behind it

[PostgreSQL 18 — Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html) documents primary, unique, and foreign-key constraints. The entity choices here are course design assumptions. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

Use this conceptual structure, then compare the [complete reference](REFERENCE_DESIGN.md):

| Entity | Identity | Relationship | Mutable facts |
| --- | --- | --- | --- |
| Owner | owner_id | One owner to many links | Account state |
| Link | link_id; unique short_code | Exactly one owner | Destination, expiry, disabled state |
| ClickEvent | event_id | Exactly one link | Occurrence facts are append-only |

A request authenticated as owner O creates link L with O as owner_id. A redirect lookup
resolves a unique short_code to L. Two clicks become events E1 and E2 pointing to L.
An edit changes L's destination, not its identity or either event ID. The model is correct
for this contract when each link has a valid owner and each event has one unambiguous link.
Database constraints can enforce references in one database; distributed event ingestion
needs an explicit validation and reconciliation policy.

Separate events cost O(number of clicks) storage but preserve occurrence detail. A counter
alone uses less storage and answers totals, while discarding timing and individual events.
Do not require a separate service merely because the diagram has a separate entity.

## When it breaks

```python
links = [("L1", "O1", "https://example.org/a"),
         ("L2", "O2", "https://example.org/a")]
by_destination = {destination: link_id for link_id, owner, destination in links}
by_id = {link_id: (owner, destination) for link_id, owner, destination in links}
print("destination keys:", len(by_destination), "identity keys:", len(by_id))
try:
    assert len(by_destination) == len(links), "destination is not unique link identity"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert len(by_id) == 2
```

**Line by line:** Two owners intentionally share a destination. The dictionary keyed by destination silently replaces one record. Keying by link_id retains both. This executed model illustrates identity loss; it is not a database constraint test.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
destination keys: 1 identity keys: 2
AssertionError: destination is not unique link identity
```

## In production

Specify deletion semantics and event retention before applying cascading deletes. A link tombstone can keep event references valid while disabling redirects. A unique short-code constraint resolves allocation races; a prior availability check cannot. A retry of the same delivered click event should reuse its event ID, while a new real click gets a new ID. Privacy and retention policies need actual product requirements.

## Check yourself

### Readiness before practice

1. Why can two links share a URL without sharing identity?
2. Which relationships are one-to-many?
3. What distinguishes two clicks from one event delivered twice?
4. What happens to events when a link is disabled?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
