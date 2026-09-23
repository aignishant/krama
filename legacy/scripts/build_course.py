"""Archived v1.0 authoring source. Do not rebuild an active v1.1 course with this file.

Topic-folder paths and LeetCode companions are defined by docs/sessions.json and the v1.1
migration. This source is retained for provenance, not as the current generator.
"""
from pathlib import Path
import csv
import hashlib
import io
import json
import re

from course_data import weeks

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-18'
DATA = weeks()


def put(path, text):
    target = ROOT / path
    if target.exists():
        raise FileExistsError(f'Refusing to overwrite {path}')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + '\n', encoding='utf-8')


def slug(title):
    return '-'.join(re.sub('[^a-z0-9]+', ' ', title.lower()).split()[:4])


def day_folder(n):
    week, offset = divmod(n - 1, 7)
    title = DATA[week]['dsa'][offset][0] if offset < 6 else f'week {week+1} review'
    return f'day-{n:03d}-{slug(title)}'


def day_link(n, track='dsa'):
    return f'../../{day_folder(n)}/{track}/README.md'


def extract_templates():
    raw = (ROOT / 'vendor/granth/SKILL.md').read_text(encoding='utf-8')
    found = {}
    for match in re.finditer(r'^### `([^`]+)`\s*\n.*?^````\w*\n(.*?)^````\s*$', raw, re.M | re.S):
        found[match[1]] = match[2]
    return found


TEMPLATES = extract_templates()
SUBS = {'PROJECT_NAME': 'Krama', 'PROJECT_SLUG': 'krama', 'PLAN_VERSION': 'v1.0.0',
        'DRIVER': 'python granth.py', 'DATE': DATE, 'TOTAL_DAYS': '168',
        'TOPIC': 'DSA, system design and advanced Python', 'FIRST_DAY': '1'}


def substitute(text):
    for key, value in SUBS.items():
        text = text.replace('{{' + key + '}}', value)
    return text


