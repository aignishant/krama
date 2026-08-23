# ADR 0002 — System design appended into one repo, not split into a sibling

**Status:** accepted · 2026-08-23

## Context

The DSA track (Days 0–230) and a system design track are usually kept apart: different books,
different repos, different study sessions. The argument for separating them is that they are
studied at different times and by people with different goals.

The argument against is stronger, and it is specific rather than aesthetic. Five ideas appear in
both: LRU caching, B-trees, LSM trees, consistent hashing, and rate limiting. Kept in two repos,
they are taught twice — badly both times. The DSA version teaches the structure with no reason to
exist; the system design version waves at "a B-tree index" without the learner ever having split
a node. Each half is the other half's missing motivation.

## Decision

One repository, two tracks, one concept-ID space, one tracker, one depth contract.

Days 210–214 (`SYS`) teach those five as structures, from scratch, with derived costs. Days 246,
247, 278 and 279 revisit them **by ID** as components under replication, partitioning and
failure, and are forbidden from re-teaching the structure.

## Consequences

- No idea is taught twice, and the second encounter can assume the first.
- `./k status` reports one number across 309 days, which is the honest number.
- The repository is large. Accepted: the tracker makes position obvious, and `CURRICULUM_INDEX.md`
  is navigable by phase.
- Track II inherits the depth contract, which was written for algorithms. Three sections needed a
  documented adaptation (§6, §7, and the ladder) rather than an exemption — see
  `.claude/skills/day-krama/reference/design_day.md`. An adaptation is recorded; an exemption
  would have been a hole.
- Someone who only wants DSA stops at Day 230 and has a complete artefact. Nothing about Track II
  leaks backwards into Track I.
