# Changelog — the plan

Structural changes to the course. Not a log of days written.

---

## 2026-08-25 · Restarted as a 180-day two-track course

The 230-day DSA course plus 78-day system design course became **one 180-day course
where every day teaches both**.

**Why.** The old version failed the reader on two counts. The material was written at
the level of someone who already had a computer science background, and the `lab/`
scaffold — `implement.py` as a stub, a reference oracle, pytest, a benchmark harness —
added setup work without adding learning. It also ran DSA for 230 days before system
design started, which meant no system design practice for most of a year.

**What changed.**

| Before | After |
|---|---|
| 308 days, DSA then system design in sequence | 180 days, both tracks every day |
| Hub `LESSON.md` + `parts/NN-section/N.N-subtopic.md` | Hub `README.md` + two lesson files + one practice sheet |
| Ten-section depth contract | Nine-section contract, story-first, interview-shaped |
| `lab/` with stub, oracle, tests, bench | Removed entirely. Full solutions in the lesson, named problems in `03-practice.md` |
| Solutions withheld from the reader (old rule 12) | Solutions shown in full (new rule 5) |
| Concept IDs (`CPX-04`, `BSR-03`) owned per day | Dropped. The day's topic is its identity |
| Derivations, proofs, potential functions, CPython internals | Cut unless an interviewer would ask (new rule 14) |
| `docs/PROBLEM_INDEX.md` as a catalogue | Dropped. Problems named per day |
| Syllabus in a hand-maintained markdown table | Syllabus is data in `scripts/curriculum.py`; the index is generated |

**System design ordering.** Fundamentals → APIs → databases → object-oriented design →
SOLID → patterns → low-level design case studies occupy days 1-96. Scaling, distributed
systems, building blocks and high-level design case studies occupy days 97-180. Low-level
design comes first because that is the round junior candidates actually get, and because
high-level design is unreadable before you know what an index and a queue are.

**Kept.** The writing style — second person, present tense, short sentences, concrete
before abstract, no cheerleading, no time estimates. The story section, which was the
best part of the old format. The refusal to hand-edit generated files.

The previous version is in [`archive/`](../archive/) in full.
