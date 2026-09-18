# Pin ledger — Krama

Append-only. **Never invent a fact** (plan §2, Principle 6). Every version, tool, limit or quota
this project depends on gets a row here with the value **actually observed**, the date it was
observed, the day that added it, and why.

If a value could not be looked up, the row says `TODO(<the exact lookup command>)` — never a
guess. A guess that happens to be right is still a guess, and the next reader cannot tell which
kind they are holding.

A later row may **supersede** an earlier one: a dated observation superseding a dated observation
is not an amendment, it is the ledger doing its job. Say so in the `Why` column.

| What | Value | Date observed | Day | Why, and how it was observed |
| ---- | ----- | ------------- | --- | ---------------------------- |

| Python | 3.12.10 | 2026-09-18 | setup | Observed with `python --version`; tools require 3.11+; practice baseline is 3.12. |
