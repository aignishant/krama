# Krama — DSA, system design and advanced Python

**168 study days · 24 weekly phases · three independent tracks.**

Built using the supplied [Granth skill](https://github.com/aignishant/granth-skill), adapted
to your daily schedule and five years of Python experience. This is the full daily assignment
plan and practice workspace; long-form Granth teaching chapters can be expanded as you study.

| Track | Daily budget | Focus |
| --- | --- | --- |
| `dsa` | 60 minutes | 144 core problems, runnable starter tests, hints, optional extensions and 24 reviews |
| `sd` | 30 minutes | Fundamentals, distributed systems, case studies and design defenses |
| `lang` | 15 minutes | Python internals, typing, concurrency, testing, profiling and production code |

Every seventh session reviews the previous six. You can study the three tracks separately and
keep independent progress. The 168-day length is a recommendation; hard problems can need extra
calendar sessions. See the overload policy in the master plan.

DSA now targets product-company interview preparation, including your Google goal. Each daily
DSA folder includes a LeetCode companion with difficulty and contract-comparison notes. Use it
as the main attempt within the existing hour. See the [full LeetCode index](docs/LEETCODE_INDEX.md)
and [interview practice method](docs/INTERVIEW_PREP.md). Premium companions have local free alternatives.

## Start here

1. Open [Day 1](days/day-001-count-target-values/LESSON.md), then choose a subject README.
2. Follow its **Navigation — where to start** section: explanation → trace → readiness →
   assignment → implementation → verification → evidence.
3. For later reading without practice, use [DSA recall](docs/DSA_RECALL.md),
   [Python recall](docs/LANG_RECALL.md), or [system design recall](docs/SD_RECALL.md).

Days 1–40 have full topic explanations across all three tracks, with worked traces, observed
teaching failures, readiness checks, and recall cards. Find them in the
[expanded teaching index](days/README.md#expanded-teaching-days). The newest block starts at
[Day 37](days/day-037-middle-node/LESSON.md) and ends at
[Day 40](days/day-040-remove-from-end/LESSON.md). Days 7, 14, 21, 28, and 35 begin with
cold attempts before repair reading. Days 41–168 have preparation navigation until expanded.
[The teaching workflow](docs/TEACHING_WORKFLOW.md) makes
explanations and recall cards part of every future day expansion.

For system design, Days 1–40 also include a complete **REFERENCE_DESIGN.md** written by the
assistant. **DESIGN.md** is your practice file: its `TODO(me)` prompts are for you when you
choose to practice. Read the reference first for guidance or compare after your own attempt;
on weekly review days, open the reference only after the cold review attempt.
See [the SD workflow and reference index](docs/SD_DESIGN_GUIDE.md#who-fills-the-todos).
Future expanded SD days include both files; reading alone does not mark study complete.

- [Master plan and all 168 daily assignments](docs/00_MASTER_PLAN.md)
- [Day 1](days/day-001-count-target-values/LESSON.md)
- [DSA practice guide](docs/PRACTICE_GUIDE.md)
- [DSA pattern notes](docs/DSA_PATTERN_GUIDE.md), [design method](docs/SD_DESIGN_GUIDE.md), [Python lab method](docs/PYTHON_LAB_GUIDE.md)
- [Independent progress instructions](docs/STUDY_WORKFLOW.md)
- [Source references](docs/SOURCES.md)

```powershell
python course.py start 1 --track dsa
python course.py practice 1
python course.py status
```

The practice command **fails initially by design**: implement `solve(data)` first. Provided
examples are smoke tests; add your own boundary and counterexample tests before marking complete.
No exercise solution has been filled in for you. Python 3.12 is the lab baseline; no dependencies
or paid services are needed to start.

## Folder shape

```text
days/day-001-count-target-values/
  LESSON.md
  CHECKLIST.md
  dsa_count-target-values/       README, PRACTICE, LEETCODE, HINTS, solution, cases, tests, notes
  sd_functional-scope/           README, DESIGN
  lang_identity-and-equality/    README, lab, notes
```

All 168 days use the same `track_topic-title` naming convention. CLI aliases stay `dsa`, `sd`
and `lang`; old IDE tabs should reopen the files under their new topic-named folders.

## Verify the course

```powershell
python course.py check
python granth.py doctor
python granth.py index
python granth.py check
```

Granth's indexes describe planning/authoring. They show assignment hubs, not completed study or
full teaching chapters. Use `course.py status` for independent study progress. Read the
[adaptation decision](docs/adr/ADR-0001-the-plan-as-adopted.md) for the preserved upstream tool's
limits. Do not use its `done` command for this workflow: it stages and commits the whole tree.
