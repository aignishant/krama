---
name: day-krama
description: Write a Krama day (DSA or system design) — the hub LESSON.md, the parts/ documents under the ten-section depth contract, the lab scaffold, and the CHECKLIST. Use this skill whenever the user asks to write, generate, draft, expand, rewrite, fix, deepen or review any day in days/, mentions a day number ("do day 37", "write the binary search day", "day 102 is thin"), asks for a lesson or part or subtopic document, asks to split a topic into parts, asks anything about the depth contract, or asks for a system-design day, drill or capacity estimate. Use it even when they phrase it casually as "next day please" or "continue the curriculum".
---

# Writing a Krama day

You are producing the teaching material for one day of a 230-day DSA curriculum. The
learner reads only these documents. If an idea is not in them, the learner never meets it.

**Read first, every time:** `docs/00_MASTER_PLAN_DSA.md` Part 11 (the depth contract) and
`CLAUDE.md` (the fifteen hard rules). Then `docs/CURRICULUM_INDEX.md` for the day's IDs.

**Which track?** Days 0–230 are Track I (DSA) — this file describes them. Days 231–308 are
Track II (system design): same contract, different §6, §7 and ladder. If the day is ≥ 231,
**read `reference/design_day.md` now** and follow it alongside this file.

---

## The procedure — six steps, in order

### Step 1 · Read the assignment

```bash
./k start <N>            # prints the index row for day N, its IDs, and its neighbours
grep -n "MISSES" -A50 docs/MISSES.md | grep "<ID>"   # has the learner failed this before?
```

Collect:
- the concept IDs this day **owns** (from the index — a day teaches only what it owns),
- the IDs it **requires** (look them up; you may reference them by number, and should),
- whether it is a **gate day** (marked `G` — different structure entirely, see Step 6),
- any ID in `docs/MISSES.md` that this day revisits.

### Step 2 · Plan the split — **before writing a single sentence**

This is the step that decides whether the day is good. Write the plan out and show it.

A **section** groups subtopics that share one mental model — usually one concept ID.
A **subtopic** is one idea that can be stated in a single sentence. If a proposed subtopic
needs "and" to state it, it is two subtopics.

Produce a table like this and put it in your response before writing:

| Part | Title | ID | The one-sentence idea | Why it is separate from its neighbour |
|---|---|---|---|---|
| 1.1 | The invariant of a search | BSR-01 | Binary search maintains "the answer is inside `[lo, hi]`" and shrinks the window. | The invariant is a claim about the *state*; 1.2 is about arithmetic on the state. |
| 1.2 | Why `(lo+hi)` overflows | BSR-02 | Midpoint arithmetic can leave the representable range in fixed-width languages, and Python's `int` hides a real cost instead. | Different failure mode, different lesson. |

Rules for the split:
- **3–8 parts per day.** Fewer than three usually means you lumped ideas together.
  More than eight usually means the *index* is wrong — say so rather than writing nine.
- **One part, one idea.** A part that would have two `§1` one-line answers is two parts.
- **Order is a dependency order**, not importance order. Part 1.1 must need nothing from 1.2.

Then **name the folders**, in the same response, before writing. Every folder says what is
inside it, so `ls days/` and `ls parts/` are tables of contents rather than lists of numbers:

| Folder | Shape | Example |
|---|---|---|
| the day | `day-NN-<kebab-slug>` | `days/day-01-what-computation-costs/` |
| a section | `NN-<kebab-slug>` | `parts/02-model-of-computation/` |
| a part | `<section>.<subtopic>-<kebab-slug>.md` | `2.1-the-ram-model.md` |

The day slug is the subject, **two to four words**, taken from the index title's head clause —
not the whole title, not a phase name. The section slug is the shared mental model that made
those subtopics one section, and it is what you write in the hub's §2 map anyway
("**Section 2** is about the model of computation") — so lift it from there.
`./k depth N` rejects a day whose folders do not match these shapes, so pick them once and
correctly. Slugs are lowercase, digits and hyphens only, no articles at the front.

### Step 3 · Write the parts — one file at a time, never batched

Path: `days/day-<NN>-<day-slug>/parts/<NN>-<section-slug>/<section>.<subtopic>-<kebab-slug>.md`

for example
`days/day-01-what-computation-costs/parts/02-model-of-computation/2.1-the-ram-model.md`.

Each file follows `reference/part_template.md` **exactly** — all ten sections, in order,
with the front-matter block. The section-by-section requirements and the failure conditions
are in `reference/depth_contract.md`; **read it before writing your first part** and re-read
§2, §7 and §9 before writing each subsequent one, because those three are where quality dies.

The three that get skimped and must not be:

- **§2 The story.** A scene. People, a place, stakes, a problem they feel before it is named.
  200–500 words. No jargon. No code. No "imagine you have an array" — that is not a scene,
  that is an array. A pharmacist finding a strip of tablets by expiry date at 2 a.m. is a scene.
- **§7 The cost, derived.** One of the five allowed derivations (plan, Part 13), named:
  summation · recurrence · accounting · potential · expectation. Show the working. Separate
  best/average/worst. Say what the constant factor hides.
- **§9 In production.** Two named real systems. Then a **verbatim quote** of what a senior
  reviewer says about this code in review. Then the **three follow-up questions** an interviewer
  asks after you get it right.