def main():
    # Record the adaptation before creating the day assignments.
    put('docs/adr/ADR-0001-the-plan-as-adopted.md', '''# ADR-0001 — Separate tracks with a fixed daily budget

- Date: 2026-09-18
- Status: accepted for the initial course; duration is an author assumption
- Related: [master plan](../00_MASTER_PLAN.md)

## Context

The user requested DSA, system design and Python in exactly three subject folders per day,
with 60, 30 and 15 minutes respectively. Python experience is five years. The supplied
Granth skill normally forbids clocks, uses shared parts/source/lab folders, and guards all
subjects with one progress ledger. Those defaults conflict with the user's explicit needs.
The working tree also contains pre-existing tracked deletions; no restore or commit is authorized.

## Decision

Use 168 study days grouped into 24 weeks, with six topic days and a seventh review day.
Every day has dsa/, sd/ and lang/. Each contains an immediately usable guided assignment.
Full Granth eleven-section teaching chapters are a separate, on-demand expansion, not claimed
to be written by these assignment briefs. Preserve granth.py verbatim for plan indexing;
course.py validates the adapted format and runs practice. Keep independent track progress.
All source code exercises remain unsolved. Timing is a cap, not a mastery guarantee.

## Options considered

| Option | Decision |
| --- | --- |
| Unmodified Granth layout and no clocks | Reject: contradicts the requested daily budget and folders. |
| One combined daily lesson and progress flag | Reject: prevents independent study of the three tracks. |
| Short topic list | Reject: omits practice contracts, revision and daily deliverables. |
| 168-day guided course with optional deep chapters | Adopt: broad coverage with explicit scope and manageable daily tasks. |

## Consequences

The three tracks can progress at different speeds. Scope is 144 new DSA problems and 24 review
sessions, not a promise of mastery of every algorithm. Hard problems can require additional
study days. The custom checker is necessary because upstream depth checks require a different
layout and forbid clocks. Passing structural checks does not certify learning or deep prose.
The upstream done command stages and commits all changes, so it is excluded from the study workflow.
Revisit the duration after week 2 using actual solve rate; append a new decision before renumbering.
''')
    put('granth.py', TEMPLATES['granth.py'])
    put('granth.toml', '''[project]
name = "Krama"
slug = "krama"
topic = "DSA, system design and advanced Python"
plan_version = "v1.0.0"
driver = "python granth.py"

[paths]
plan = "docs/00_MASTER_PLAN.md"
docs = "docs"
days = "days"

[toolchain]
lint = ""
format_check = ""
test = "python course.py check"
''')
    put('.gitignore', '__pycache__/\n*.pyc\n.venv/\n.pytest_cache/\n.env\n.env.*\n!.env.example\n*.key\n*.pem\n')
    for name in ('PINS', 'SOURCES', 'GLOSSARY', 'PROVENANCE', 'CHANGELOG_PLAN'):
        body = substitute(TEMPLATES[f'docs/{name}.md'])
        if name == 'PINS':
            body += '\n| Python | 3.12.10 | 2026-09-18 | setup | Observed with `python --version`; tools require 3.11+; practice baseline is 3.12. |\n'
        elif name == 'PROVENANCE':
            digest = hashlib.sha256((ROOT / 'vendor/granth/SKILL.md').read_bytes()).hexdigest()
            body += f'\n| Granth | https://github.com/aignishant/granth-skill | Local skill SHA256 `{digest}` | MIT; see ../vendor/granth/LICENSE | {DATE} | Course author, code inspection | Local plan parsing/index generation; no done/commit command executed. |\n'
        elif name == 'CHANGELOG_PLAN':
            body += '\n- 2026-09-18 — Initial adaptation: timed independent tracks and guided assignments; 168-day scope assumed. All 168 days affected. See ADR-0001.\n'
        elif name == 'SOURCES':
            body += '''
| spec:python-3.12-library | The Python Standard Library | rolling | https://docs.python.org/3.12/library/index.html | 2026-09-18 | assigned reference | Python track |
| spec:python-data-model | 3. Data model | rolling | https://docs.python.org/3/reference/datamodel.html | 2026-09-18 | assigned reference | Python track; compare version before using new behavior |
| spec:algorithms-2020 | Introduction to Algorithms | 2020 | https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ | 2026-09-18 | assigned reference | DSA track |
| RFC 9110 | HTTP Semantics | 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | 2026-09-18 | assigned reference | SD weeks 1–3 |
| spec:postgres-concurrency | Chapter 13. Concurrency Control | rolling | https://www.postgresql.org/docs/current/mvcc.html | 2026-09-18 | assigned reference | SD database and transaction sessions |
| spec:consensus-paper | In Search of an Understandable Consensus Algorithm | 2014 | https://raft.github.io/raft.pdf | 2026-09-18 | assigned reference | SD coordination sessions |
| spec:sre-book | Site Reliability Engineering — Table of Contents | rolling | https://sre.google/sre-book/table-of-contents/ | 2026-09-18 | assigned reference | SD reliability and operations |

These landing pages/records were opened live. Individual linked chapters are assigned readings,
not claims of a fresh verification of every interface. Recheck the exact versioned page before
each lab. Case-study workloads and service targets are hypothetical design inputs.
'''
        put(f'docs/{name}.md', body)
    put('docs/PROGRESS.md', '''# Whole-course progress

No study work has been completed on behalf of the learner. Append a row only when all three
tracks for that study day meet their acceptance criteria. Daily activity belongs in the
independent [track ledger](TRACK_PROGRESS.csv), including partial and unsuccessful attempts.
Granth reports aggregate progress; course.py status reports each track independently.
Writing an assignment never closes its objective IDs.

| Day | Date | IDs closed | Evidence | Gates green? |
| --- | --- | --- | --- | --- |
''')
    put('docs/adr/README.md', '# Decisions\n\n| Record | Status |\n| --- | --- |\n| [0001 — timed independent tracks](ADR-0001-the-plan-as-adopted.md) | accepted |')
    put('docs/adr/ADR-0000-template.md', TEMPLATES['docs/adr/ADR-0000-template.md'])
    put('docs/GRANTH_REFERENCE.md', '# Upstream reference\n\nThe [vendored skill](../vendor/granth/SKILL.md) preserves the full original contract and templates.\nThe [adaptation decision](adr/ADR-0001-the-plan-as-adopted.md) and master plan define this course.\n`granth.py` is copied verbatim; its depth command applies only to future full teaching chapters,\nnot these timed assignments. Its `done` command stages all files and commits; use manual progress tracking here.\n')

    plan = '''---
plan: krama
version: "v1.0.0"
days: 168
tracks: 3
ids: 504
phases: 24
---

# Krama — master course plan

## 1 · Outcome and assumptions

Krama means sequence: steady practice in three independently usable tracks. The assumed goal
is strong software-engineering and interview readiness, not competitive-programming specialization.
Python assumes five years of practical experience; DSA and design start with a diagnostic foundation.
Duration is 168 study days, or 24 weeks at seven sessions per week. At six sessions per week it
takes 28 calendar weeks. The count is an initial recommendation, not a user-specified deadline.

The deliverable is a complete daily assignment course and practice workspace. Deep eleven-section
Granth chapters are not prewritten. Official references supply further teaching; daily exercises
have explicit outcomes, and DSA includes original self-contained problem statements and examples.
504 IDs identify session outcomes, including assessments; they are not 504 unrelated concepts.

## 2 · Principles

Study tracks independently and in their own order. Write a hypothesis before code. Start with a
simple correct baseline, then explain the improvement. Record failed attempts. Leave exercises
unsolved until you do them. Every test must be capable of detecting a real mistake. Cite actual
sources, distinguish assumptions from observations, and keep algorithmic complexity separate from
runtime measurements. Completion means evidence and explanation, not merely reading a page.

## 3 · Portfolio

DSA: tested solutions, complexity arguments, counterexamples, a mistake log and cold re-solves.
System design: short decision memos, sequence/component diagrams and case studies ending in a
defensible design portfolio. Python: focused experiments and a tiny local job runner, with tests
for cleanup, concurrency and failure paths. No cloud deployment or paid platform is required.

## 4 · Daily budget and overload policy

| Track | Daily cap | Session allocation |
| --- | --- | --- |
| dsa | 60 minutes | 5 recall + 10 concept/trace + 30 core attempt + 10 tests/explanation + 5 log |
| sd | 30 minutes | 5 recall + 10 reference/concept + 12 one design deliverable + 3 critique |
| lang | 15 minutes | 3 predict + 8 experiment + 4 explain/test |

Total: 105 minutes daily. Across 168 sessions the budget is 168 DSA hours, 84 design hours and
42 Python hours. Optional exercises replace spare time; they never add mandatory time. Hard DSA
sessions may use the whole attempt window for deriving a baseline and invariant. Mark partial,
then use review time to finish; do not label an unfinished exercise mastered. If more than two
core problems remain unresolved at a weekly gate, pause that track's new topics and use additional
calendar sessions. Other tracks can continue. The 168-day map is a sequence, not a deadline.

## 5 · Environment and sources

Local Python observed: 3.12.10; scripts use only the standard library. Tooling requires Python
3.11+; core experiments target 3.12. Newer interpreter topics require reading version notes and
are not claimed to run on 3.12. Use PowerShell from the repository root. No package installation
is needed to begin. See [sources](SOURCES.md), [pins](PINS.md) and [provenance](PROVENANCE.md).

## 6 · Tracks

<!-- granth:tracks:start -->
| Track | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Data structures and algorithms | DSA | 168 | Correctness, implementation, complexity and cold practice |
| System design | SD | 168 | Requirements, scale, data, failures and tradeoffs |
| Advanced Python | PY | 168 | Semantics, maintainability, runtime behavior and production code |
<!-- granth:tracks:end -->

## 7 · Weekly phases

Each phase has six topic sessions and a seventh review. Pass each track separately. A DSA gate
requires two cold re-solves with tests and explanations; SD requires a revised design artifact
and one failure walkthrough; Python requires a bug reproduction/fix and a spoken explanation.

<!-- granth:phases:start -->
| Phase | Days | Theme | Gate |
| --- | --- | --- | --- |
'''
    for w in DATA:
        start, end = (w['week']-1)*7+1, w['week']*7
        plan += f"| {w['week']} | {start}-{end} | {' / '.join(w['themes'])} | Two cold DSA re-solves; one SD defense; one Python regression test. |\n"
    plan += '<!-- granth:phases:end -->\n\n## 8 · Complete day map\n\nThe third column assigns IDs; each ID belongs to exactly one day.\n\n<!-- granth:day-map:start -->\n'
    sessions = []
    for w in DATA:
        plan += f"\n### Phase {w['week']} — {w['themes'][0]}\n\n| Day | Title | IDs assigned |\n| --- | --- | --- |\n"
        for offset in range(7):
            n = (w['week']-1)*7+offset+1
            titles = [w[t][offset][0] for t in ('dsa','sd','lang')] if offset < 6 else [f"Week {w['week']} {t} review" for t in ('DSA','design','Python')]
            ids = [f'{prefix}-{n:02d}' for prefix in ('DSA','SD','PY')]
            plan += f"| {n} | DSA: {titles[0]}; SD: {titles[1]}; Python: {titles[2]} | {', '.join(ids)} |\n"
            sessions.append({'day':n, 'week':w['week'], 'folder':day_folder(n), 'titles':titles, 'ids':ids, 'review':offset==6})
    plan += '''<!-- granth:day-map:end -->

## 9 · Assessment and retention

DSA scores each of correctness, explanation, complexity and test quality from 0 to 2. Pass a
weekly gate at 6/8 or above with correctness=2, including at least one cold solve without hints.
Design scores requirements, data/API, scale and failure tradeoffs from 0 to 2; pass at 6/8 with
no unexplained source of truth. Python passes when you can predict, run, explain and test one
subtle behavior without copying an answer. Scores are diagnostic, not employment guarantees.

Recall prior work at study-day offsets +1, +7 and +21. Daily links list candidates: choose one
for the five-minute recall budget; use weekly review for full re-solves. Missed reviews become
a queue, not three additional mandatory problems. After day 168, use the review queue for
four further weekly retention sessions; these are optional maintenance beyond this plan.

## 10 · Progress and traceability

[TRACK_PROGRESS.csv](TRACK_PROGRESS.csv) is an append-only event ledger: day, track, status,
date, evidence and notes. Status is not-started, partial, needs-review or complete; the latest
row for each pair is current. `python course.py status` shows independent next sessions.
[PROGRESS.md](PROGRESS.md) records a whole day only after all three tracks pass. No study
completion is prefilled. Generated Granth indexes are a plan/authoring view, not the independent
study ledger. A hub-only status is expected for guided assignments without deep chapters.

## 11 · Adapted day contract

Each day contains exactly dsa/, sd/ and lang/, plus an orienting LESSON.md and CHECKLIST.md.
DSA has README.md, PRACTICE.md, HINTS.md, solution.py, cases.json, test_solution.py and NOTES.md.
Review days point to explicit earlier core problems and have their own replacement solve target.
SD has a bounded assignment, design-response template and checklist. Python has a focused lab
assignment, unsolved lab.py and notes. Each subject can be opened without reading the other two.

A complete practice session includes understanding the contract, a baseline, an independent
attempt, boundary tests, a complexity argument and a failure note. Provided example fixtures are
smoke checks, not exhaustive correctness proofs. Add your own cases and a small brute-force oracle
where feasible. Solutions intentionally raise NotImplementedError until you implement them.

Full teaching chapters may later be written within each subject folder, one idea per document,
with motivation, mechanism, real failure evidence and production implications. Consult the
vendored Granth contract for that expansion. Never disguise assignment briefs as full chapters.
Use `python course.py check` for this format. Upstream `granth.py depth` cannot validate it;
its no-clock/parts-folder assumptions remain unchanged in the preserved upstream code.

## 12 · Teaching and practice style

Use plain language and explicit contracts. Explain why a pattern applies before writing code.
Draw state or data flow where it clarifies an invariant. Keep hints separate and staged. No solved
learner reps. Name actual observed failures; never fabricate a traceback or benchmark. Python
does not repeat beginner syntax, loops or basic function lessons. State CPython-specific behavior
as such. Advanced and optional work must fit spare time or a later review session.

## 13 · Amendments

2026-09-18: v1.0.0 adopted with the user's timing/layout overriding upstream defaults; see
[ADR-0001](adr/ADR-0001-the-plan-as-adopted.md). Scope, sequencing or layout changes require an
append-only decision and changelog entry before renumbering. No automatic commit is part of study.
'''
    put('docs/00_MASTER_PLAN.md', plan)
    put('docs/sessions.json', json.dumps(sessions, indent=2))
    put('docs/TRACK_PROGRESS.csv', 'day,track,status,date,evidence,notes')
    put('docs/MISTAKES.csv', 'day,track,problem_or_topic,wrong_assumption,minimal_counterexample,repair,next_review,status')
    put('docs/REVIEW_QUEUE.csv', 'source_day,track,due_study_day,review_kind,status\n' + '\n'.join(f'{n},dsa,{n+gap},{"cold-solve" if gap>1 else "recall"},pending' for n in range(1,169) if n%7 for gap in (1,7,21)))

    for s in sessions:
        n, w = s['day'], DATA[s['week']-1]
        offset = (n-1)%7
        base = f"days/{s['folder']}"
        put(f'{base}/LESSON.md', f'''---
day: {n}
phase: {s['week']}
title: "{s['titles'][0]}"
ids: []
kind: guided-assignment
plan_version: "v1.0.0"
parts: 0
generated: "{DATE}"
status: planned
---

# Day {n:03d}

This is a guided assignment hub. Assigned IDs: {', '.join(s['ids'])}; none are claimed completed.

| Subject | Budget | Open |
| --- | --- | --- |
| DSA | 60 minutes | [{s['titles'][0]}](dsa/README.md) |
| System design | 30 minutes | [{s['titles'][1]}](sd/README.md) |
| Python | 15 minutes | [{s['titles'][2]}](lang/README.md) |

You may take these in separate sittings and progress at different speeds.
Read the relevant subject only, then record evidence in that track's notes and ledger.
See [daily checklist](CHECKLIST.md) and [master plan](../../docs/00_MASTER_PLAN.md).
''')
        put(f'{base}/CHECKLIST.md', '# Daily track completion\n\n- [ ] DSA core and its acceptance criteria complete.\n- [ ] SD deliverable and critique complete.\n- [ ] Python experiment and explanation complete.\n- [ ] Append separate track results; append whole-day progress only when all three pass.\n')
        chosen = w['dsa'][offset] if offset < 6 else w['dsa'][4]
        title, contract, inp, out, target, hint = chosen
        assigned = title if offset < 6 else f'Cold re-solve: {title}'
        source_day = n if offset < 6 else n-2
        recall = [n-gap for gap in (1,7,21) if n-gap>0]
        recall_links = ', '.join(f'[day {p}]({day_link(p)})' for p in recall) or 'No earlier session; state your baseline confidence.'
        prerequisite = 'Comfort writing and running Python functions; DSA knowledge is diagnosed here.' if n==1 else f'Prior DSA session: [day {n-1}]({day_link(n-1)}). Read only its notes if already comfortable.'
        put(f'{base}/dsa/README.md', f'''# Day {n:03d} DSA — {s['titles'][0]}

**Budget:** 60 minutes. **Outcome:** {s['ids'][0]}. **Theme:** {w['themes'][0]}.

## Prerequisite and recall

{prerequisite}
Recall one candidate, not all of them: {recall_links}

## Session

| Step | Minutes | Work |
| --- | --- | --- |
| Recall | 5 | Explain a previous invariant without notes. |
| Understand | 10 | Read the contract; trace a small example; choose a baseline. |
| Solve | 30 | Implement the core problem in solution.py without reading hints first. |
| Verify | 10 | Run tests, add boundary cases, explain time and space. |
| Record | 5 | Write the mistake, evidence and next review. |

## Core assignment

**{assigned}.** {contract}

Start in [PRACTICE.md](PRACTICE.md). The invariant to investigate is kept in
[HINTS.md](HINTS.md), so the first attempt remains independent. Expected target: {target}.
This is a target to justify, not a claim that any implementation meets it.

## Learn and explain

Read [week {s['week']} in the DSA pattern guide](../../../docs/DSA_PATTERN_GUIDE.md)
for this week's mechanism before the first attempt.

Before optimizing, write what a straightforward correct algorithm would enumerate or maintain.
On the sample, record the changing state after each meaningful step. Identify what remains true
before and after an update. Explain why termination gives the required answer and whether output
order or mutation is part of the contract. Include Python slicing, sorting and integer costs
when they materially affect your complexity claim.

Reference: [Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
Use the lecture notes matching **{w['themes'][0]}** for additional teaching; reading the whole
course is not assigned. Advanced topics beyond that reference are introduced by their practice
contracts and staged hints; use a review session for deeper derivations.

## Done when

- [ ] I can restate the contract, including ties, empty input and mutation rules.
- [ ] The core solution passes provided and self-authored tests.
- [ ] I can justify correctness and the time/space bound.
- [ ] I recorded a wrong approach or counterexample and can explain its repair.
- [ ] I logged complete, partial or needs-review honestly.

If time expires, record the next concrete step in [NOTES.md](NOTES.md). The optional extension
replaces spare time; it is never additional required work.
''')
        review = ''
        if offset == 6:
            review = f'''## Weekly assessment

Use the 60-minute session as 5 recall + 20 re-solve + 20 second re-solve + 10 critique + 5 log.
First re-solve [day {n-6}]({day_link(n-6)}), then the core below from
[day {source_day}]({day_link(source_day)}), both from blank code. A harder unresolved problem
may replace the second. The local fixture checks the second problem only; run the first day's
tests against your first re-solve too. Score correctness/explanation/complexity/tests 0–2 each;
pass at 6/8 with correctness=2 and at least one hint-free solve. Review is not a new problem.

'''
        put(f'{base}/dsa/PRACTICE.md', f'''# Practice — {assigned}

{review}## Contract

{contract}

Implement `solve(data)` in [solution.py](solution.py). `data` is the JSON object below.
Return the described JSON-compatible result. Python uses `None`, `True` and `False` for JSON
null/true/false. All unspecified inputs satisfy the stated preconditions; define any additional
edge behavior before adding a case. Numbers use the usual unit-cost interview model unless
you explicitly analyze arbitrary-size integer operations. Tree inputs are null or nested
`[value,left,right]`; graphs use integer vertices; linked-list tasks must build real nodes.

## Example

Input:
```json
{inp}
```

Expected output:
```json
{out}
```

## Complete practice sequence

1. Restate inputs, outputs, valid ranges, tie rules and allowed mutation.
2. Describe a simple baseline and its cost; keep it as a small-input oracle where practical.
3. Trace the example by hand and state one invariant or recurrence.
4. Implement independently. After a sustained attempt, reveal one hint at a time.
5. Run `python course.py practice {n}` from the repository root. The starter is intentionally RED.
6. Add at least four independent cases to cases.json: smallest valid input, repeated/equal
   values when allowed, an adversarial ordering or topology, and a boundary/no-answer case.
7. If practical, compare random tiny inputs with the baseline using a fixed seed.
8. Deliberately introduce one plausible bug, observe a failing test, then undo the bug.
9. Explain correctness, time, auxiliary space and output space. Target: **{target}**.
10. Record whether you solved independently or used hints; schedule a cold re-solve.

## Optional extension

Change one contract assumption (tie rule, online arrival, mutation permission or duplicate
policy). Write the new contract and a distinguishing test before adapting the solution. Explain
which invariant survives and which fails. Skip this if the core or due review needs the time.

## Evidence

Record test command/output, four added cases, the invariant, complexity and the minimal failure
in [NOTES.md](NOTES.md). The provided sample is a smoke test, not an exhaustive judge.
''')
        put(f'{base}/dsa/HINTS.md', f'''# Hints — {title}

Open only after an independent attempt. These guide the mechanism without supplying a solution.

<details><summary>Hint 1 — representation</summary>

{hint}

</details>

<details><summary>Hint 2 — proof obligation</summary>

Write the state immediately before an update and immediately after it. Identify which discarded
possibilities can no longer improve the answer. For recursive/DP tasks, state the subproblem
and why every dependency is smaller or already available.

</details>

<details><summary>Hint 3 — targeted debugging</summary>

Find the smallest valid input on which your baseline and optimized versions disagree. Compare
their state traces at the first divergence, including equality, initial state and final cleanup.
Recheck the contract before changing the algorithm.

</details>
''')
        put(f'{base}/dsa/solution.py', f'"""{title}. See PRACTICE.md for the complete contract."""\n\ndef solve(data):\n    # TODO(me): implement and explain the invariant before optimizing.\n    raise NotImplementedError("TODO(me): solve the core exercise")\n')
        put(f'{base}/dsa/cases.json', json.dumps([{'name':'specified example','input':json.loads(inp),'expected':json.loads(out)}], indent=2))
        put(f'{base}/dsa/test_solution.py', '''"""Run directly, or with python course.py practice N from the root."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('exercise_solution', HERE / 'solution.py')
solution = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution)


class ExerciseCases(unittest.TestCase):
    def test_cases(self):
        cases = json.loads((HERE / 'cases.json').read_text(encoding='utf-8'))
        self.assertTrue(cases, 'Keep at least one example case.')
        for case in cases:
            with self.subTest(case=case['name']):
                actual = solution.solve(copy.deepcopy(case['input']))
                self.assertEqual(actual, case['expected'])


if __name__ == '__main__':
    unittest.main()
''')
        put(f'{base}/dsa/NOTES.md', '''# My DSA evidence

- Attempt date and status:
- Baseline and why it is correct:
- Invariant or recurrence:
- Complexity (time / auxiliary / output space):
- Added edge cases:
- Actual test command and output:
- Wrong approach and minimal counterexample:
- Hints used:
- Next step or cold review date:
''')
        for track in ('sd','lang'):
            title, task = w[track][offset] if offset<6 else (f"Week {s['week']} review", '')
            track_index = 1 if track=='sd' else 2
            if offset==6:
                task = (f'Revisit days {n-6}–{n-1}. Choose your weakest design decision, revise its diagram or memo, then defend one alternative and walk through one failure.' if track=='sd' else f'Revisit days {n-6}–{n-1}. From memory reproduce one surprising behavior, write a regression test for its repair, and explain the mechanism.')
            budget = 30 if track=='sd' else 15
            split = '5 recall + 10 concept/reference + 12 design + 3 critique' if track=='sd' else '3 predict + 8 experiment + 4 explain/test'
            ref = ('[HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html), [consensus paper](https://raft.github.io/raft.pdf), and [reliability book contents](https://sre.google/sre-book/table-of-contents/). Choose the section relevant to this assignment; do not read all four.' if track=='sd' else '[The Python Standard Library](https://docs.python.org/3.12/library/index.html) and [Data model](https://docs.python.org/3/reference/datamodel.html). Use the named module or protocol; compare version notes with your local interpreter.')
            put(f'{base}/{track}/README.md', f'''# Day {n:03d} — {title}

**Track:** {track}. **Budget:** {budget} minutes ({split}). **Outcome:** {s['ids'][track_index]}.
**Weekly theme:** {w['themes'][track_index]}.

## Assignment

{task}

## Work method

{('Produce one bounded artifact: a small diagram, a calculation with units, a state table or a short decision memo. Label assumptions before reasoning from them. Trace one concrete request or failure through the result. Compare at least one alternative and state why your choice fits the requirements.' if track=='sd' else 'Predict the behavior before running code. Write a tiny experiment in lab.py using the local interpreter, observe its actual output, then add an assertion covering the surprise or failure. Finish with a short explanation of the mechanism and where it matters in production. Basic Python syntax is assumed.')}

## References

Read the [{('system design method' if track=='sd' else 'Python lab method')}](../../../docs/{('SD_DESIGN_GUIDE' if track=='sd' else 'PYTHON_LAB_GUIDE')}.md) when starting this track.

{ref}
Source records were checked on {DATE}; fetch the exact relevant section when studying.
For later case studies, reuse earlier track notes rather than adding a new reading project.

## Acceptance check

- [ ] I completed the specific assignment above and saved evidence.
- [ ] I can explain the mechanism or tradeoff without reading my notes.
- [ ] I named one failure or counterexample and the response to it.
- [ ] I distinguished an assumption from an observed result.
- [ ] I recorded complete, partial or needs-review in the independent track ledger.

{('Save the answer in [DESIGN.md](DESIGN.md). Full service implementation is not required.' if track=='sd' else 'Save observations in [NOTES.md](NOTES.md). Run lab.py from its folder or by its full relative path; no packages are required for the core experiments.')}
When the cap is reached, record the next step. Continue this track later without blocking the other two.
''')
            if track=='sd':
                put(f'{base}/sd/DESIGN.md', f'''# Design evidence — {title}

## Required output

{task}

## Assumptions and requirement

TODO(me): state the workload, target or constraint relevant to this task; do not invent a measured fact.

## Diagram, calculation or state trace

TODO(me): show the requested artifact with labeled units, arrows, ownership or transitions.

## Decision and alternative

TODO(me): explain the choice and one credible alternative. State what would make you change it.

## Failure walkthrough

TODO(me): trace a concrete failure, user impact and recovery. Name the invariant preserved or lost.

## Self-review

- What is still uncertain?
- What would I measure or verify next?
- Status and next step:
''')
            else:
                put(f'{base}/lang/lab.py', f'"""{title}. Read README.md, predict first, then implement the experiment."""\n\ndef main():\n    # TODO(me): write the experiment and a meaningful assertion.\n    raise NotImplementedError("TODO(me): run the Python experiment")\n\n\nif __name__ == "__main__":\n    main()\n')
                put(f'{base}/lang/NOTES.md', '# Python evidence\n\n- Prediction before running:\n- Interpreter version and command:\n- Actual observation or error:\n- Why it happens:\n- Regression assertion:\n- Production implication:\n- Status and next step:\n')
    # Canonical course entry and supporting instructions.
    put('days/README.md', '# Daily sessions\n\nOpen a numbered folder, then dsa/, sd/ or lang/. All 168 days have all three.\nThe full map is in [the master plan](../docs/00_MASTER_PLAN.md).\nUse `python course.py start 1 --track dsa` from the root to find the first assignment.\n')
    put('README.md', '''# Krama — DSA, system design and advanced Python

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

## Start here

- [Master plan and all 168 daily assignments](docs/00_MASTER_PLAN.md)
- [Day 1](days/day-001-count-target-values/LESSON.md)
- [DSA practice guide](docs/PRACTICE_GUIDE.md)
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
  dsa/   README, PRACTICE, HINTS, solution, cases, tests, notes
  sd/    README, DESIGN
  lang/  README, lab, notes
```

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
''')
    put('docs/PRACTICE_GUIDE.md', '''# DSA practice contract

This is a broad interview-oriented course. Advanced range queries, matching, bitmask DP and
tree rerooting provide breadth; deep competitive programming, geometry, FFT and advanced flow
are outside the core. A one-hour daily budget prioritizes one serious problem over a problem quota.

## What each section contains

Every core day supplies an original problem contract, JSON example, target complexity, unsolved
function, executable fixture test, staged hints, boundary-test instructions and evidence notes.
The statement is self-contained; no external judge account is required. Review days deliberately
repeat earlier problems and should not be counted as new problems.

## How to solve

1. Name the input size and clarify the contract.
2. Describe a slow correct baseline; do not optimize an undefined problem.
3. State the invariant or recurrence and trace one example.
4. Attempt independently, then use one hint if stuck.
5. Implement, run fixtures, and add four cases chosen to attack assumptions.
6. Use a small brute-force oracle or metamorphic property when appropriate.
7. Explain correctness, complexity, mutation and output ordering.
8. Keep the smallest failing input in the mistake ledger.

For lists test boundaries, duplicates and order. For trees test empty/skewed/balanced shapes when
allowed. For graphs test disconnected regions, self-loops only if allowed, cycles and unreachable
targets. For DP test base states, impossible states and zero-valued choices. For cache designs
test updates, repeated access, eviction ties and minimum capacity. A sample passing is insufficient.

## Weekly rubric

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Correctness | Cannot finish baseline | Needs hints or misses a case | Independently correct with tests |
| Explanation | Cannot state why | Describes steps | States and defends invariant/recurrence |
| Complexity | Wrong or missing | Mostly right | Accounts for relevant operations and space |
| Tests | Sample only | Some boundaries | Adversarial cases plus a demonstrated failure |

Pass at 6/8 or above with correctness=2. Otherwise mark needs-review and use the next review
session. More than two unresolved core problems means pause that track's new content. Optional
extensions and bonus readings are the first things to drop. Retention matters more than a streak.
''')
    put('docs/STUDY_WORKFLOW.md', '''# Study separately and record honestly

Run commands from the repository root. `python course.py start N --track dsa` (or sd/lang)
prints the path and assignment. `python course.py practice N` runs that day's DSA example tests.
The tool never opens a GUI, edits progress automatically, or commits your work.

## Independent progress

Append events to TRACK_PROGRESS.csv; keep old events. Allowed tracks: dsa, sd, lang.
Allowed statuses: not-started, partial, needs-review, complete. Example syntax only:

```csv
1,dsa,partial,2026-09-18,days/day-001-count-target-values/dsa/NOTES.md,Baseline written; add boundary tests
1,lang,complete,2026-09-18,days/day-001-count-target-values/lang/NOTES.md,Experiment and explanation recorded
```

Use your real dates and evidence. The latest event for each day/track is current. Quote CSV
fields containing commas. `python course.py status` shows counts and the first unfinished day
for each track. A complete flag is self-reported, not a certificate from the checker.

Check the boxes in each subject README only after its acceptance criteria pass. When all three
tracks for a day pass, tick its CHECKLIST and append the aggregate row to PROGRESS.md. Example:

```text
| 1 | actual-date | DSA-01, SD-01, PY-01 | links to the three evidence files | yes |
```

Then run `python granth.py index`. Assignment hubs intentionally claim no completed IDs; if
you want the upstream traceability view to reflect earned completion, set that day's hub ids
to exactly its assigned IDs only after all three gates pass. This is separate from authoring
full teaching chapters. Do not mark a subject complete because another subject is finished.

## Catch-up

Use the seventh session for unfinished core work, cold re-solves and a failure review. Keep
budgets unchanged. If a track stays behind, add calendar sessions to that track; never borrow
the Python or design budget silently. Resume from the first unfinished subject session.

REVIEW_QUEUE.csv schedules DSA recall at +1/+7/+21 study-day offsets. Pick one due recall in the
daily recall slot; use weekly sessions for full re-solves. After the course, due dates beyond
168 form optional maintenance. MISTAKES.csv records failed assumptions and minimal examples.
''')
    instructions = '''# Krama course operating rules

Read docs/00_MASTER_PLAN.md and docs/adr/ADR-0001-the-plan-as-adopted.md first.
The user's 60/30/15-minute budget and dsa/sd/lang layout override Granth's no-clock/shared-parts
defaults. Python assumes five years of experience. Preserve independent study progress.
The current deliverable is a guided assignment course; never call its briefs full depth-checked
teaching chapters. Use course.py check for the actual format and granth.py doctor/index for
planning. granth.py is preserved verbatim from vendor/granth/SKILL.md.

Read existing files before editing them. Do not overwrite learner solutions or notes. Never
complete learner TODO(me) exercises unless specifically requested. Record actual failures and
source checks, not reconstructed outputs. Do not restore old Git deletions or commit without
authorization. In particular do not invoke granth.py done, which stages the whole repository.

When expanding a day, work inside the requested subject folder, consult the full vendored
Granth teaching contract, verify exact interfaces, and keep core assignment versus optional
deep reading explicit. No assumption that finishing DSA is required before opening Python.
'''
    put('CLAUDE.md', instructions)
    put('.claude/skills/day-krama/SKILL.md', '''---
name: day-krama
description: Expand one Krama subject assignment into teaching parts while preserving its practice and the user's independent daily budgets.
---

Read CLAUDE.md, the master plan, ADR-0001 and the requested day's subject files. Ask which subject
only if it is genuinely ambiguous; a request for all three means all three. Use the vendored
Granth SKILL.md's full teaching contract for depth, but keep parts within dsa/, sd/ or lang/
and preserve the 60/30/15-minute core assignment. Mark deeper reading optional. Inspect that
track's progress rather than blocking on another track. Never overwrite learner code or notes.
Use one idea per document, a plain-language explanation, mechanism, observed failure, production
implication and a check. Keep exercise solutions unsolved. Verify sources when used. Run
python course.py check after writing, and report exactly which teaching documents were added.
''')
    print(f'Created {len(sessions)} days, 504 subject folders, 144 new DSA problems and 24 review sessions.')


if __name__ == '__main__':
    raise SystemExit('Archived v1.0 scaffolder: edit the current course using docs/sessions.json; do not regenerate learner work.')
