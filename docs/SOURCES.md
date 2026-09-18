# Source ledger — Krama

Append-only. **Never invent a citation** (plan §11.4.1, rule 5). Every primary source a document
teaches or cites gets a row here, and the row is written **only after the record was opened
live** and the title copied from it rather than from memory.

This is the strictest of the three verification rules because it fails the most quietly. A wrong
version pin breaks the next install. A plausible identifier attached to the wrong title survives
for years, gets copied into other people's notes, and is never caught.

**Cite by title and identifier, never by author.** The identifier resolves to exactly one
document, and it is what a reader types.

Accepted identifier forms: `arXiv:2401.12345` · `doi:10.1145/3597503` · `RFC 9110` ·
`ISO/IEC 9899:2018` · `spec:<name>-<revision>`. Anything citation-shaped that matches none of
these is rejected by `python granth.py depth`.

| Identifier | Exact title | Year | URL | Record checked | Taught on | Cited by |
| ---------- | ----------- | ---- | --- | -------------- | --------- | -------- |

| spec:python-3.12-library | The Python Standard Library | rolling | https://docs.python.org/3.12/library/index.html | 2026-09-18 | assigned reference | Python track |
| spec:python-data-model | 3. Data model | rolling | https://docs.python.org/3/reference/datamodel.html | 2026-09-18 | assigned reference | Python track; compare version before using new behavior |
| spec:algorithms-2020 | Introduction to Algorithms | 2020 | https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ | 2026-09-18 | assigned reference | DSA track |
| RFC 9110 | HTTP Semantics | 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | 2026-09-18 | assigned reference | SD weeks 1–3 |
| spec:postgres-concurrency | Chapter 13. Concurrency Control | rolling | https://www.postgresql.org/docs/current/mvcc.html | 2026-09-18 | assigned reference | SD database and transaction sessions |
| spec:consensus-paper | In Search of an Understandable Consensus Algorithm | 2014 | https://raft.github.io/raft.pdf | 2026-09-18 | assigned reference | SD coordination sessions |
| spec:sre-book | Site Reliability Engineering — Table of Contents | rolling | https://sre.google/sre-book/table-of-contents/ | 2026-09-18 | assigned reference | SD reliability and operations |

These landing pages/records were opened live. Individual linked chapters are assigned readings,
not claims of a fresh verification of every interface. Recheck the exact versioned page before
each lab. Case-study workloads and service targets are hypothetical design inputs.
