# Provenance ledger — Krama

Append-only. Every third-party thing this project runs, vendors or depends on gets a row here
**before it is ever run** — source, licence, version, who audited it and when, and what it is
permitted to touch.

This is Principle 12, blast radius before capability, written as a table. A dependency you have
not audited is a capability you have granted without deciding to.

| What | Source | Version | Licence | Audited on | Audited by | Permitted scope |
| ---- | ------ | ------- | ------- | ---------- | ---------- | --------------- |

| Granth | https://github.com/aignishant/granth-skill | Local skill SHA256 `261b8aac0df3997ecd5510724e02ec8f0232f1f704ab24169a602e17b420a620` | MIT; see ../vendor/granth/LICENSE | 2026-09-18 | Course author, code inspection | Local plan parsing/index generation; no done/commit command executed. |