Write in the order 1.1, 1.2, 2.1 … Later parts may reference earlier ones by number; earlier
parts may never forward-reference.

### Step 4 · Scaffold the lab

```bash
./k scaffold <N>
```

Then fill in three of the four files — **never the fourth**:

- `reference.py` — the brute-force oracle. Correct by inspection. Slow is fine.
- `test_implement.py` — Hypothesis strategies + the explicit edge battery (empty, single,
  all-equal, sorted, reverse-sorted, duplicates, max size, negatives), asserting
  `implement(x) == reference(x)`.
- `bench.py` — doubles `n` six or more times, prints `n`, time, and **the ratio column**.
- `implement.py` — **signature, docstring contract, `raise NotImplementedError`. Nothing else.**
  Writing this file for the learner destroys the point of the repo (`CLAUDE.md` Rule 12).

The docstring contract states: the signature, the pre-conditions, the post-condition/invariant,
the required complexity, and the **forbidden imports** for that day.

### Step 5 · Assemble the hub last

`days/day-<NN>-<day-slug>/LESSON.md`, following `reference/hub_template.md` — seven sections:
question of the day · the map · what you already have · setup · the build brief ·
the problem ladder · the gate.

The hub is written **last** because only now do you know what the parts actually say.
It is short. It is a map, not a summary — if the hub explains the idea, the parts are failing.

The ladder has four rungs (warm-up → core → stretch → interview). **Every problem is selected
from `docs/PROBLEM_INDEX.md`** — run `./k ladder <PREFIX>` and pick from what is catalogued,
carrying each problem's "really testing" line across verbatim. Never invent a ladder entry at
writing time, and never paste a problem statement. If the catalogue lacks what the day needs, add
it to the catalogue first, in its own commit. The stretch rung must name the earlier ID it
combines with.

For Track II days the rungs are **recall → read → drill → critique** instead; see
`reference/design_day.md`.

Then write `CHECKLIST.md` from `reference/checklist_template.md`.

### Step 6 · Verify

```bash
./k depth <N>     # must be green
./k check         # ruff, format, offline tests, depth on all written days
```

If `./k depth` fails, fix the document — never the checker.

Report back with: the split table, the files created, and the depth result.

---

## Gate days are different

A gate day (marked **G** in the index) owns no new IDs and has no `parts/`. It contains:

1. **The interrogation** — 8–15 questions answered *out loud, without notes*, hardest last,
   answers in `<details>` blocks. Draw at least three from `docs/MISSES.md`.
2. **The build** — one implementation using ≥3 IDs from the phase, with the same lab scaffold.
3. **The retention set** — 3 problems whose IDs come from **two phases back**.
4. **`NOTES.md`** — the learner writes the single mistake they made most this phase.
   `./k done` refuses a gate day with an empty `NOTES.md`.

---

## Self-review before you report done

Run this list against every part you wrote. Any "no" means rewrite, not patch.

- [ ] Could a reader who has never heard this word follow §1→§5 without stopping?
- [ ] Is §2 a **scene**, with a person in it, that I could film?
- [ ] Does §5 state an **invariant** in words, and does the diagram show it?
- [ ] Does §6 explain **why that line and not the obvious alternative**, and include a near-miss?
- [ ] Does §7 show **working**, not a claimed complexity?
- [ ] Is the error text in §8 **real** — the exact CPython wording?
- [ ] Does §9 contain a named system, a reviewer quote, and three interviewer follow-ups?
- [ ] Does §10 include one question that **breaks** the structure and one that cites a prior ID?
- [ ] Zero time estimates anywhere in the day?
- [ ] Do the day folder and every section folder carry a slug that says what is inside them?
- [ ] Is `implement.py` still a stub?

## Common failure modes, named so you can avoid them

| Failure | What it looks like | Fix |
|---|---|---|
| **The textbook voice** | "In this section, we shall examine…" | Second person, present tense, start with the thing. |
| **The fake story** | "Imagine an array of numbers…" | An array is not a scene. Put a human under pressure in a real place. |
| **Asserted complexity** | "This runs in O(n log n)." | Show the sum or the recurrence. |
| **The wall of code** | 40 lines, one comment on top | Fragments of ≤10 lines, prose between. |
| **Library leakage** | `import heapq` on Day 40 | Check the index for which day owns it. |
| **Depth by length** | Same idea restated three ways | Cut the restatements; add a *different* idea as a new part. |
| **Solution leakage** | `implement.py` filled in, or the answer in §6 | §6 teaches the mechanism on a *different* example than the lab task. |
| **Numbered folders** | `days/day-37/parts/02/` | Slug every folder: `day-37-binary-search/parts/02-the-monotone-predicate/`. |

## Reference files

- `reference/depth_contract.md` — the ten sections, what each must contain, what fails it.
  **Read before writing your first part in any session.**
- `reference/design_day.md` — what changes for Track II (Days 231–308): §6 without an algorithm,
  §7 as capacity arithmetic, the drill ladder, and the hinge back to Days 210–214.
  **Read whenever the day number is ≥ 231.**
- `reference/part_template.md` — copy this for every part.
- `reference/hub_template.md` — copy this for `LESSON.md`.
- `reference/checklist_template.md` — copy this for `CHECKLIST.md`.
