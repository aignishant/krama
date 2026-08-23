# Day 0 — The Foundry

> Before you learn a single algorithm: the tools, the repo, the contract, and how to read
> a document here so that it actually changes what you can do.

**Owns:** `FND-01` · `FND-02` · `FND-03` · `FND-04`  |  **Phase 0 — The Foundry**

*Orientation day: no `parts/`. One of the two exemptions in the plan (the other is gate days).*

---

## 1. The question of the day

There is a particular kind of failure that happens to people who study data structures and
algorithms, and it is worth naming on Day 0 so that you can watch for it for the next 230 days.

It goes like this. You read about a segment tree. It makes sense. The diagram is clear, the
recursion is elegant, you nod. Two weeks later a problem needs a segment tree and you cannot
write one. Not "you write it slowly" — you cannot start. You know *what it is*. You have never
once *held* it.

That gap — between recognising an idea and being able to produce it — is the entire problem
this repo is built to solve, and almost every design decision in it is downstream of that one
observation. Today you install the tools that make the gap visible, and learn how to read a
document here so that the gap closes instead of widening.

---

## 2. `FND-01` — The contract you are signing

Six clauses. They are not motivational. They are operational, and each one costs you something.

**One. You write every line.** The lessons show you the mechanism, always on a *different*
example than the day's lab task. `lab/implement.py` arrives as a stub with a docstring contract
and `raise NotImplementedError`. If you fill it by copying from the lesson, the repo has no way
to stop you and no reason to exist. The rule that keeps you honest is simple and you should
adopt it today: **the core rung of the ladder is solved from an empty file.** Not from a
half-remembered one. Empty.

**Two. From scratch before library.** You will write a binary heap before you are allowed to
`import heapq`. You will write a hash table before you lean on `dict`. This is not nostalgia.
It is that `heapq.heappush` is a name until you have written the sift-up loop, and after you
have written it, it is a thing you can reason about — including reasoning about *when not to
use it*.

**Three. Every cost is derived.** You are never allowed to write "this is O(n log n)" in a note
or say it in an interview without being able to produce the sum or the recurrence that makes it
true. Phase 1 is eight days long entirely because of this clause.

**Four. A day is a unit of subject, not of time.** You will find no time estimates anywhere in
this repo. Not on Day 1, not on Day 173. Some days are one sitting. Day 120 (lazy propagation) is
probably four. A curriculum that promises half an hour a day is promising you a pace,
and a pace is the one thing that cannot be promised about understanding.

**Five. You log what you get wrong.** `./k miss BSR-03` appends a concept ID to
`docs/MISSES.md`. Gate days read that file first. By Day 230 it is the most valuable file in
the repository, and the capstone write-up is assembled from it. The instinct to skip this is
strong and it is exactly the instinct that leaves you re-learning binary search boundaries for
the fourth time.

**Six. The tracker is generated.** `docs/TRACKER.md` is produced from disk by
`scripts/tracker.py`. You cannot tick a day you did not do, because there is no box to tick —
there is only whether the files exist and the checklist inside them is ticked. Hand-editing it
is a lie told to a person who will need the truth in four months: you.

---

## 3. `FND-02` — The toolchain

Four tools, and a reason for each.

### Python 3.12+ and `uv`

`uv` is the package and environment manager. It is used here rather than `pip` + `venv` for one
reason that matters to this specific project: it resolves and installs fast enough that adding a
dependency mid-lesson does not break your concentration.

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then, from the repo root:

```bash
uv python install 3.12
uv sync
```

`uv sync` reads `pyproject.toml` and `uv.lock` and builds `.venv/` with **exact** pinned
versions. Rule 15 of the plan: nothing floats. A benchmark you cannot re-run is an anecdote.

### `ruff` — lint and format

One tool, both jobs, fast. It is not here to make your code pretty. It is here because
`ruff check` catches the class of mistake that wastes twenty minutes in a lab: the unused
variable that reveals you assigned to the wrong name, the shadowed builtin, the mutable default
argument.

### `pytest` + `hypothesis`

`pytest` runs the tests. `hypothesis` **generates** them — it invents inputs, finds the one that
breaks your code, then shrinks it to the smallest breaking case and shows you that.

This pairing is the technical heart of the repo, and it deserves a moment on Day 0, because it
is what makes "from scratch" safe. Every lab has two implementations: `reference.py`, which is
brute force, slow, and correct by inspection; and `implement.py`, which is yours. The test says:

```python
@given(st.lists(st.integers()))
def test_matches_reference(xs: list[int]) -> None:
    assert implement(xs) == reference(xs)
```

Hypothesis will throw hundreds of lists at that assertion — empty, single-element, all-equal,
enormous, full of duplicates, full of negatives — and when it finds a failure it hands you
`[0, 0]` rather than the 900-element list it actually found first. You get the *smallest*
counterexample, which is usually the one that also explains the bug.

The habit this builds: you stop asking "does it work on my example" and start asking
"for what input is my invariant false".

### Verify it

```bash
uv run python -c "import sys, hypothesis, pytest; print(sys.version)"
uv run ruff --version
```

---

## 4. `FND-03` — How to read a Krama document

