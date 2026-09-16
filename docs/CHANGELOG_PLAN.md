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

---

## 2026-09-16 · The languages course merged into the days

Krama Languages — a separate 180-day course under `langs/`, with its own driver `./l`,
its own syllabus, contract and skill — became **the languages half of every Krama day**.

**Why.** Two courses of exactly 180 days each, meant to be done together, were tracked
apart. Finishing "day 12" meant finishing it twice, in two folders, with two `next`
commands that could disagree. The reader wanted one day to be one thing: when day N is
done, everything for day N is done — DSA, system design, and the three languages.

**What changed.**

| Before | After |
|---|---|
| `langs/days/day-NNN-<theme>/` beside `days/day-NNN-<topic>/` | One folder, `days/day-NNN-<topic>/`; the DSA slug names it |
| `01-python-*`, `02-go-*`, `03-cpp-*`, `04-practice.md` | `05-lang-python-*`, `06-lang-go-*`, `07-lang-cpp-*`; the exercises fold into `03-practice.md` |
| Front matter `track: python / go / cpp` | `track: lang-python / lang-go / lang-cpp`, so the C++ contest lesson (`track: cpp`) stays distinct |
| `langs/scripts/syllabus/part1..3.py` | `scripts/syllabus/langs/part1..3.py`, loaded by the one `scripts/curriculum.py` |
| `./l status / next / check / build` | `./k` does all of it; `./k status` shows every track and `./k next` names the files a day still needs |
| A day was four files and "complete" meant DSA + system design | A day is seven files and complete means DSA + system design + all three language lessons |
| `langs/docs/00_HOW_A_DAY_WORKS.md` and `langs/CLAUDE.md` | Folded into the root contract and `CLAUDE.md`; rules 16 and 17 carry the languages-only rules |
| `/day-langs N` wrote a separate course's day | `/day-krama N` writes the whole day and hands the languages half to `/day-langs` |

**Filenames kept.** The languages files keep the slug rule they were named with (first
four words, no connector trimming) so that moving them changed only the prefix. The ten
days already written moved with their history.

**Practice sheets.** The separate language practice sheet became `08-lang-practice.md`
on the move and is being folded into `03-practice.md` one block of days at a time. The
folded set is `UNIFIED_PRACTICE_DAYS` in `scripts/build_skeleton.py`; until it reaches
180, an unfolded day still carries the `08-` file and `./k check` expects it there.

**Kept.** The languages syllabus itself, unchanged: nine phases, ten projects, six
five-day builds, an eight-day capstone, Go carrying Protocol Buffers and gRPC. The
nine-section contract, with the languages headings for §1, §6 and §8. The C++ contest
track, now named as such to tell it apart from the languages track's C++ lesson.
