# How to read a day

Each day is a folder:

- **`LESSON.md`** — the hub. The question of the day, the map of parts and their reading order,
  what you already need, the build brief, the problem ladder, the gate. It is a map, not a
  summary: if the hub explains the idea, the parts have failed.
- **`parts/<NN>-<section-slug>/<section>.<subtopic>-<slug>.md`** — the teaching. One idea per
  document, ten sections each. A **section** groups subtopics sharing one mental model, and the
  folder is named for it, so `ls parts/` tells you what the day contains before you open
  anything; the hub says the same thing at more length.
- **`lab/`** — `implement.py` (yours, a stub until you fill it), `reference.py` (the slow oracle),
  `test_implement.py` (Hypothesis against the oracle), `bench.py` (the doubling ratio table).
- **`CHECKLIST.md`** — `./k done N` refuses to commit until every box is ticked.

## The reading protocol

§1 cover-and-recite · §2 slowly, do not skim it because it has no code · §5 redraw the diagram by
hand and say the invariant aloud · §6 cover the prose and predict why each line · §7 work the
derivation on paper alongside · §8 actually reproduce the error in a REPL · §10 the next morning,
cold, with the document closed.

A workable order: §1–§6 in one sitting with paper; then the lab; then §7–§9 after the lab,
because the cost section lands differently once you have built the thing; then §10 the next day.

## The two exemptions

**Day 0** is orientation and **gate days** are examinations. Neither has `parts/`. Every other
day does.
