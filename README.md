# 🪜 Krama

**308 days from "what is an algorithm" to designing, proving, implementing and defending any
data structure, algorithm, or system asked of you.** Python, from scratch, with the cost derived
and a test that can go red.

- **Track I — Days 0–230:** data structures and algorithms. 33 phases, 272 concept IDs.
- **Track II — Days 231–308:** system design, on the same depth contract. 10 phases, 85 IDs.

Days 210–214 are the hinge: LRU, B-trees, LSM trees and consistent hashing are taught in Track I
as *structures*, from scratch, and revisited in Track II as *components* under replication,
partitioning and failure. Nothing is taught twice.

| | |
|---|---|
| **The plan** | [`docs/00_MASTER_PLAN_DSA.md`](docs/00_MASTER_PLAN_DSA.md) — 308 days, 43 phases, 357 concept IDs |
| **The problems** | [`docs/PROBLEM_INDEX.md`](docs/PROBLEM_INDEX.md) — 386 problems by concept ID, plus 16 design drills |
| **The doc standard** | [Part 11 — the depth contract](docs/00_MASTER_PLAN_DSA.md#part-11--the-depth-contract-doc-architecture-v100) — one document per subtopic, ten sections each |
| **The day map** | [`docs/CURRICULUM_INDEX.md`](docs/CURRICULUM_INDEX.md) — every day, its IDs, its gate |
| **Progress** | [`docs/TRACKER.md`](docs/TRACKER.md) — generated, never hand-edited |
| **Amendments** | [`docs/CHANGELOG_PLAN.md`](docs/CHANGELOG_PLAN.md) |
| **Start here** | [`days/day-00-setup/LESSON.md`](days/day-00-setup/LESSON.md) |

## The problem this repo exists to solve

You read about a segment tree. It makes sense. Two weeks later a problem needs one and you
cannot start. You know *what it is*. You have never once *held* it.

Every design decision here is downstream of that gap.

## Getting started

```bash
git clone <your fork> krama && cd krama
uv sync
./k status
# then: days/day-00-setup/LESSON.md
```

Six commands run the whole loop:

```bash
./k status         # how far along am I — computed from disk, never stored
./k start 37       # print today's hub and list its parts in reading order
./k scaffold 37    # create day 37's lab/
./k depth 37       # does day 37 satisfy the depth contract?
./k check          # ruff + format + offline pytest + depth on every written day
./k done 37        # refuses to commit until the checklist is ticked and checks are green
./k ladder BSR     # every catalogued problem for a phase or a concept
```

## How a day is written

A day is a folder — a short hub plus one document per subtopic, never one long page:

```
days/day-37-binary-search/
├── LESSON.md                       # the hub: question, map, setup, build brief, ladder, gate
├── parts/01-the-search-invariant/1.1-the-invariant-of-a-search.md
├── parts/01-the-search-invariant/1.2-why-lo-plus-hi-overflows.md
├── parts/02-searching-on-answers/2.1-the-monotone-predicate.md
├── lab/                            # implement · reference oracle · property tests · bench
└── CHECKLIST.md
```

Every folder is named for what is in it, so `ls days/` reads as a table of contents. The
commands still take the *number* — `./k start 37` globs `day-37-*` — so a slug can be improved
later without breaking anything.

Every part carries the same ten sections, and they trace one path — from a reader who has never
heard of the idea to one who could defend it in a design review:

**one-line answer → the story** (a scene, no jargon) **→ the idea in plain language → where it
actually shows up → the mechanism** (with the invariant stated) **→ line by line** (fragments of
≤10 lines, plus the near-miss) **→ the cost, derived** (the sum, the recurrence, the potential
function — never an asserted complexity) **→ when it breaks** (the real traceback, pasted) **→
in production** (what a senior reviewer says, what an interviewer probes) **→ check yourself.**

`./k depth N` fails the day if any of them is missing. It cannot check whether the writing is
good — that is the writer's job, and `CLAUDE.md` is where that standard lives.

Two things you will not find in these documents: **a time estimate**, and **an idea that stops at
the toy example**. A day is a unit of subject, not of time.

## The rules that shape every file

The full sixteen are Part 1 of the plan. The six that shape every line:

1. **From scratch before library.** The binary heap before `heapq`. The hash table before `dict`.
2. **You write every line.** `lab/implement.py` ships as a stub with a docstring contract. The
   lesson demonstrates the mechanism on a *different* example, on purpose.
3. **Every cost is derived.** Summation, recurrence, accounting, potential, or expectation —
   named, and shown. "This is O(n log n)" without working is a rejected document.
4. **Measure what you claim.** Every complexity claim has a benchmark whose ratio column bends
   the way the theory says — or an explanation of why it doesn't (it is usually cache behaviour).
5. **Reproduce the failure on screen.** The real `IndexError`, pasted, not paraphrased.
6. **Depth over density.** One idea, one document. A wall of text is depth's disguise.

## Writing the days that aren't written yet

`docs/TRACKER.md` shows exactly which days exist. To produce the next one, in VS Code with
Claude Code:

```
/day-krama 2
```

That skill lives at [`.claude/skills/day-krama/SKILL.md`](.claude/skills/day-krama/SKILL.md).
It plans the part split first **and shows it to you before writing**, writes one document per
subtopic, assembles the hub last, and ends by running `./k depth 2` — which is what stops a thin
day from being called written.

## Repository layout

```
krama/
├── k                          # the daily driver
├── CLAUDE.md                  # operating rules for the AI pair-programmer
├── docs/
│   ├── 00_MASTER_PLAN_DSA.md
│   ├── CURRICULUM_INDEX.md
│   ├── TRACKER.md             # generated by scripts/tracker.py
│   ├── MISSES.md              # what you got wrong, by concept ID
│   ├── CHANGELOG_PLAN.md
│   └── adr/
├── days/                      # day-00-setup … day-230-<slug>, each folder named for its subject
├── scripts/depth_check.py     # enforces the plan's Part 11 depth contract
├── scripts/tracker.py         # regenerates docs/TRACKER.md
├── src/krama/                 # deliberately almost empty — you type every line
└── .claude/skills/day-krama/  # the skill that writes a day
```
