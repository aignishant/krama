# The depth contract — the ten sections

Authoritative source: `docs/00_MASTER_PLAN_DSA.md`, Part 11. This file is the working version
you read while writing.

Every `parts/` document has these ten `##` headings, in this order, with these exact titles.
`scripts/depth_check.py` matches on the headings, so do not rename them.

---

## Front matter

```yaml
---
id: BSR-01              # exactly one concept ID, from CURRICULUM_INDEX.md
day: 37
section: 1
subtopic: 1
title: The invariant of a search
requires: [CPX-03, ARR-01]    # IDs the reader must already own; used for backlinks
---
```

---

## §1 — The one-line answer

The entire idea in one sentence a tired person could repeat at the end of a long day.

- **Fails if**: it contains a term this document defines later.
- **Fails if**: it is two sentences, or one sentence with a semicolon doing the work of two.
- Test: read it to someone who knows nothing. If they say "what's a predicate", rewrite it.

## §2 — The story

A scene. 200–500 words. Zero jargon. Zero code. Zero variables.

- A **person**, a **place**, a **constraint**, and a **cost of getting it wrong**.
- The reader must feel the problem before it has a name.
- The story must contain, without naming them, the exact mechanics the idea will use — so that
  §3 can rename them rather than introduce them.
- **Fails if**: it is an analogy sentence ("a hash table is like a filing cabinet").
- **Fails if**: deleting it changes nothing later in the document.

Good story seeds: a night-shift pharmacist; a warehouse pick route; a phone exchange in 1962;
an airport gate agent reseating a full flight; a librarian after a flood; a chess tournament
pairing desk; a hospital triage board.

## §3 — The idea in plain language

The story, renamed. This is where the vocabulary arrives, and every term is introduced by
pointing at something the story already established.

- **Fails if**: a term appears that the story did not earn.
- End with the formal statement of the idea in one indented block.

## §4 — Where this actually shows up

- **Two named real systems** — PostgreSQL's planner, the Linux CFS scheduler, Git's packfiles,
  Redis's expiry cycle, a CDN's cache eviction. Named, with what specifically it does there.
- **One interview framing** — how the idea is disguised when it is asked.
- **Fails if**: it says "widely used in many applications".

## §5 — The mechanism

How it works, step by step.

- A **diagram** (Mermaid for structure, ASCII for memory/arrays), captioned with what to notice.
- The **invariant**, stated in words in bold: *what is true before every step and after every step*.
- A trace: one small concrete input walked through, showing the state at each step.
- **Fails if**: no invariant is stated.

## §6 — Line by line

The from-scratch Python, in fragments of **≤10 lines**, each followed by prose.

- Each fragment's prose answers: *why this line, and not the obvious alternative?*
- At least one **near-miss**: the version that looks correct, plus the exact input that kills it.
- Type hints on the signature. No library shortcuts the curriculum hasn't reached yet.
- **Fails if**: the code is one block with a comment on top.
- **Fails if**: it solves the same problem as today's `lab/implement.py` task. Teach the
  mechanism on a *different* example, or the learner copies instead of building.

## §7 — The cost, derived

Name the derivation technique, then do it.

| Technique | Use when | Must show |
|---|---|---|
| Summation | Loops | The sum, and its closed form |
| Recurrence | Divide and conquer | `T(n) = aT(n/b) + f(n)`, then unrolling or Master case with justification |
| Accounting | Amortized, credit-based | The credit invariant, and that credit never goes negative |
| Potential | Amortized, state-based | `Φ` defined, `Φ ≥ 0`, `Φ(∅) = 0`, amortized = actual + ΔΦ |
| Expectation | Randomised | The probability space, stated explicitly, then linearity |

Then:
- **Best / average / worst**, separated, each with the input that causes it.
- **Space**: auxiliary vs total. Recursion stack counts.
- **What the constant hides**: cache misses, allocation, comparison cost, Python interpreter
  overhead vs C-level loops.
- **Fails if**: a complexity is stated without working.

## §8 — When it breaks

The real failure, reproduced.

- The **actual traceback text**, pasted, in a code block:
  ```
  RecursionError: maximum recursion depth exceeded in comparison
  ```
- Or the off-by-one, shown with the exact input and the wrong output side by side.
- Or the input that turns average case into worst case, with the measured slowdown.
- Then the fix, and *why the fix is not just a patch*.
- **Fails if**: the error is paraphrased ("you'll get a recursion error").

## §9 — In production

Three required blocks:

1. **At scale** — what changes when `n` is 10⁹, when the data is on disk, when there are
   32 threads, when it is distributed across machines. Cache locality. Memory. Tail latency.
2. **What a senior reviewer says** — a verbatim quote, in a blockquote, of the comment this
   code gets in review. Realistic and slightly blunt.
   > "This is correct but it re-hashes on every lookup. Hoist it, or the profile will
   > point here in six months and nobody will remember why."
3. **What an interviewer probes** — exactly three follow-up questions, asked after you get the
   main answer right, with a one-line note on what each is really checking.

- **Fails if**: it repeats §4 instead of adding the scale story.

## §10 — Check yourself

4–8 questions, easiest first, answers in `<details><summary>` blocks.

- At least one asks the reader to **break** the thing — construct the input that defeats it.
- At least one **cites a previous concept ID by number** and asks how the two relate.
- At least one is a **"what would you say in review"** question, not a recall question.
- **Fails if**: every question is recall.

---

## The checker

`./k depth <N>` verifies, per part: front matter present and parseable, the ID is one the index
assigns to this day, all ten headings present in order, §2 word count in range, §6 contains a
fenced code block, §7 contains one of the five technique keywords, §8 contains a fenced block,
§9 contains a blockquote, §10 contains at least one `<details>` and one ID reference.

It cannot check whether the writing is good. That is your job.