Every teaching document in `days/*/parts/` has exactly ten sections, always in the same order.
The full specification is
[Part 11 of the master plan](../../docs/00_MASTER_PLAN_DSA.md#part-11--the-depth-contract-doc-architecture-v100).
What follows is not the specification — it is *how to use it*, which is a different thing and
nobody tells you this part.

| § | Section | How to read it |
|---:|---|---|
| 1 | The one-line answer | Read it. Then **cover it and say it back.** If you can't, you are not ready for §2 — reread. It is one sentence; there is no excuse. |
| 2 | The story | Read it slowly, once, and **do not skim it because it has no code in it.** This is the section that makes the idea retrievable in six months. People who skip it read faster and forget everything. |
| 3 | The idea in plain language | Read it while consciously mapping each new term back to the thing in the story it names. "Oh — the *pivot* is the pharmacist's middle drawer." |
| 4 | Where this shows up | Skim on the first pass. Come back to it before an interview; this is where the "so where would you actually use this" answer lives. |
| 5 | The mechanism | **Redraw the diagram by hand on paper.** Not optional. Then close the document and state the invariant out loud. |
| 6 | Line by line | Read the fragment, then **cover the prose and predict why that line**. Then read the prose. The near-miss at the end is the most valuable code in the document — the bug you will actually write is in there. |
| 7 | The cost, derived | Work the derivation on paper *alongside* the document. Reading a derivation and producing one are different skills and only the second is tested. |
| 8 | When it breaks | **Reproduce it.** Actually type the failing input into a REPL and see the traceback with your own eyes. Reading `RecursionError` is not the same as hitting one. |
| 9 | In production | Read the reviewer quote twice. That is what your code will get said about it. The three interviewer follow-ups are your revision cards. |
| 10 | Check yourself | Do this **without the document open**, the day *after* you read it, not the same day. Same-day answers measure short-term memory, which is not the thing you are building. |

A concrete reading protocol, if you want one to start with: §1–§6 in one sitting with paper;
then the lab; then §7–§9 after the lab, because the cost section lands differently once you have
built the thing; then §10 the next morning, cold.

---

## 5. `FND-04` — The loop

Six commands run all 230 days.

```bash
./k status          # where am I — computed from disk and the index, never stored
./k start 12        # print day 12's hub and list its parts in reading order
./k scaffold 12     # create day 12's lab/ from the stubs
./k depth 12        # does day 12 satisfy the depth contract?
./k check           # ruff + format + offline pytest + depth on every written day
./k done 12         # commit gate: checklist ticked, checks green, tracker regenerated
./k miss BSR-03     # log a concept you got wrong
```

`./k done` is the only one that commits, and it refuses in three cases: an unticked checklist
box, a failing check, or a gate day with an empty `NOTES.md`. The refusals are the feature.

### The repo, briefly

```
krama/
├── k                          # the daily driver
├── CLAUDE.md                  # operating rules for the AI pair-programmer
├── docs/
│   ├── 00_MASTER_PLAN_DSA.md  # the sixteen rules and the depth contract
│   ├── CURRICULUM_INDEX.md    # every day, its concept IDs, its gate
│   ├── TRACKER.md             # generated — never hand-edited
│   ├── MISSES.md              # what you got wrong, by concept ID
│   └── adr/                   # decision records
├── days/
│   ├── day-00-setup/          # you are here
│   └── day-NN-<slug>/         # LESSON.md + parts/ + lab/ + CHECKLIST.md
├── scripts/                   # tracker.py, depth_check.py
└── .claude/skills/day-krama/  # the skill that writes a day
```

### Writing days that don't exist yet

`docs/TRACKER.md` shows what is written. To produce the next day, in VS Code with Claude Code:

```
/day-krama 2
```

The skill reads the index for Day 2's concept IDs, plans the part split *and shows you the split
before writing*, writes one document per subtopic, assembles the hub last, and finishes by
running `./k depth 2`. If the split it proposes looks wrong to you, say so — that conversation
is worth more than the document.

---

## 6. The build brief

Today's lab exists to prove the harness works, not to teach an algorithm.

```bash
./k scaffold 0
```

Implement in `days/day-00-setup/lab/implement.py`:

```python
def running_max(xs: list[int]) -> list[int]:
    """Return the list whose i-th element is max(xs[0..i]).

    Pre:   xs may be empty.
    Post:  len(result) == len(xs); result is non-decreasing;
           result[i] == max(xs[:i+1]) for all i.
    Time:  O(n), single pass.
    Space: O(n) for the output, O(1) auxiliary.
    """
```

**Forbidden today:** `itertools.accumulate`, `numpy`, and any solution that calls `max()` on a
slice inside the loop — that is the O(n²) version, and `bench.py` will show you its ratio column
climbing towards 4 while yours sits near 2. Write the slow one first *on purpose*, run the
bench, look at the two ratio columns side by side, then write the fast one. That contrast is the
actual lesson of Day 0, and it is the shape of every cost argument in Phase 1.

Done when:

```bash
uv run pytest days/day-00-setup/lab -q
uv run python days/day-00-setup/lab/bench.py
```

---

## 7. The gate

Say these out loud, without notes, before ticking the checklist.

1. What are the two things `./k done` refuses on, and why does refusing help you?
2. What is `reference.py` for, given that it is slower and you already have `implement.py`?
3. Hypothesis found a failure in a 900-element list and reported `[0, 0]`. What did it do,
   and why is the reported case more useful than the one it found first?
4. Which section of a Krama document should you do the day *after* you read it, and why?
5. Why does the repo forbid time estimates? Give the reason, not the rule.
6. In your own words: what is the difference between recognising a segment tree and holding one?

Then:

```bash
./k done 0
```

Tomorrow is Day 1 — `CPX-01`, `CPX-02`: what an algorithm actually is, and the imaginary machine
every complexity claim you will ever make is secretly about.
