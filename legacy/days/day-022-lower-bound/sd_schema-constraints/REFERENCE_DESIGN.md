# Schema reference — owners and links

This is a complete proposed answer to today's schema task. SQL is an authored PostgreSQL 18
artifact, not an executed migration. [CONCEPTS.md](CONCEPTS.md) explains the rules;
[DESIGN.md](DESIGN.md) belongs to your practice.

## Assumptions and product rules

Every link has one existing owner. A case-sensitive short code is globally unique and cannot
be empty. Link identity survives destination edits. Different links may share a destination,
and one owner may create many links. Owner deletion is rejected while links remain. Creation
time is stored with time-zone semantics and never intentionally edited by this application.
These are chosen product rules, not inferred universal URL-shortener requirements.

## Proposed schema

```sql
CREATE TABLE owners (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    display_name text NOT NULL
);

CREATE TABLE links (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_id bigint NOT NULL REFERENCES owners(id) ON DELETE RESTRICT,
    code text COLLATE "C" NOT NULL UNIQUE CHECK (length(code) > 0),
    destination_url text NOT NULL CHECK (length(destination_url) > 0),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

The primary keys provide stable identity. The code constraint enforces one redirect identity
even if requests race. The explicit C collation makes the code comparison case-sensitive for
this design. The owner foreign key prevents orphan rows, while NOT NULL disallows unowned links.
The length checks reject empty strings; they do not establish URL validity. The application
separately validates the accepted URL schemes and syntax and derives owner_id from authorization.
Foreign-key existence alone would not stop a caller from naming another existing owner.

Product rules and lookup needs are distinct:

| Artifact | Purpose | Deliberately not implied |
| --- | --- | --- |
| links.code UNIQUE | Global code identity; also supports exact lookup | Unique destination URLs |
| links.owner_id foreign key | Valid ownership reference | One link per owner or caller authorization |
| Proposed owner/time index on Day 23 | Fast ordered owner listing | A new validity rule |

PostgreSQL creates supporting unique indexes for primary/unique constraints. It does not
automatically create an index on the referencing owner_id column. Its ordinary unique-null
behavior is avoided here by requiring code. These semantics come from the
[constraints documentation](https://www.postgresql.org/docs/18/ddl-constraints.html).

## Decision and alternative

Global uniqueness fits a redirect path that contains only the code. An alternative unique
(owner_id,code) constraint allows each owner to reuse a code, but then owner context must
also participate in resolution. Do not switch without changing the public lookup contract.
RESTRICT makes owner removal an explicit workflow. CASCADE is defensible only if deleting an
owner is intended to remove all owned links and its consequences have been accepted.

## Failure walkthrough

Two transactions request `spruce`. Both application prechecks find it absent. The database
constraint arbitrates conflicting inserts: both cannot commit that same code. Map a conflict
to a stable API outcome; for generated codes retry with a different code within a bounded
policy. For an explicitly requested alias, report conflict rather than silently changing it.
The exact winner is timing-dependent, not assumed here. Similarly, deletion of an owner with
links is rejected; perform an explicit link-removal or ownership-transfer workflow first.

## Self-review

This schema covers identities, global code uniqueness, mandatory ownership, and a deletion
choice. It does not enforce every URL or lifecycle policy, nor prove lookup latency. Before
implementation, verify code normalization, authorization, migration handling for existing
duplicates, and owner-deletion behavior. Test duplicate codes, missing owners, empty values,
and a concurrent collision in a real database. No such database test is claimed here.
