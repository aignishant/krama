---
day: 22
part: "2.1"
title: "Put data rules at the write boundary"
ids: [SD-22]
level: working
prerequisites: ["Day 15 domain identities; tables and keys"]
failure: true
---

# Put data rules at the write boundary

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Use constraints for facts that must stay true for every write, and choose lookup indexes from separate access patterns.

## The story

Two requests both check that a short code is unused and then insert it. A read-before-write check alone cannot protect uniqueness under concurrent writers.

## The idea in plain language

A table row represents an entity. A primary key identifies it; UNIQUE prevents repeated
key values; NOT NULL requires a value; a foreign key requires an existing referenced key.
For this design, each link has one owner and a globally unique non-null code. Many links
may share an owner or destination. A foreign key protects existence, not whether the caller
is authorized to act for that owner. A product invariant and a useful lookup path are
different decisions even when the database implements a constraint with an index.

## Why Krama needs it

This develops SD-22 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[PostgreSQL 18 constraints](https://www.postgresql.org/docs/18/ddl-constraints.html) documents primary, unique, non-null, and foreign-key semantics. The link product rules are explicit assumptions.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

Map the product rules before choosing SQL:

| Rule | Proposed database artifact | Why |
| --- | --- | --- |
| Owner has stable identity | owners.id PRIMARY KEY | One referenced entity |
| Link has stable identity | links.id PRIMARY KEY | Edits preserve identity |
| Code maps to one link globally | code NOT NULL UNIQUE | No ambiguous redirect |
| Every link belongs to an existing owner | owner_id NOT NULL REFERENCES owners(id) | No orphan ownership |
| Owner listing should be fast | A separate candidate index on owner/time | Performance, not validity |

Race trace: A checks code `spruce`, B checks the same code, both see absent, A inserts,
B inserts. Without enforced uniqueness, two rows satisfy the application's local check.
A database uniqueness constraint makes the second conflicting committed value unacceptable.
The service must handle the conflict and return a documented response or choose another code.
Two sequential application checks do not reproduce the concurrent race.

The [reference](REFERENCE_DESIGN.md) supplies complete proposed PostgreSQL DDL and deletion
policy. Non-null identity fields avoid treating missing values as real keys. PostgreSQL's
ordinary unique constraint can otherwise admit multiple nulls. Keys incur index storage and
write maintenance. A foreign key on links.owner_id does not automatically create a lookup
index on that referencing column; assess that path separately.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
rows = []
a_saw_free = not any(row['code'] == 'spruce' for row in rows)
b_saw_free = not any(row['code'] == 'spruce' for row in rows)
if a_saw_free:
    rows.append({'code': 'spruce', 'owner': 1})
if b_saw_free:
    rows.append({'code': 'spruce', 'owner': 2})
print('check-then-insert duplicates:', len(rows))
assert len({row['code'] for row in rows}) < len(rows)

accepted_codes = set()
def constrained_insert(code):
    if code in accepted_codes:
        raise ValueError('duplicate code')
    accepted_codes.add(code)

constrained_insert('spruce')
try:
    constrained_insert('spruce')
except ValueError as error:
    print('serialized rule model:', error)
assert accepted_codes == {'spruce'}
```

**Line by line:** Both prechecks run before either insert, deliberately modeling an interleaving. The second half models a serialized uniqueness decision; this Python function is not itself a concurrent database substitute.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
check-then-insert duplicates: 2
serialized rule model: duplicate code
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Decide owner deletion explicitly. RESTRICT rejects deletion while links remain; CASCADE
would remove dependent rows and needs a product justification. A single-row CHECK cannot
enforce every cross-row business rule. Application validation remains useful for good errors
and URL policy, but it complements authoritative integrity checks. Inspect existing data
before proposing a migration that assumes the new constraints already hold.

## Check yourself

### Readiness before practice

1. Why can two successful prechecks still produce duplicates?
2. Which rule permits many links per owner?
3. Why does an owner foreign key not prove caller authorization?
4. Which proposed index is about lookup cost rather than product validity?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
