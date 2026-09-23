---
name: granth
description: Scaffold and run a depth-first, day-by-day curriculum repository for any topic — a master plan, progress and source ledgers, ADRs, CLAUDE.md, .claude/ skills, and a dependency-free toolchain that enforces the day format. Use when the user says "initiate <topic>", or asks to create a master plan, learning plan, study plan, curriculum, syllabus, course repo, roadmap or knowledge base with progress tracking and traceability; also to write the next day of an existing granth repo, add an ADR, amend a plan, or audit one. Triggers: initiate, master plan, curriculum, learning plan, study plan, syllabus, roadmap, "teach me X properly", "97 days", day-by-day, progress ledger, ADR, traceability.
argument-hint: "initiate <topic> | day <N> | adr <title> | amend <what changed> | audit | doctor"
---

# granth — a curriculum repository, forged from a topic

> **granth** (ग्रंथ) — a treatise: a work that carries a whole subject, in order, and can be
> handed to someone else.

This skill builds and maintains repositories in one specific shape: a **master plan** that is the
single source of truth, a **day map** that assigns every concept to exactly one day, **append-only
ledgers** that record what actually happened, **ADRs** for structural decisions, and a **depth
contract** that says what "covered properly" means — enforced by a dependency-free Python
toolchain, so the standard is checked and not merely stated.

**Everything this skill emits is in this file.** Part 2 below carries every file body verbatim.
Copy them; do not paraphrase them, and do not rewrite the Python from memory.

## The three ideas everything else follows from

1. **A day is a hub plus one document per subtopic**, never one long page. If a subtopic cannot be
   read on its own and explained back out loud, it has not been split finely enough.
2. **A day is a unit of subject, not of time.** No document carries a duration, an estimate or a
   pace. An explanation is never trimmed because a day is running long — the day gets another
   part instead.
3. **Never invent a fact.** Versions, interfaces and citations are looked up live on the day they
   are used, with a dated ledger row. A failed lookup leaves the exact command, never a guess.

---

## Routing

Read the argument. Match one verb and follow that section.

| The user says | Verb | Go to |
| --- | --- | --- |
| "initiate \<topic\>", "make me a curriculum/master plan for X", "scaffold a study repo" | **initiate** | [Part 1](#part-1--initiate) and [Part 2](#part-2--the-files-to-write) |
| "day 7", "write the next day", "continue" | **day** | [Writing a day](#writing-a-day) |
| "adr for X", "record this decision" | **adr** | [adr](#adr) |
| "the spec moved", "amend the plan", "X is deprecated now" | **amend** | [amend](#amend) |
| "audit this repo", "is this curriculum any good?" | **audit** | [audit](#audit) |
| "doctor", "something is broken" | **doctor** | [doctor](#doctor) |

**No verb, just a topic** (`granth machine learning`) → treat it as **initiate**, and say so in one
line before starting.

**Ambiguous** → ask. Do not guess between "scaffold a new repository" and "write the next day of
this one"; one of those two answers destroys work.

---

# Part 1 — initiate

## Step 0 · Preflight

Run these before anything else, and act on what they say.

```bash
pwd && ls -a
git rev-parse --is-inside-work-tree 2>/dev/null || echo "not a git repo"
test -f granth.toml && echo "ALREADY A GRANTH REPO"
```

| What you find | What to do |
| --- | --- |
| `granth.toml` exists | **Stop.** This is already a granth repository. Ask whether the user wants `doctor`, `day N`, or a genuinely new repository elsewhere. Never scaffold over an existing plan. |
| Not a git repository | Say so and offer `git init`. Do not run it silently — a repository created in the wrong directory is a mess to unpick. |
| Non-empty and unrelated | Name the files you can see and ask whether to scaffold **here** or in a new subdirectory. Do not guess. |
| `docs/00_MASTER_PLAN.md` without `granth.toml` | May be a hand-written plan. **Read it first.** Offer to adopt it — keep the content, add the markers and the toolchain — rather than overwrite. |
| Empty directory, or a fresh `git init` | Proceed. |

**Never overwrite a file you have not read.** If a target path exists, read it, show the user what
is there, and ask.

## Step 1 · Understand the topic before asking about it

1. **Search for the shape of the field.** Its canonical primary sources — papers, specifications,
   standards, RFCs. The tools people actually use. What changed recently enough that a plan written
   from memory would already be wrong.
2. **Find the natural divisions.** Most subjects fall into three to seven threads that run the
   whole length. Those become the tracks. If you cannot name them, the topic is either too small
   for a curriculum or too vague to plan yet — say so.
3. **Find the artifact.** The one thing a learner could build that exercises most of the subject.
   A curriculum with an artifact can ask "is this concept load-bearing?" and get a mechanical
   answer. One without an artifact drifts into a reading list.

Bring what you found into the interview as concrete proposals — "I'd suggest these five tracks;
here's why" — not as open questions. A user who has to invent the structure themselves did not
need this skill.

## Step 2 · The interview

Use `AskUserQuestion`. **At most two rounds of up to four questions.** Lead every question with
your recommendation, and say why.

### Round 1 — the four that change everything

| Question | Why it is expensive to change later |
| --- | --- |
| **Scope: how many days?** Offer short (20–30), standard (60–100), deep (150+), recommending from the concept count you actually found. | The day map is the spine. Changing the count renumbers every day and every folder. |
| **The artifact: what gets built?** Propose one concrete thing and one alternative. | Everything downstream is tested against it. |
| **The constraints:** budget, tools, platform, anything that must stay free or offline. | A constraint discovered on day 40 is a rewrite. |
| **The toolchain:** is there code that lints and tests, or is this reading and writing only? | Decides whether `check` has lint/test steps, and what `.gitignore` needs. |

### Round 2 — only if Round 1 left something genuinely open

The tracks (offer your proposed set for approval), whether the topic has primary sources worth
teaching in their own documents, and the project's name if the user has not given one.

### Decide these yourself, without asking

- The ID prefixes (derive from track names: `Agent Concepts` → `AG`).
- The phase boundaries (runs of 5–8 days sharing a theme, each ending at a gate you can state in
  one line).
- The plan version (`v1.0.0`) and the file layout (fixed — that is the point of the skill).
- Whether numbering starts at 0 or 1. **Recommend 0** when the first day is toolchain and
  repository setup closing no IDs, because a setup day that claims IDs makes every later count
  wrong.
- The name, if the user gave none: propose two or three short, memorable options **with their
  meaning**, because the plan's §1 asks for it. Slug is lowercase, no spaces.

## Step 3 · Design the curriculum

This is what separates a scaffold from a plan. Do it before writing any file, and **show the user
the day map before writing it to disk.**

**Tracks and IDs.** Three to seven tracks, each with a 2–4 letter uppercase prefix and a one-line
description of what runs through it. IDs are `PREFIX-NN` from `01` within each track, and **every
ID appears in exactly one day** — `doctor` fails if one appears twice. Aim for **1–3 IDs per day**;
a day with six IDs is four days wearing a trench coat.

**Phases.** Runs of roughly 5–8 days sharing a theme, each with a **gate you can state in one line
and actually check** — "the parser round-trips every fixture", "the service survives a restart
mid-request". A gate you cannot check is a heading. Phase 0, if used, is setup and closes no IDs.

**The day map.** One row per day: number, title, IDs. The title is a **phrase that says what the
day teaches**, not a category — "Tools by hand — schemas, the call, the result turn", not "Tools".
The folder slug is derived from it. Order by dependency, not neatness: the hand-rolled version of a
mechanism comes before the framework that hides it (Principle 3).

> **Write every day's row.** A day map with `... 40 more days ...` in it is not a plan: every tool
> that reads it will report a 12-day curriculum, and the user finds out on day 13. If the scope is
> large, this is the work — do it.

Print the tracks, the phases and the full day map. Ask for corrections. **Then** write files.

### Topic patterns — six shapes, and what changes for each

Say which pattern you think the topic is, and why. These are starting proposals, not answers.

| Pattern | Tracks | Artifact | Sources | Toolchain | What matters most |
| --- | --- | --- | --- | --- | --- |
| **Framework or SDK** <br>*Rust, React* | core model · framework surface · tooling · operations · testing | one application that grows all the way through | sometimes — design documents, RFC-style proposals | real | Principle 3: hand-roll the router or state store **once** before adopting the thing that does it, or the framework is a box you cannot debug. Put the exact `--version` command in §5 and re-run it at every gate. |
| **Research-heavy** <br>*transformers, consensus* | mathematics · architectures · training · evaluation · the failure literature | a small implementation that stays readable | **heavy** — most days get one | real, plus "does the demo still run" | The ablation switch. A demo without one proves code ran, not that the idea mattered — and telling those apart *is* the skill. |
| **Protocol or spec** <br>*HTTP, OAuth* | wire format · state machine · security · extensions · interop | a minimal client and server that talk to each other and to real implementations | **heavy and precise** — cite the revision, never "the spec" | real; conformance fixtures that go red | `When it breaks` carrying the real bytes: the actual status line, the actual error frame. Put "has the revision changed?" in the freshness check and mean it. |
| **No code at all** <br>*music theory, contract law* | vocabulary · the core system · exceptions · history · practice | still concrete: a portfolio, a case book, a composed piece | often — statutes, standards, foundational texts | **empty strings** — `check` then runs depth + index, which is right | Keeping the check that can go RED: an exercise with a wrong answer you can actually get. And `In production` = what a professional does under a real deadline or a real opponent. |
| **Ops and infra** <br>*Kubernetes, observability* | primitives · deployment · observability · reliability · security · cost | one service, deployed, watched, broken, recovered | some — postmortems, design documents | real, and the gate should actually run the thing | The **deliberate-failure part is the day**: kill it mid-request, fill the disk, partition the network. Principle 12 — every new power here can delete something real. |
| **Interview or exam prep** <br>*DSA, system design* | patterns · data structures · complexity · communication | a solved-and-explained set you could hand to someone else — the *explanations* are the artifact | occasionally | real: solutions have tests, tests go red first | Not solving the reps. `TODO(me)` stays unsolved, or you have produced a reading list with extra steps. |

**If the topic fits none of them**, design from four questions: what is the one thing worth
building? what three to seven threads run its whole length? what must stay true throughout? what
can go red at the end of a day? **If question 1 or 4 has no answer, the topic is not ready for a
curriculum** — say that plainly rather than scaffolding something that cannot check itself.

## Step 4 · Write the repository

Emit exactly this tree, using the file bodies in **Part 2** below. Substitute every `{{...}}`
placeholder; nothing is left unsubstituted anywhere.

```text
<repo>/
├── CLAUDE.md                          the operating rules every session reads first
├── README.md
├── granth.toml                        identity, paths, the contract's knobs
├── granth.py                          THE WHOLE TOOLCHAIN — copy verbatim, byte for byte
├── .gitignore
├── .env.example                       only if the topic needs secrets
├── docs/
│   ├── 00_MASTER_PLAN.md              the contract — this is the real work
│   ├── PROGRESS.md  PINS.md  SOURCES.md  GLOSSARY.md  PROVENANCE.md  CHANGELOG_PLAN.md
│   └── adr/  README.md  ADR-0000-template.md  ADR-0001-the-plan-as-adopted.md
├── days/
│   ├── README.md
│   └── _TEMPLATES/  LESSON.md  CHECKLIST.md  PART.md  SOURCE.md
└── .claude/
    ├── settings.json
    └── skills/day-<slug>/SKILL.md     the project's own day-writing skill
```

`docs/TRACEABILITY.md`, `docs/CURRICULUM_INDEX.md`, `docs/TRACKER.md`, `docs/WIKI.md` and
`docs/wiki/` are **not written by hand** — Step 5 generates them.

### The three repeated blocks

Three blocks in the master plan are **one row each** and must be expanded to as many rows as the
design needs. Getting this wrong is the most common way to produce a broken plan.

| Block | Markers | Expand to |
| --- | --- | --- |
| Tracks | `granth:tracks` | one row per track |
| Phases | `granth:phases` | one row per phase |
| Day map | `granth:day-map` | **one row per day**, under a `### Phase N — theme` heading per phase |

**Keep the markers exactly as written.** They are how `granth.py` reads the plan, and a heading
rename must never break a tool.

### Every placeholder

| Placeholder | Value |
| --- | --- |
| `{{PROJECT_NAME}}` | the display name |
| `{{PROJECT_SLUG}}` | lowercase, no spaces — used in folder and skill names |
| `{{NAME_MEANING}}` | one line: what the name means and why it fits |
| `{{TOPIC}}` | one line: what this curriculum teaches |
| `{{PLAN_VERSION}}` | `v1.0.0` |
| `{{DATE}}` | today, `YYYY-MM-DD` |
| `{{DRIVER}}` | `python granth.py` |
| `{{TOTAL_DAYS}}` `{{FIRST_DAY}}` `{{LAST_DAY}}` | from the day map |
| `{{PHASE_COUNT}}` `{{TRACK_COUNT}}` `{{ID_TOTAL}}` | counted from the design, not estimated |
| `{{END_STATE}}` | what exists on the last day, in one sentence |
| `{{NON_GOAL_1..3}}` | three things this curriculum deliberately does not do |
| `{{EXTRA_PRINCIPLES}}` | extra principles for this topic, numbered from 13, or empty |
| `{{ARTIFACT_DESCRIPTION}}` | a few paragraphs: what gets built, how it grows across the phases |
| `{{ARTIFACT_ONE_LINE}}` | the same in one line, for ADR-0001 |
| `{{CONSTRAINTS}}` | budget, tools, platform, and what each one implies |
| `{{CONSTRAINTS_ONE_LINE}}` | the same in one line, for ADR-0001 |
| `{{BASELINE_ROW_1..2}}` | table rows: what is pinned, to what, verified how, re-checked when |
| `{{FRESHNESS_1..2}}` | what to re-check at every phase gate |
| `{{SCOPE_RATIONALE}}` | why this many days and not fewer or more |
| `{{ONE_PARAGRAPH_PITCH}}` | the README's opening paragraph |
| `{{GITHUB_USER}}` | the user's GitHub handle, or drop the credit line |
| `{{ENVIRONMENT_BLOCK}}` | runtime, shell and package manager, as prose plus a code block |
| `{{LINT_COMMAND}}` `{{FORMAT_COMMAND}}` `{{TEST_COMMAND}}` | the real commands, or **empty strings** for a curriculum with no code |
| `{{ENV_VAR_1}}` `{{ENV_VAR_1_COMMENT}}` | one row per secret; drop `.env.example` if there are none |
| `{{TRACK_n_*}}` `{{PHASE_n_*}}` `{{DAY_n_*}}` | the repeated rows above |

The day templates under `days/_TEMPLATES/` carry `{{PROJECT_NAME}}`, `{{PLAN_VERSION}}` and
`{{DRIVER}}` — **substitute those too**. Their `NN`, `S.T` and `<slug>` markers are a different
thing and are meant to stay: a writer fills those in.

---

# Part 2 — the files to write

Each block below is one file, given whole. **`granth.py` in particular is copied verbatim** — it
is tested, and a rewritten-from-memory checker is a checker that passes everything.

### `granth.toml`

This repository's identity and the knobs the contract exposes.

````toml
# granth.toml - this repository's identity, and the knobs the depth contract exposes.
#
# The master plan is the single source of truth for *what the curriculum is*: the tracks, the
# phases and the day map all live there, between `<!-- granth:...:start -->` markers, so that a
# human reading the plan and a script parsing it can never disagree. This file holds only what
# the plan cannot express - where things live, and the shell commands of the local toolchain.
#
# Every key is optional. Delete a line to take the default.

[project]
name         = "{{PROJECT_NAME}}"     # how the project is named in generated documents
slug         = "{{PROJECT_SLUG}}"     # lowercase, no spaces; used in skill and folder names
topic        = "{{TOPIC}}"            # one line: what this curriculum teaches
plan_version = "v1.0.0"               # must match every hub's `plan_version` frontmatter
driver       = "python granth.py"   # how generated documents tell the reader to run commands

[paths]
plan = "docs/00_MASTER_PLAN.md"
docs = "docs"
days = "days"

[contract]
# Directory names inside a day folder.
parts_dir   = "parts"
sources_dir = "sources"

# The ladder every part declares. A day climbs it; a day that is all `foundation` is a tutorial,
# and a day that opens at `production` has skipped the reader.
levels = ["foundation", "working", "production"]

# Fenced blocks whose contents are output, a diagram or a config dump. They carry no logic, so
# the contract does not demand a walkthrough after them - demanding one would only teach padding.
no_walkthrough_langs = [
  "", "text", "console", "output", "traceback", "mermaid", "diff", "json", "toml", "yaml", "ini", "csv",
]

# Headings under which a code block is evidence rather than teaching.
exempt_headings = "when it breaks|check yourself|verify|budget|ledger|the map|setup"

# Every day carries at least one part whose subject is a deliberate failure. The part declares
# itself with `failure: true` in its frontmatter, because no script can recognise one by reading.
require_failure_part = true

# Every identifier a document cites must already have a dated row in docs/SOURCES.md. Set false
# only for a curriculum with no citable primary sources at all - and think twice before you do.
require_sources = true

# The eleven part sections, in the order the contract requires them. The order is the pedagogy:
# scene before definition, definition before mechanism, mechanism before failure, failure before
# production. Changing it is a plan amendment, not a preference.
part_sections = [
  "one-line answer",
  "the story",
  "the idea in plain language",
  "why this project needs it",
  "the source behind it",
  "the mechanism",
  "line by line",
  "the source in one demo",
  "when it breaks",
  "in production",
  "check yourself",
]

# The eleven hub sections, numbered in the hub as `## §1 ...` through `## §11 ...`.
hub_sections = [
  "Where we are",
  "The map",
  "Setup",
  "Build brief",
  "The check that must be able to fail",
  "Budget",
  "Traps",
  "Verify before you build",
  "Say it out loud",
  "Done when",
  "Ledger & commit",
]

# Reword a heading here if the project's voice needs it; the slot itself stays. The value is a
# regular expression matched against the heading text, case-insensitively.
# [contract.section_patterns]
# "why this project needs it" = "why .{0,40}needs? it"

[toolchain]
# Whatever this project runs to stay honest. Leave a value empty and `check` skips that step,
# which is the right setting for a curriculum with no code in it.
lint         = "{{LINT_COMMAND}}"
format_check = "{{FORMAT_COMMAND}}"
test         = "{{TEST_COMMAND}}"
````

### `granth.py`

**The whole toolchain. Copy it byte for byte — do not rewrite it from memory, and do not 'improve' it while copying.** Stdlib only, Python 3.11+.

````python
#!/usr/bin/env python3
"""granth — the whole toolchain for this curriculum repository, in one file.

    python granth.py status | brief N | start N | parts N | new N [slug]
                     depth [N] [--list] | index [--check] | check | done N | doctor

Stdlib only, Python 3.11+ (tomllib). A repository that teaches you something should not need a
package install before it can check itself.

The master plan is the single source of truth for *what the curriculum is*: tracks, phases and the
day map live there between `<!-- granth:...:start -->` markers, so a person reading the plan and
this script parsing it cannot disagree. granth.toml holds only what the plan cannot express.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

if sys.version_info < (3, 11):  # pragma: no cover
    sys.exit("granth: needs Python 3.11 or newer (tomllib is stdlib from 3.11).")

import tomllib

ROOT = Path(__file__).resolve().parent

# Day titles carry em dashes and non-Latin words, and a Windows console still defaults to a legacy
# code page. Line buffering keeps this script's own output in order with its subprocesses'.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", line_buffering=True)
        except (ValueError, OSError):  # pragma: no cover
            pass

# =============================================================================================
# Configuration
# =============================================================================================

# The eleven part sections. The order is the pedagogy — scene before definition, definition before
# mechanism, mechanism before failure, failure before production. Changing it is a plan amendment.
PART_SECTIONS = [
    "one-line answer",
    "the story",
    "the idea in plain language",
    "why this project needs it",
    "the source behind it",
    "the mechanism",
    "line by line",
    "the source in one demo",
    "when it breaks",
    "in production",
    "check yourself",
]
SECTION_PATTERNS = {
    "one-line answer": r"one[- ]line answer",
    "the story": r"the story",
    "the idea in plain language": r"idea in plain language",
    "why this project needs it": r"why .{0,40}needs? it",
    "the source behind it": r"the (source|paper|spec) behind it",
    "the mechanism": r"mechanism",
    "line by line": r"line by line",
    "the source in one demo": r"(source|paper|spec) in one demo",
    "when it breaks": r"when it breaks",
    "in production": r"in production",
    "check yourself": r"check yourself",
}
# "Line by line" is a bolded lead-in after each code block, not a heading in a fixed place, so it
# is excluded from the order comparison; unexplained_code_blocks() enforces it per fence instead.
ORDER_EXEMPT = {"line by line"}
CONDITIONAL = {"the source behind it", "line by line", "the source in one demo"}

HUB_SECTIONS = [
    "Where we are", "The map", "Setup", "Build brief",
    "The check that must be able to fail", "Budget", "Traps", "Verify before you build",
    "Say it out loud", "Done when", "Ledger & commit",
]
LEVELS = ["foundation", "working", "production"]
NO_WALKTHROUGH_LANGS = ["", "text", "console", "output", "traceback", "mermaid", "diff",
                        "json", "toml", "yaml", "ini", "csv"]
EXEMPT_HEADINGS = r"when it breaks|check yourself|verify|budget|ledger|the map|setup"

# A day is a unit of subject, not of time. A duration field silently authorises the worst edit in
# technical writing: cutting an explanation because the day is running long.
TIME_BANS = [
    (r"^\s*(reading_minutes|duration|time_estimate|minutes|est_time|estimated_hours"
     r"|estimated hours|effort|pace)\s*:", "a duration field in frontmatter"),
    (r"\b\d+\s*[-–]?\s*\d*\s*(minutes?|mins?|hours?|hrs?)\b(?!\s*(of |the |per ))",
     "a time estimate in the prose"),
    (r"\*\*(Time|Duration|Estimated hours):?\*\*", "a bolded time line"),
    (r"should take (about |around |roughly )?\w+", "a 'should take ...' pace"),
]

PART_KEYS = ["day", "part", "title", "ids", "level", "prerequisites", "prev", "next"]
# A source document has no `part` — it is not a subtopic of anything — and adds `source`.
SOURCE_KEYS = ["day", "source", "title", "ids", "level", "prerequisites", "prev", "next"]
HUB_KEYS = ["day", "phase", "title", "ids", "kind", "plan_version", "parts", "generated", "status"]

# A citation is an identifier, never a person: an identifier resolves to exactly one document and
# is what a reader types.
SOURCE_ID_RE = re.compile(
    r"arXiv:\d{4}\.\d{4,5}(?:v\d+)?"
    r"|arXiv:[a-z-]+(?:\.[A-Z]{2})?/\d{7}"
    r"|doi:10\.\d{4,9}/[^\s)\]|,;\"'`>*<]+"
    r"|RFC\s?\d{3,5}"
    r"|ISO[/ ]?(?:IEC[/ ]?)?\d{3,5}(?:-\d+)?(?::\d{4})?"
    r"|spec:[a-z0-9][a-z0-9.\-/]*", re.I)
# Only the two colon-prefixed forms: `spec:` and `iso:` collide with ordinary English, and these
# are the forms where a malformed identifier is both likely and silent.
SOURCE_ID_LOOSE_RE = re.compile(r"\b(?:arxiv|doi)\s*:\s*\S+", re.I)

PART_NAME_RE = re.compile(r"^(\d+)\.(\d+)-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
SECTION_DIR_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
SOURCE_NAME_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
DAY_DIR_RE = re.compile(r"^day-(\d{2,3})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
ANY_DAY_DIR_RE = re.compile(r"^day-(\d{2,3})(?:-([a-z0-9-]*))?$")
ID_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,7})-(\d{2,3})\b")


@dataclass
class Config:
    name: str = "Project"
    slug: str = "project"
    topic: str = "the subject"
    plan_version: str = "v1.0.0"
    driver: str = "python granth.py"
    plan: Path = field(default_factory=lambda: ROOT / "docs" / "00_MASTER_PLAN.md")
    docs: Path = field(default_factory=lambda: ROOT / "docs")
    days: Path = field(default_factory=lambda: ROOT / "days")
    sources_dir: str = "sources"
    parts_dir: str = "parts"
    levels: list[str] = field(default_factory=lambda: list(LEVELS))
    part_sections: list[str] = field(default_factory=lambda: list(PART_SECTIONS))
    section_patterns: dict[str, str] = field(default_factory=lambda: dict(SECTION_PATTERNS))
    hub_sections: list[str] = field(default_factory=lambda: list(HUB_SECTIONS))
    no_walkthrough_langs: list[str] = field(default_factory=lambda: list(NO_WALKTHROUGH_LANGS))
    exempt_headings: str = EXEMPT_HEADINGS
    require_failure_part: bool = True
    require_sources: bool = True
    lint: str = ""
    format_check: str = ""
    test: str = ""

    @property
    def sources_ledger(self) -> Path:
        return self.docs / "SOURCES.md"

    @property
    def progress(self) -> Path:
        return self.docs / "PROGRESS.md"

    def rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return path.as_posix()


def load_config() -> Config:
    """Read granth.toml. Every key is optional; the constants above are the standing contract."""
    cfg = Config()
    path = ROOT / "granth.toml"
    if not path.exists():
        return cfg
    with path.open("rb") as handle:
        raw = tomllib.load(handle)
    p, paths = raw.get("project", {}), raw.get("paths", {})
    c, t = raw.get("contract", {}), raw.get("toolchain", {})
    for key in ("name", "slug", "topic", "plan_version", "driver"):
        setattr(cfg, key, p.get(key, getattr(cfg, key)))
    for key, default in (("plan", "docs/00_MASTER_PLAN.md"), ("docs", "docs"), ("days", "days")):
        value = Path(paths.get(key, default))
        setattr(cfg, key, value if value.is_absolute() else ROOT / value)
    for key in ("sources_dir", "parts_dir", "levels", "part_sections", "hub_sections",
                "no_walkthrough_langs", "exempt_headings", "require_failure_part",
                "require_sources"):
        setattr(cfg, key, c.get(key, getattr(cfg, key)))
    cfg.section_patterns = {**cfg.section_patterns, **c.get("section_patterns", {})}
    for key in ("lint", "format_check", "test"):
        setattr(cfg, key, t.get(key, ""))
    return cfg


# =============================================================================================
# Reading the plan and the days
# =============================================================================================

def marked_block(text: str, marker: str) -> str:
    """Text between `<!-- granth:<marker>:start -->` and its `:end`.

    Markers rather than heading names: a heading can be reworded freely, a marker cannot be
    reworded by accident.
    """
    name = re.escape(marker)
    hit = re.search(rf"<!--\s*granth:{name}:start\s*-->(.*?)<!--\s*granth:{name}:end\s*-->",
                    text, re.S)
    return hit.group(1) if hit else ""


def _sep(cells: list[str]) -> bool:
    real = [c for c in cells if c.strip()]
    return bool(real) and all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in real)


def table_rows(block: str) -> list[list[str]]:
    """Data rows of every Markdown table in `block`. A header is the row a separator follows."""
    rows, lines = [], [ln.strip() for ln in block.splitlines()]
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if _sep(cells):
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if nxt.startswith("|") and _sep([c.strip() for c in nxt.strip("|").split("|")]):
            continue
        rows.append(cells)
    return rows


def ids_in(text: str) -> list[str]:
    seen: dict[str, None] = {}
    for m in ID_RE.finditer(text or ""):
        seen.setdefault(f"{m.group(1)}-{m.group(2)}", None)
    return list(seen)


@dataclass
class PlanDay:
    number: int
    title: str
    ids: list[str]


@dataclass
class Track:
    prefix: str
    name: str
    count: int | None


@dataclass
class Phase:
    number: str
    days: str
    theme: str
    gate: str
    first: int | None
    last: int | None


def read_plan(cfg: Config) -> str:
    if not cfg.plan.exists():
        sys.exit(f"granth: no plan at {cfg.rel(cfg.plan)} — run the initiate step first.")
    return cfg.plan.read_text(encoding="utf-8")


def plan_days(cfg: Config) -> dict[int, PlanDay]:
    block = marked_block(read_plan(cfg), "day-map")
    if not block:
        sys.exit("granth: the plan carries no <!-- granth:day-map:start --> block.\n"
                 "        Every day document is checked against it — add the markers and re-run.")
    days: dict[int, PlanDay] = {}
    for cells in table_rows(block):
        if len(cells) < 2 or not re.fullmatch(r"\d{1,3}", cells[0]):
            continue
        days[int(cells[0])] = PlanDay(int(cells[0]), cells[1],
                                      ids_in(cells[2]) if len(cells) > 2 else [])
    return days


def plan_tracks(cfg: Config) -> list[Track]:
    tracks = []
    for cells in table_rows(marked_block(read_plan(cfg), "tracks")):
        if len(cells) < 2:
            continue
        prefix = re.sub(r"[`*]", "", cells[1]).strip()
        if not re.fullmatch(r"[A-Z][A-Z0-9]{1,7}", prefix):
            continue
        count = int(cells[2]) if len(cells) > 2 and re.fullmatch(r"\d+", cells[2].strip()) else None
        tracks.append(Track(prefix, cells[0].strip("* "), count))
    return tracks


def plan_phases(cfg: Config) -> list[Phase]:
    phases = []
    for cells in table_rows(marked_block(read_plan(cfg), "phases")):
        if len(cells) < 2:
            continue
        span = re.sub(r"[`*]", "", cells[1]).strip()
        b = re.findall(r"\d+", span)
        phases.append(Phase(re.sub(r"[`*]", "", cells[0]).strip(), span,
                            cells[2] if len(cells) > 2 else "",
                            cells[3] if len(cells) > 3 else "",
                            int(b[0]) if b else None, int(b[-1]) if b else None))
    return phases


def phase_of(day: int, phases: list[Phase]) -> Phase | None:
    return next((p for p in phases
                 if p.first is not None and p.last is not None and p.first <= day <= p.last), None)


def day_dirs(cfg: Config) -> dict[int, Path]:
    """Every days/day-NN-<slug>/ keyed by number.

    The number is the identity and the slug a label on it, so a folder can be renamed to a better
    slug at any time without breaking a single tool.
    """
    found: dict[int, Path] = {}
    if cfg.days.exists():
        for entry in sorted(cfg.days.iterdir()):
            m = ANY_DAY_DIR_RE.match(entry.name) if entry.is_dir() else None
            if m:
                found[int(m.group(1))] = entry
    return found


def find_day(cfg: Config, number: int) -> Path | None:
    return day_dirs(cfg).get(number)


def part_files(folder: Path, cfg: Config) -> list[Path]:
    d = folder / cfg.parts_dir
    return sorted(d.rglob("*.md")) if d.is_dir() else []


def source_files(folder: Path, cfg: Config) -> list[Path]:
    d = folder / cfg.sources_dir
    return sorted(d.glob("*.md")) if d.is_dir() else []


def is_written(folder: Path, cfg: Config) -> bool:
    """A day is *written* only when it has a hub and a non-empty parts directory."""
    return (folder / "LESSON.md").exists() and bool(part_files(folder, cfg))


def frontmatter(text: str) -> dict[str, str] | None:
    """The leading `---` block as flat key to value. Not a YAML parser, and does not need to be."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    meta = {}
    for line in text[3:end].splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            key, sep, value = line.partition(":")
            if sep:
                meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def body(text: str) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    return text if end == -1 else text[end + 4:]


def progress_days(cfg: Config) -> list[int]:
    """Day numbers with a row in the progress ledger — the ledger is what 'complete' means."""
    if not cfg.progress.exists():
        return []
    done = []
    for line in cfg.progress.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("|"):
            first = s.strip("|").split("|")[0].strip()
            if re.fullmatch(r"\d{1,3}", first):
                done.append(int(first))
    return sorted(set(done))


# =============================================================================================
# The depth contract, checked by a machine
# =============================================================================================

@dataclass
class Report:
    day: int
    failures: list[str] = field(default_factory=list)
    parts: int = 0
    sources: int = 0

    def fail(self, where: str, message: str) -> None:
        self.failures.append(f"{where}: {message}")

    @property
    def ok(self) -> bool:
        return not self.failures


def source_ids(value: str) -> list[str]:
    return [h.group(0) for h in SOURCE_ID_RE.finditer(value or "")]


def malformed_source_ids(text: str) -> list[str]:
    """Citation-shaped strings no accepted form matches.

    Compares by start position rather than trimming punctuation: a real citation in prose is
    followed by a backtick or a bracket, and guessing what to strip is how this produces false
    failures.
    """
    valid = {h.start() for h in SOURCE_ID_RE.finditer(text)}
    return [h.group(0).strip() for h in SOURCE_ID_LOOSE_RE.finditer(text) if h.start() not in valid]


def ledger_ids(cfg: Config) -> frozenset[str]:
    if not cfg.sources_ledger.exists():
        return frozenset()
    text = cfg.sources_ledger.read_text(encoding="utf-8")
    return frozenset(m.group(0).lower() for m in SOURCE_ID_RE.finditer(text))


def sources_taught(cfg: Config) -> dict[str, list[str]]:
    """identifier -> documents declaring it. A source is taught once and cited thereafter."""
    taught: dict[str, list[str]] = {}
    for number, folder in day_dirs(cfg).items():
        for path in source_files(folder, cfg):
            meta = frontmatter(path.read_text(encoding="utf-8")) or {}
            for i in source_ids(meta.get("source", "")):
                taught.setdefault(i.lower(), []).append(f"day {number} {path.name}")
    return taught


def _fences(cfg: Config, text: str):
    """Yield (start, lang, heading, end) per fence.

    A fence may be longer than three backticks so it can contain a shorter one — which is how a
    lesson shows the contents of a Markdown file.
    """
    lines, heading, i = text.splitlines(), "", 0
    while i < len(lines):
        if lines[i].startswith("#"):
            heading, i = lines[i], i + 1
            continue
        fence = re.match(r"^(`{3,})([\w+-]*)\s*$", lines[i])
        if not fence:
            i += 1
            continue
        closing = re.compile(rf"^`{{{len(fence.group(1))},}}\s*$")
        start, i = i, i + 1
        while i < len(lines) and not closing.match(lines[i]):
            i += 1
        i += 1
        yield start, fence.group(2).lower(), heading, i


def _needs_walkthrough(cfg: Config, lang: str, heading: str) -> bool:
    return lang not in cfg.no_walkthrough_langs and not re.search(
        cfg.exempt_headings, heading, re.I)


def unexplained_code_blocks(cfg: Config, text: str) -> list[int]:
    """Fences no walkthrough follows. An unexplained line is a bug in the document: the reader
    can copy it but cannot change it."""
    lines, out = text.splitlines(), []
    for start, lang, heading, after in _fences(cfg, text):
        if not _needs_walkthrough(cfg, lang, heading):
            continue
        j, explained = after, False
        while j < len(lines):
            if re.search(r"line by line", lines[j], re.I):
                explained = True
                break
            if re.match(r"^`{3,}[\w+-]", lines[j]) or lines[j].startswith("## "):
                break
            j += 1
        if not explained:
            out.append(start + 1)
    return out


def has_explainable_code(cfg: Config, text: str) -> bool:
    return any(_needs_walkthrough(cfg, lg, h) for _, lg, h, _ in _fences(cfg, text))


def check_no_clocks(cfg: Config, text: str, where: str, report: Report) -> None:
    prose = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    for pattern, description in TIME_BANS:
        hit = re.search(pattern, prose, re.I | re.M)
        if hit:
            snippet = hit.group(0).strip().replace("\n", " ")
            report.fail(where, f"{description} ({snippet!r}) — a day carries no clock")


def section_regex(cfg: Config, name: str) -> re.Pattern[str]:
    pattern = cfg.section_patterns.get(name, re.escape(name))
    if name == "line by line":
        return re.compile(rf"^#{{2,4}}\s.*{pattern}|^\*\*Line by line:?\*\*", re.I | re.M)
    return re.compile(rf"^#{{2,4}}\s.*{pattern}", re.I | re.M)


def check_sections(cfg: Config, content: str, meta: dict[str, str], where: str,
                   report: Report, is_source: bool) -> None:
    """Required sections present, unconditional ones in the contract's order.

    Three are conditional — each required exactly when its trigger is present. No script can
    decide whether an idea has a citable origin, so the writer declares it and the script checks
    that the declaration and the section agree.
    """
    triggers = {
        "the source behind it": bool(source_ids(meta.get("sources", ""))),
        "line by line": has_explainable_code(cfg, content),
        "the source in one demo": is_source,
    }
    positions: list[tuple[int, str]] = []
    for name in cfg.part_sections:
        hit = section_regex(cfg, name).search(content)
        required = triggers.get(name, True)
        if hit is None:
            if required:
                report.fail(where, f"missing section '{name}'")
            continue
        if name == "the source behind it" and not required:
            report.fail(where, "carries 'the source behind it' but declares no 'sources' — the "
                               "section and the key are required exactly when the other is present")
        if name not in ORDER_EXEMPT:
            positions.append((hit.start(), name))
    found = {n for _, n in positions}
    ordered = [n for _, n in sorted(positions)]
    expected = [n for n in cfg.part_sections if n in found]
    if ordered != expected:
        report.fail(where, "sections are out of order — the sequence is the pedagogy. "
                           f"found {ordered}, expected {expected}")
    for token in malformed_source_ids(content):
        report.fail(where, f"{token!r} is citation-shaped but matches no accepted identifier form")


def check_citations(cfg: Config, meta: dict[str, str], where: str, report: Report) -> None:
    if not cfg.require_sources:
        return
    known = ledger_ids(cfg)
    for i in source_ids(meta.get("sources", "")) + source_ids(meta.get("source", "")):
        if i.lower() not in known:
            report.fail(where, f"{i} is not in {cfg.rel(cfg.sources_ledger)} — look the record up "
                               "live and add a dated row before citing it")


@dataclass
class PartResult:
    section: int
    subtopic: int
    declares_failure: bool = False


def check_part(cfg: Config, path: Path, day: int, report: Report) -> PartResult | None:
    where = cfg.rel(path)
    name = PART_NAME_RE.match(path.name)
    if not name:
        report.fail(where, "filename must be <section>.<subtopic>-<kebab-slug>.md")
        return None
    section, subtopic = int(name.group(1)), int(name.group(2))
    folder = SECTION_DIR_RE.match(path.parent.name)
    if not folder:
        report.fail(cfg.rel(path.parent),
                    "a section folder is NN-<kebab-slug> — a bare number is an address, "
                    "not an answer")
    elif int(folder.group(1)) != section:
        report.fail(where, f"sits in {path.parent.name} but its number says section {section}")

    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    if meta is None:
        report.fail(where, "no YAML frontmatter")
        return PartResult(section, subtopic)
    for key in PART_KEYS:
        if key not in meta:
            report.fail(where, f"frontmatter is missing '{key}'")
    if meta.get("level") and meta["level"] not in cfg.levels:
        report.fail(where, f"level {meta['level']!r} is not one of {cfg.levels}")
    if meta.get("day") and meta["day"].strip() != str(day):
        report.fail(where, f"frontmatter says day {meta['day']} but it sits in day {day}")

    content = body(text)
    check_sections(cfg, content, meta, where, report, is_source=False)
    check_citations(cfg, meta, where, report)
    check_no_clocks(cfg, text, where, report)
    for line in unexplained_code_blocks(cfg, content):
        report.fail(where, f"code block at line {line} has no 'Line by line' walkthrough after it")
    return PartResult(section, subtopic,
                      meta.get("failure", "").strip().lower() in {"true", "yes"})


def check_source(cfg: Config, path: Path, day: int, report: Report) -> int | None:
    where = cfg.rel(path)
    name = SOURCE_NAME_RE.match(path.name)
    if not name:
        report.fail(where, "a source document is NN-<kebab-slug>.md, numbered from 01")
        return None
    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    if meta is None:
        report.fail(where, "no YAML frontmatter")
        return int(name.group(1))
    for key in SOURCE_KEYS:
        if key not in meta:
            report.fail(where, f"frontmatter is missing '{key}'")
    if "part" in meta:
        report.fail(where, "a source document has no 'part' — it is not a subtopic of anything")
    declared = source_ids(meta.get("source", ""))
    if not declared:
        report.fail(where, "frontmatter 'source' must carry exactly one resolvable identifier")
    elif len(declared) > 1:
        report.fail(where, f"'source' declares {len(declared)} identifiers — one document, "
                           "one source")
    if meta.get("level") and meta["level"] not in cfg.levels:
        report.fail(where, f"level {meta['level']!r} is not one of {cfg.levels}")

    content = body(text)
    check_sections(cfg, content, meta, where, report, is_source=True)
    check_citations(cfg, meta, where, report)
    check_no_clocks(cfg, text, where, report)
    for line in unexplained_code_blocks(cfg, content):
        report.fail(where, f"code block at line {line} has no 'Line by line' walkthrough after it")
    return int(name.group(1))


def check_hub(cfg: Config, folder: Path, part_count: int, report: Report) -> None:
    hub = folder / "LESSON.md"
    where = cfg.rel(hub)
    if not hub.exists():
        report.fail(cfg.rel(folder), "no LESSON.md — the hub is what assembles the day")
        return
    text = hub.read_text(encoding="utf-8")
    meta = frontmatter(text)
    if meta is None:
        report.fail(where, "no YAML frontmatter")
        return
    for key in HUB_KEYS:
        if key not in meta:
            report.fail(where, f"frontmatter is missing '{key}'")
    if meta.get("plan_version") and meta["plan_version"] != cfg.plan_version:
        report.fail(where, f"plan_version {meta['plan_version']!r} but granth.toml says "
                           f"{cfg.plan_version!r}")
    if meta.get("parts", "").strip().isdigit() and int(meta["parts"]) != part_count:
        report.fail(where, f"frontmatter claims {meta['parts']} parts; {part_count} are on disk")

    content = body(text)
    if not re.search(r"^>\s", content, re.M):
        report.fail(where, "no yesterday / today / tomorrow blockquote")
    positions = []
    for index, title in enumerate(cfg.hub_sections, start=1):
        hit = re.search(rf"^#{{2,3}}\s*(?:§\s*)?{index}\b.*", content, re.M)
        if hit is None:
            report.fail(where, f"missing hub section {index} — {title}")
        else:
            positions.append((hit.start(), index))
    if [n for _, n in sorted(positions)] != [n for _, n in positions]:
        report.fail(where, "hub sections are out of order")
    # The hub orients and assembles; the parts teach.
    if re.search(r"\*\*Line by line:?\*\*", content, re.I):
        report.fail(where, "the hub carries a 'Line by line' walkthrough — teaching belongs "
                           "in a part")
    check_no_clocks(cfg, text, where, report)
    if not (folder / "CHECKLIST.md").exists():
        report.fail(cfg.rel(folder), "no CHECKLIST.md — a day has no definition of done without it")


def check_numbering(numbers: list[tuple[int, int]], where: str, report: Report) -> None:
    """Sections run 1..N with no gaps, and so do subtopics inside each.

    A gap means a document was deleted or never written, and nothing else in the repository would
    say so — the reader would simply never learn that 2.3 was meant to exist.
    """
    if not numbers:
        return
    sections = sorted({s for s, _ in numbers})
    if sections != list(range(1, len(sections) + 1)):
        report.fail(where, f"section numbers {sections} — they must run 1..N with no gaps")
    for section in sections:
        subs = sorted(sub for sec, sub in numbers if sec == section)
        if subs != list(range(1, len(subs) + 1)):
            report.fail(where, f"section {section} subtopics {subs} — must run 1..N with no gaps")


def check_day(cfg: Config, number: int) -> Report:
    report = Report(day=number)
    folder = find_day(cfg, number)
    if folder is None:
        report.fail(f"day {number}", f"no folder in {cfg.rel(cfg.days)}")
        return report
    where = cfg.rel(folder)
    if not DAY_DIR_RE.match(folder.name):
        report.fail(where, "a day folder is day-NN-<kebab-slug> — a number alone is "
                           "indistinguishable from every other day in a file tree or a git log")
    parts_dir = folder / cfg.parts_dir
    if not parts_dir.is_dir():
        report.fail(where, f"no {cfg.parts_dir}/ — a day without it is not written")
        return report
    for path in sorted(parts_dir.glob("*.md")):
        report.fail(cfg.rel(path),
                    f"loose in {cfg.parts_dir}/ — every part lives in its section folder")

    numbers, failure_declared = [], False
    for path in sorted(parts_dir.rglob("*.md")):
        if path.parent == parts_dir:
            continue
        result = check_part(cfg, path, number, report)
        if result:
            numbers.append((result.section, result.subtopic))
            failure_declared = failure_declared or result.declares_failure
    report.parts = len(numbers)
    check_numbering(numbers, where, report)
    if report.parts == 0:
        report.fail(where, f"{cfg.parts_dir}/ holds no part documents")

    source_numbers = []
    for path in source_files(folder, cfg):
        result = check_source(cfg, path, number, report)
        if result is not None:
            source_numbers.append(result)
    report.sources = len(source_numbers)
    if source_numbers and sorted(source_numbers) != list(range(1, len(source_numbers) + 1)):
        report.fail(where, f"source numbers {sorted(source_numbers)} — must run 01..NN, no gaps")

    if cfg.require_failure_part and not failure_declared:
        report.fail(where, "no part declares 'failure: true' — every day carries at least one "
                           "part whose subject is a deliberate failure")
    check_hub(cfg, folder, report.parts, report)

    plan, hub = plan_days(cfg), folder / "LESSON.md"
    if hub.exists() and number in plan:
        meta = frontmatter(hub.read_text(encoding="utf-8")) or {}
        claimed, assigned = set(ids_in(meta.get("ids", ""))), set(plan[number].ids)
        for extra in sorted(claimed - assigned):
            report.fail(cfg.rel(hub), f"claims {extra}, which the plan does not assign to this day")
        for missing in sorted(assigned - claimed):
            report.fail(cfg.rel(hub), f"the plan assigns {missing} to this day; the hub omits it")
    return report


def cmd_depth(cfg: Config, args: list[str]) -> int:
    if "--list" in args:
        print(f"granth depth contract for {cfg.name} ({cfg.plan_version})\n")
        print("A part document carries, in order:")
        for n in cfg.part_sections:
            print(f"  - {n}{' (conditional)' if n in CONDITIONAL else ''}")
        print("\nA hub carries, in order:")
        for i, t in enumerate(cfg.hub_sections, start=1):
            print(f"  {i:>2}. {t}")
        print(f"\nLevels: {', '.join(cfg.levels)}")
        print(f"Sources: {cfg.sources_dir}/   Parts: {cfg.parts_dir}/")
        return 0

    targets = [int(a) for a in args if a.isdigit()] or sorted(
        n for n, f in day_dirs(cfg).items() if is_written(f, cfg))
    if not targets:
        print("granth: no written days yet — nothing to check.")
        return 0
    reports = [check_day(cfg, n) for n in targets]
    # A source is taught once in the whole curriculum, so this check spans days.
    cross = [f"{i} is taught in {len(p)} places ({', '.join(p)}) — a source is taught once "
             "and cited thereafter" for i, p in sorted(sources_taught(cfg).items()) if len(p) > 1]

    failed = 0
    for r in reports:
        head = f"day {r.day:>2}  {r.parts} parts" + (f" + {r.sources} sources" if r.sources else "")
        if r.ok:
            print(f"OK    {head}")
        else:
            failed += 1
            print(f"FAIL  {head}")
            for line in r.failures:
                print(f"        {line}")
    if cross:
        print("FAIL  curriculum")
        for line in cross:
            print(f"        {line}")
    if failed or cross:
        print(f"\n{failed} of {len(reports)} day(s) fail the depth contract.")
        return 1
    print(f"\nOK all {len(reports)} day(s) meet the depth contract.")
    return 0


# =============================================================================================
# The generated indexes
# =============================================================================================

BANNER = "> **Do not edit this file by hand.** It is regenerated by `{d} index`."


def truncate(text: str, width: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= width else text[:width - 1].rstrip() + "…"


def one_line_answer(text: str) -> str:
    """The first paragraph under the one-line-answer heading, flattened.

    Reads the paragraph rather than the first line: day documents are hard-wrapped, so stopping at
    the newline cuts most answers mid-sentence.
    """
    hit = re.search(r"^#{2,4}\s.*one[- ]line answer.*$", text, re.I | re.M)
    if not hit:
        return ""
    out: list[str] = []
    for line in text[hit.end():].splitlines():
        s = line.strip().lstrip("> ").strip()
        if s.startswith("#") or s.startswith("```"):
            break
        if not s:
            if out:
                break
            continue
        out.append(s)
    return re.sub(r"\s+", " ", " ".join(out))


class DayFacts:
    def __init__(self, cfg: Config, number: int, folder: Path) -> None:
        self.number, self.folder = number, folder
        self.written = is_written(folder, cfg)
        self.hub = frontmatter((folder / "LESSON.md").read_text(encoding="utf-8")) or {}
        self.title = self.hub.get("title", "")
        self.ids = ids_in(self.hub.get("ids", ""))
        self.parts, self.sources = [], []
        for path in part_files(folder, cfg):
            if path.parent == folder / cfg.parts_dir:
                continue
            text = path.read_text(encoding="utf-8")
            meta = frontmatter(text) or {}
            self.parts.append({"part": meta.get("part", ""),
                               "title": meta.get("title", path.stem),
                               "level": meta.get("level", ""),
                               "answer": one_line_answer(body(text)),
                               "path": f"{cfg.parts_dir}/{path.parent.name}/{path.name}"})
        for path in source_files(folder, cfg):
            meta = frontmatter(path.read_text(encoding="utf-8")) or {}
            self.sources.append({"source": meta.get("source", ""),
                                 "title": meta.get("title", path.stem),
                                 "path": f"{cfg.sources_dir}/{path.name}"})

    @staticmethod
    def key(part: dict[str, str]) -> tuple[float, float]:
        bits = re.findall(r"\d+", part["part"])
        return (float(bits[0]) if bits else 0.0, float(bits[1]) if len(bits) > 1 else 0.0)


def day_link(cfg: Config, number: int, facts: dict[int, DayFacts]) -> str:
    """A link that still points somewhere sensible before the day exists."""
    name = facts[number].folder.name if number in facts else f"day-{number:02d}"
    return f"../days/{name}/LESSON.md"


def build_all(cfg: Config) -> dict[Path, str]:
    read_plan(cfg)
    plan, phases, tracks = plan_days(cfg), plan_phases(cfg), plan_tracks(cfg)
    complete = set(progress_days(cfg))
    facts = {n: DayFacts(cfg, n, f) for n, f in sorted(day_dirs(cfg).items())
             if (f / "LESSON.md").exists()}
    today, d = date.today().isoformat(), cfg.driver
    head = [f"_Generated {today} by `granth.py`._", BANNER.format(d=d), ""]

    # --- traceability -----------------------------------------------------------------------
    track_of = {t.prefix: t.name for t in tracks}
    rows, open_count = [], 0
    for number, day in sorted(plan.items()):
        ph = phase_of(number, phases)
        for i in day.ids:
            claimed = number in facts and i in facts[number].ids
            if number in complete and claimed:
                mark, status = "[x]", f"closed day {number}"
            elif claimed:
                mark, status, open_count = "[~]", f"written day {number}, not in the ledger", open_count + 1
            else:
                mark, status, open_count = "[ ]", "open", open_count + 1
            rows.append(f"| `{i}` | {track_of.get(i.split('-')[0], i.split('-')[0])} "
                        f"| {ph.number if ph else '-'} | {number} | {mark} {status} |")
    trace = "\n".join([f"# Traceability — {cfg.name}", "", *head,
        "An ID counts as **closed** only when its day has a row in `docs/PROGRESS.md` *and* its",
        "hub's frontmatter claims the ID. **An open ID from a completed phase is a bug**, not a",
        "backlog item.", "", f"**{len(rows) - open_count} of {len(rows)} closed.**", "",
        "| ID | Track | Phase | Planned day | Status |", "| --- | --- | --- | --- | --- |",
        *rows, ""])

    # --- curriculum index -------------------------------------------------------------------
    where = {i: (n, d_.title) for n, d_ in sorted(plan.items()) for i in d_.ids}
    lines = [f"# Curriculum index — {cfg.name}", "", *head,
             "The day map answers *what does day 43 teach?* This answers the reverse — *where do I",
             "learn `XX-14`?* Every ID appears exactly once; a duplicate or a missing ID is a plan",
             "bug.", ""]
    seen = set()
    for track in tracks:
        owned = sorted((i for i in where if i.startswith(f"{track.prefix}-")),
                       key=lambda i: int(i.split("-")[1]))
        seen.update(owned)
        lines += [f"## {track.name} (`{track.prefix}-`) — {len(owned) or 'no'} IDs", "",
                  "| ID | Day | Day title |", "| --- | --- | --- |"]
        lines += [f"| `{i}` | [{where[i][0]}]({day_link(cfg, where[i][0], facts)}) "
                  f"| {truncate(where[i][1], 96)} |" for i in owned]
        lines.append("")
        if track.count is not None and owned and len(owned) != track.count:
            lines += [f"> **Mismatch.** The plan's track table says {track.count} IDs; the day map "
                      f"assigns {len(owned)}. Fix the plan, then regenerate.", ""]
    if sorted(set(where) - seen):
        lines += ["## Unclaimed prefixes", "",
                  "Assigned in the day map, but the prefix has no row in the track table.", "",
                  "| ID | Day |", "| --- | --- |"]
        lines += [f"| `{i}` | {where[i][0]} |" for i in sorted(set(where) - seen)] + [""]
    index = "\n".join(lines)

    # --- tracker ----------------------------------------------------------------------------
    written = [n for n, f in facts.items() if f.written]
    total = len(plan)
    pct = lambda c: f"{(100 * c / total):.1f}%" if total else "-"  # noqa: E731
    lines = [f"# Tracker — {cfg.name}", "", *head,
             "A day is **written** with a hub and a non-empty parts directory, and **complete**",
             "only when it also has a ledger row. A thin day is visible from the parts column.", "",
             "| | Count | Of plan |", "| --- | --- | --- |",
             f"| Days in the plan | **{total}** | 100% |",
             f"| Days written | **{len(written)}** | {pct(len(written))} |",
             f"| Days complete | **{len(complete & set(plan))}** | {pct(len(complete & set(plan)))} |",
             f"| Subtopic documents | **{sum(len(f.parts) for f in facts.values())}** | — |",
             f"| Source documents | **{sum(len(f.sources) for f in facts.values())}** | — |", "",
             "## Every day", "", "| Day | Phase | Title | Status | Parts | Sources | IDs |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for number, day in sorted(plan.items()):
        f_, ph = facts.get(number), phase_of(number, phases)
        status = ("complete" if number in complete and f_ and f_.written
                  else "written" if f_ and f_.written else "hub only" if f_ else "not started")
        title = truncate(f_.title if f_ and f_.title else day.title, 72)
        cell = f"[{title}]({day_link(cfg, number, facts)})" if f_ else title
        lines.append(f"| {number} | {ph.number if ph else '-'} | {cell} | {status} "
                     f"| {len(f_.parts) if f_ else 0} | {len(f_.sources) if f_ else 0} "
                     f"| {', '.join(f'`{i}`' for i in day.ids) or '—'} |")
    lines += ["", "## Phases", "", "| Phase | Days | Theme | Written | Complete | Gate |",
              "| --- | --- | --- | --- | --- | --- |"]
    for ph in phases:
        if ph.first is None or ph.last is None:
            continue
        span = [n for n in plan if ph.first <= n <= ph.last]
        lines.append(f"| {ph.number} | {ph.days} | {truncate(ph.theme, 48)} "
                     f"| {len([n for n in span if n in facts and facts[n].written])}/{len(span)} "
                     f"| {len([n for n in span if n in complete])}/{len(span)} "
                     f"| {truncate(ph.gate, 56)} |")
    tracker = "\n".join(lines + [""])

    # --- wiki -------------------------------------------------------------------------------
    lines = [f"# {cfg.name} wiki — one row per day", "", *head,
             "For a day's parts open `wiki/day-NN.md`; open the day folder itself only to write",
             "it. Cross-day lookups live in `wiki/ENTITIES.md`.", "",
             "| Day | Subject | IDs closed | Parts | Sources |", "| --- | --- | --- | --- | --- |"]
    for number, f_ in sorted(facts.items()):
        srcs = ", ".join(s["source"] for s in f_.sources if s["source"]) or "—"
        lines.append(f"| [{number:02d}](wiki/day-{number:02d}.md) | {truncate(f_.title, 84)} "
                     f"| {', '.join(f_.ids) or '—'} | {len(f_.parts)} | {srcs} |")
    wiki = "\n".join(lines + [""])

    out = {cfg.docs / "TRACEABILITY.md": trace, cfg.docs / "CURRICULUM_INDEX.md": index,
           cfg.docs / "TRACKER.md": tracker, cfg.docs / "WIKI.md": wiki}

    # --- one page per day, plus the entity index ---------------------------------------------
    for number, f_ in facts.items():
        rel = f"../../days/{f_.folder.name}"
        lines = [f"# Day {number:02d} — {f_.title}", "", *head,
                 f"Hub: [`LESSON.md`]({rel}/LESSON.md) — IDs closed: {', '.join(f_.ids) or 'none'}",
                 "", "| Part | Title | Level | One-line answer |", "| --- | --- | --- | --- |"]
        for p in sorted(f_.parts, key=DayFacts.key):
            lines.append(f"| {p['part']} | [{truncate(p['title'], 60)}]({rel}/{p['path']}) "
                         f"| {p['level']} | {truncate(p['answer'], 120)} |")
        if f_.sources:
            lines += ["", "## Sources taught on this day", "", "| Identifier | Document |",
                      "| --- | --- |"]
            lines += [f"| {s['source']} | [{truncate(s['title'], 72)}]({rel}/{s['path']}) |"
                      for s in f_.sources]
        out[cfg.docs / "wiki" / f"day-{number:02d}.md"] = "\n".join(lines + [""])

    lines = [f"# Entities — {cfg.name}", "", *head,
             "The answer to *which day taught X?* and *is this source already taught?* — the two",
             "questions a long curriculum makes expensive to answer by reading.", "",
             "## Sources", "", "| Identifier | Taught on | Document |", "| --- | --- | --- |"]
    srows = sorted((s["source"], n, s["title"]) for n, f_ in facts.items()
                   for s in f_.sources if s["source"])
    lines += ([f"| {i} | [day {n}](day-{n:02d}.md) | {truncate(t, 72)} |" for i, n, t in srows]
              or ["| — | — | no source documents yet |"])
    lines += ["", "## Curriculum IDs", "", "| ID | Closed on |", "| --- | --- |"]
    irows = sorted(((i, n) for n, f_ in facts.items() for i in f_.ids),
                   key=lambda r: (r[0].split("-")[0], int(r[0].split("-")[1])))
    lines += ([f"| `{i}` | [day {n}](day-{n:02d}.md) |" for i, n in irows]
              or ["| — | no IDs claimed yet |"])
    out[cfg.docs / "wiki" / "ENTITIES.md"] = "\n".join(lines + [""])
    return out


def cmd_index(cfg: Config, args: list[str]) -> int:
    docs = build_all(cfg)
    if "--check" in args:
        stale = [cfg.rel(p) for p, t in docs.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != t]
        if stale:
            print("granth: these generated documents are stale —")
            for name in stale:
                print(f"        {name}")
            print(f"        run `{cfg.driver} index`.")
            return 1
        print(f"OK {len(docs)} generated document(s) are current.")
        return 0
    for path, text in docs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    print(f"OK wrote {len(docs)} generated document(s) under {cfg.rel(cfg.docs)}/.")
    return 0


# =============================================================================================
# The day brief, and the order guard
# =============================================================================================

def cmd_brief(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "brief")
    plan, phases = plan_days(cfg), plan_phases(cfg)
    complete, on_disk = progress_days(cfg), day_dirs(cfg)
    out: list[str] = [f"# {cfg.name} — brief for day {day}", ""]
    status = 0

    if day not in plan:
        first, last = (min(plan), max(plan)) if plan else (0, 0)
        print("\n".join(out + [f"**STOP.** The plan has no day {day}. It runs {first} to {last}.",
              "Adding, merging or reordering a day is a plan amendment: write the ADR first."]))
        return 1
    entry, ph = plan[day], phase_of(day, phases)

    expected = (max(complete) + 1) if complete else min(plan)
    if day != expected:
        status = 1
        if day in complete:
            out += [f"**STOP.** Day {day} already has a row in the progress ledger.",
                    f"The next unwritten day is **{expected}**."]
        elif day < expected:
            out.append(f"**STOP.** Day {day} is behind the ledger. The next day is **{expected}**.")
        else:
            missing = ", ".join(str(n) for n in range(expected, day) if n not in complete)
            out += [f"**STOP.** Day {day} is out of order — day **{expected}** is next.", "",
                    f"Not yet in the ledger: {missing}.",
                    "Never skip a day, merge two days, or reorder days without an ADR."]
        out += ["", "---", ""]

    out += ["## The assignment", "", f"**Title (from the plan):** {entry.title}", ""]
    out.append(f"**Close exactly these IDs — no more, no fewer:** {', '.join(entry.ids)}"
               if entry.ids else
               "**Closes no IDs.** State why in the hub, so traceability stays honest.")
    out.append("")
    if ph:
        out += [f"**Phase {ph.number} — {ph.theme}**", "", f"- Days in the phase: {ph.days}",
                f"- The gate this day feeds: {ph.gate}", ""]

    claimed: set[str] = set()
    for number, folder in on_disk.items():
        hub = folder / "LESSON.md"
        if number in complete and hub.exists():
            claimed |= set(ids_in((frontmatter(hub.read_text(encoding="utf-8")) or {}).get("ids", "")))
    debt = [(n, i) for n, p in sorted(plan.items()) if n < day for i in p.ids if i not in claimed]
    if debt:
        out += ["## Open IDs from earlier days", "",
                "An open ID from a day already behind you is a bug, not a backlog item.", ""]
        out += [f"- `{i}` was assigned to day {n} and is not closed." for n, i in debt] + [""]

    previous = max((n for n in plan if n < day), default=None)
    if previous is not None:
        folder = find_day(cfg, previous)
        out += [f"## Where day {previous} left off", ""]
        if folder is None:
            out.append(f"No folder for day {previous} — it was never written.")
        else:
            hub = folder / "LESSON.md"
            meta = frontmatter(hub.read_text(encoding="utf-8")) if hub.exists() else None
            if meta:
                out += [f"- Hub: `{cfg.rel(hub)}`", f"- Title: {meta.get('title', '?')}",
                        f"- Status: {meta.get('status', '?')}"]
            checklist = folder / "CHECKLIST.md"
            boxes = ([ln.strip() for ln in checklist.read_text(encoding="utf-8").splitlines()
                      if ln.strip().startswith("- [ ]")] if checklist.exists() else [])
            if boxes:
                out.append(f"- **{len(boxes)} unticked checklist box(es)** — ask before moving on:")
                out += [f"    {b}" for b in boxes[:8]]
                if len(boxes) > 8:
                    out.append(f"    ... and {len(boxes) - 8} more")
            elif checklist.exists():
                out.append("- Checklist: fully ticked.")
            if is_written(folder, cfg):
                out.append(f"- Read its parts before writing day {day}; build on them, never "
                           "repeat them.")
        out.append("")

    taught = sorted((meta["source"], n, meta.get("title", p.stem))
                    for n, f_ in sorted(on_disk.items()) for p in source_files(f_, cfg)
                    if (meta := frontmatter(p.read_text(encoding="utf-8")) or {}).get("source"))
    if taught:
        out += ["## Sources already taught (cite and link these — never teach one twice)", "",
                "| Identifier | Day | Document |", "| --- | --- | --- |"]
        out += [f"| {i} | {n} | {t} |" for i, n, t in taught] + [""]

    out += ["## Before you write a line", "",
            f"1. `{cfg.rel(cfg.plan)}` — the depth contract section, in full. It is the standard.",
            "2. The style guide section of the same plan — the register and the story rules.",
            f"3. `{cfg.rel(cfg.docs / 'GLOSSARY.md')}` — so a term defined on day 3 is defined the "
            "same way today.",
            "4. Verify every fact live. A version, an interface, a citation: look it up today, or",
            "   leave a TODO carrying the exact lookup command. Never a remembered answer.", ""]
    if status == 0:
        out.append(f"**Day {day} is next. Go.**")
    print("\n".join(out))
    return status


# =============================================================================================
# The rest of the driver
# =============================================================================================

def need_day(cfg: Config, args: list[str], command: str) -> int:
    if not args or not re.fullmatch(r"\d{1,3}", args[0]):
        sys.exit(f"usage: {cfg.driver} {command} <day-number>")
    return int(args[0])


def slugify(text: str) -> str:
    """A 1-4 word kebab-case label from the plan's title.

    Titles read `<subject> — <the elaboration>`, so the slug comes from the head phrase: truncating
    the whole title at four words lands mid-clause.
    """
    head = re.split(r"\s+[-–—:]\s+", text.strip(), maxsplit=1)[0]
    words = re.sub(r"[^a-z0-9]+", " ", head.lower()).split()
    dropped = {"a", "an", "the", "and", "of", "to", "in", "for", "with", "on", "by", "its"}
    return "-".join(([w for w in words if w not in dropped] or words)[:4]) or "day"


def cmd_status(cfg: Config, args: list[str]) -> int:
    plan = plan_days(cfg)
    written = [n for n, f in day_dirs(cfg).items() if is_written(f, cfg)]
    complete = [n for n in progress_days(cfg) if n in plan]
    nxt = (max(complete) + 1) if complete else (min(plan) if plan else 0)
    print(f"{cfg.name} ({cfg.plan_version}): {len(complete)}/{len(plan)} days complete, "
          f"{len(written)} written. Next: day {nxt}.")
    return 0


def cmd_start(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "start")
    folder = find_day(cfg, day)
    if folder is None:
        print(f"no day {day} on disk yet — `{cfg.driver} brief {day}` says what it must cover.")
        return 1
    if not is_written(folder, cfg):
        print(f"day {day} has a folder but no parts — it is not written.")
        return 1
    print(f"-> open {cfg.rel(folder / 'LESSON.md')}   (read its map, then the parts in order)")
    for path in part_files(folder, cfg):
        print(f"     {path.relative_to(folder).as_posix()}")
    for path in source_files(folder, cfg):
        print(f"     {path.relative_to(folder).as_posix()}   (read after the parts)")
    return 0


def cmd_parts(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "parts")
    folder = find_day(cfg, day)
    if folder is None or not (folder / cfg.parts_dir).is_dir():
        print(f"day {day} has no {cfg.parts_dir}/ — it is not written.")
        return 1
    for path in part_files(folder, cfg):
        print(path.relative_to(folder / cfg.parts_dir).as_posix())
    return 0


def cmd_new(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "new")
    plan = plan_days(cfg)
    if day not in plan:
        print(f"the plan has no day {day} — amend the plan first.")
        return 1
    if find_day(cfg, day):
        print(f"day {day} already exists at {cfg.rel(find_day(cfg, day))}.")
        return 1
    templates = cfg.days / "_TEMPLATES"
    if not templates.is_dir():
        print(f"no templates at {cfg.rel(templates)} — nothing to scaffold from.")
        return 1
    slug = slugify(args[1]) if len(args) > 1 else slugify(plan[day].title)
    folder = cfg.days / f"day-{day:02d}-{slug}"
    (folder / cfg.parts_dir / "01-rename-me").mkdir(parents=True, exist_ok=True)
    (folder / "lab").mkdir(exist_ok=True)
    for name in ("LESSON.md", "CHECKLIST.md"):
        if (templates / name).exists():
            shutil.copy(templates / name, folder / name)
    if (templates / "PART.md").exists():
        shutil.copy(templates / "PART.md",
                    folder / cfg.parts_dir / "01-rename-me" / "1.1-rename-me.md")
    print(f"-> {cfg.rel(folder)}")
    print(f"   the plan assigns: {plan[day].title}")
    print(f"   IDs to close: {', '.join(plan[day].ids) or 'none'}")
    print("   rename the section folder and the part file to say what they teach, then write.")
    return 0


def cmd_check(cfg: Config, args: list[str]) -> int:
    for command, label in ((cfg.lint, "lint"), (cfg.format_check, "format"), (cfg.test, "tests")):
        if command:
            print(f"--- {label}: {command}", flush=True)
            if subprocess.call(command, shell=True, cwd=ROOT) != 0:
                print(f"FAIL {label}")
                return 1
    print("--- depth contract", flush=True)
    if cmd_depth(cfg, []) != 0:
        return 1
    print("--- generated documents", flush=True)
    if cmd_index(cfg, ["--check"]) != 0:
        return 1
    print("\nOK all green")
    return 0


def cmd_done(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "done")
    folder = find_day(cfg, day)
    if folder is None:
        print(f"no folder for day {day}.")
        return 1
    checklist = folder / "CHECKLIST.md"
    if not checklist.exists():
        print(f"FAIL no {cfg.rel(checklist)} — a day has no definition of done without it.")
        return 1
    boxes = [ln for ln in checklist.read_text(encoding="utf-8").splitlines()
             if ln.strip().startswith("- [ ]")]
    if boxes:
        print(f"FAIL {len(boxes)} unticked box(es) in {cfg.rel(checklist)}:")
        for line in boxes:
            print(f"      {line.strip()}")
        return 1
    if day not in progress_days(cfg):
        print(f"FAIL day {day} has no row in {cfg.rel(cfg.progress)}.")
        print("      Paste the row from the hub's ledger section first — the ledger is the record,")
        print("      and a commit is not one.")
        return 1
    # Regenerate BEFORE checking: the ledger row this command just insisted on is itself an input
    # to the indexes, so checking first would fail on a staleness the day created.
    if cmd_index(cfg, []) != 0 or cmd_check(cfg, []) != 0:
        return 1
    meta = frontmatter((folder / "LESSON.md").read_text(encoding="utf-8")) or {}
    ids = ids_in(meta.get("ids", ""))
    message = f"day {day:02d}: {meta.get('title', folder.name)}"
    if ids:
        message += f" — closes {', '.join(ids)}"
    if subprocess.call(["git", "add", "-A"], cwd=ROOT) != 0:
        return 1
    if subprocess.call(["git", "commit", "-m", message], cwd=ROOT) != 0:
        return 1
    print(f"OK day {day} committed.")
    return 0


def cmd_doctor(cfg: Config, args: list[str]) -> int:
    """The repository's own wiring, checked before blaming a day for a tool's failure."""
    problems = []
    if not (ROOT / "granth.toml").exists():
        problems.append("no granth.toml at the repository root")
    if not cfg.plan.exists():
        problems.append(f"no plan at {cfg.rel(cfg.plan)}")
    else:
        text = cfg.plan.read_text(encoding="utf-8")
        problems += [f"the plan has no <!-- granth:{m}:start --> block"
                     for m in ("tracks", "phases", "day-map") if not marked_block(text, m)]
    problems += [f"no {cfg.rel(cfg.docs / n)}" for n in
                 ("PROGRESS.md", "CHANGELOG_PLAN.md", "GLOSSARY.md", "SOURCES.md")
                 if not (cfg.docs / n).exists()]
    if not (cfg.docs / "adr").is_dir():
        problems.append(f"no {cfg.rel(cfg.docs / 'adr')}/")
    if not cfg.days.is_dir():
        problems.append(f"no {cfg.rel(cfg.days)}/")
    if not (ROOT / ".gitignore").exists():
        problems.append("no .gitignore — secrets discipline starts with the file that enforces it")

    plan = plan_days(cfg) if cfg.plan.exists() else {}
    seen: dict[str, int] = {}
    for number, day in plan.items():
        for i in day.ids:
            if i in seen:
                problems.append(f"{i} is assigned to both day {seen[i]} and day {number}")
            seen[i] = number
    if problems:
        print("granth doctor found:")
        for line in problems:
            print(f"  - {line}")
        return 1
    print(f"OK {cfg.name}: config, plan markers, ledgers and day map all present.")
    print(f"   {len(plan)} days planned, {len(seen)} IDs assigned, each to exactly one day.")
    return 0


COMMANDS = {"status": cmd_status, "brief": cmd_brief, "start": cmd_start, "parts": cmd_parts,
            "new": cmd_new, "depth": cmd_depth, "index": cmd_index, "check": cmd_check,
            "done": cmd_done, "doctor": cmd_doctor}

USAGE = """usage: {d} <command> [args]

  status          how many days are written, how many complete, what is next
  brief N         what day N must close, its gate, and whether N is allowed yet
  start N         point at day N's hub and list its documents in reading order
  parts N         list day N's subtopic documents
  new N [slug]    scaffold an empty day folder from days/_TEMPLATES/
  depth [N]       check day N (or every written day) against the depth contract
  depth --list    print the contract as configured
  index [--check] regenerate the derived documents in docs/ (or fail if stale)
  check           lint + format + tests + depth contract + generated documents
  done N          refuse unless the checklist is ticked and the ledger row exists, then commit
  doctor          this repository's own wiring: config, plan markers, ledgers, day map
"""


def main(argv: list[str]) -> int:
    cfg = load_config()
    command = argv[0] if argv else "help"
    handler = COMMANDS.get(command)
    if handler is None:
        print(USAGE.format(d=cfg.driver))
        return 0 if command in {"help", "-h", "--help"} else 2
    return handler(cfg, argv[1:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
````

### `docs/00_MASTER_PLAN.md`

The contract. Expand the three marked blocks to one row per track, per phase and **per day**; §11 and §12 are copied as they stand.

````markdown
---
plan: {{PROJECT_SLUG}}
version: "{{PLAN_VERSION}}"
topic: "{{TOPIC}}"
tracks: {{TRACK_COUNT}}
ids: {{ID_TOTAL}}
days: {{TOTAL_DAYS}}
phases: {{PHASE_COUNT}}
doc_architecture: "hub + parts/ (see §11)"
amended: "{{DATE}}"
---

# MASTER PLAN {{PLAN_VERSION}} — {{PROJECT_NAME}}

## {{TOPIC}}

> **{{PROJECT_NAME}}** — {{NAME_MEANING}}
>
> **Purpose: this is the single source of truth.** Every other document in this repository points
> back here. When a day document and this plan disagree, this plan is right and the day is a bug.
> When *reality* and this plan disagree, the plan is amended first (Principle 8) — never patched
> around in silence.

---

## Table of contents

| § | Section |
| --- | --- |
| 1 | The vision — what exists at the end |
| 2 | Core principles — the rules that are never broken |
| 3 | The artifact — what actually gets built |
| 4 | Constraints & budget |
| 5 | The baseline — what this plan is pinned to, and how it is verified |
| 6 | The tracks and the ID scheme |
| 7 | The phases |
| 8 | The day map — day to IDs closed |
| 9 | Phase gates and the freshness check |
| 10 | Ledgers and traceability |
| **11** | **The depth contract — how a day is written** |
| 12 | The style guide |
| 13 | Amendment record |

---

## 1 · The vision — what exists at the end

By day {{LAST_DAY}} you will have **{{END_STATE}}**, and you will be able to defend every decision
inside it.

The measure is not how many days were finished. It is whether, handed the finished thing and a
sceptical reviewer, you can explain each part, say what it costs, name what breaks it, and show
the check that catches the breakage.

Three things this plan is trying to prevent:

1. **The tutorial ceiling.** Following steps produces something that runs and understanding that
   evaporates the moment the inputs change. Every subtopic here therefore ends at the real-system
   version, not the toy one (Principle 10).
2. **The forgotten middle.** In a curriculum this long, day 3 is forgotten by day 66. Every term
   is defined on first use, *including terms from earlier days, with a link back*, and the
   glossary is a ledger rather than an afterthought.
3. **The unverifiable claim.** Notes written from memory rot silently. Every version, interface
   and citation is looked up on the day it is used, and the document names what was checked
   (Principle 6).

### 1.1 Stated non-goals

These are decisions, not blind spots. Writing them down stops each of them being re-litigated on
a day when the real subject is something else.

- {{NON_GOAL_1}}
- {{NON_GOAL_2}}
- {{NON_GOAL_3}}

---

## 2 · Core principles — the rules that are never broken

<!-- granth:principles:start -->

1. **Doc-first.** The day document is written before the work; the work follows the document. A
   thing built first and explained afterwards gets explained in the shape it happened to take,
   which is not the same as the shape it should have.
2. **One day, one commit.** Append-only, traceable history. The repository is the memory.
3. **Build first, compare after.** Hand-roll the mechanism once, then adopt the tool that does it
   for you — so the tool is a convenience and never a mystery. A tool adopted before the
   mechanism is understood becomes a thing you cannot debug.
4. **Every concept is load-bearing.** If removing it would not change the artifact, it does not
   get a day. Coverage is not the goal; a working understanding is.
5. **Depth over density.** A day is a hub plus one document per subtopic, never one long page. If
   a subtopic cannot be read on its own, understood without scrolling past a different subtopic,
   and explained back out loud, it has not been split finely enough. A wall of text is not depth —
   it is depth's disguise. The full contract is §11.
6. **Never invent a fact.** A version, an interface, a limit, a citation: look it up **live on the
   day it is used**, or leave a `TODO` containing **the exact lookup command**. The document names
   what was checked and when. A guess that happens to be right is still a guess, and the next
   reader cannot tell which kind they are holding.
7. **Fail honestly.** Errors surface, escalate and are logged. Nothing fabricates a result to
   cover an error — and this applies to the writer as much as to anything that is built. An
   unrun command's output is a `TODO`, never a plausible transcript.
8. **If reality changes, the plan is amended first.** A moved specification, a renamed interface,
   a changed limit: amend via `docs/CHANGELOG_PLAN.md` and, for anything structural, an ADR —
   *then* continue. Days are never silently patched. Stop and say so.
9. **Every day ends with a check that can go RED.** A check that cannot fail has verified nothing.
   At least one per day, and at least one day per phase whose subject is a deliberate failure.
10. **Assume no prior knowledge, finish at production.** Every subtopic opens where a reader who
    has never met the idea can stand, defines its jargon on first use — including jargon from
    earlier days, with a link back — and does not stop at the toy example. It ends with how the
    idea is used in a real system: what a professional does instead of the teaching version, what
    breaks at scale or under pressure, the review comment, the interview question. Strong basics
    and advanced technique are the same document, in that order.
11. **A day is a unit of subject, not a unit of time.** No document carries a time estimate, a
    duration, an "estimated hours" field or a suggested pace — not in frontmatter, not in prose,
    not in a checklist. A topic is finished when it is understood, in one sitting or in five.
    **Nothing is ever trimmed to fit a clock**; a day that runs long gets another part, not a
    shorter explanation.
12. **Blast radius before capability.** Every new power arrives together with its containment
    story: what it can reach, what stops it, and what the blast looks like when the stop fails.
{{EXTRA_PRINCIPLES}}

<!-- granth:principles:end -->

> Principles 5, 10 and 11 are made concrete by **§11, the depth contract**, and are enforced
> mechanically by `granth.py` (`{{DRIVER}} depth N`) — and, for everything a script
> cannot judge, by reading.

---

## 3 · The artifact — what actually gets built

{{ARTIFACT_DESCRIPTION}}

The artifact is what makes Principle 4 checkable. "Is this concept load-bearing?" has a mechanical
answer: delete it and see whether the artifact still works. Nothing here is learned in the
abstract and hoped to be useful later.

---

## 4 · Constraints & budget

{{CONSTRAINTS}}

A constraint written down is a curriculum. A constraint discovered on day 40 is a rewrite.

---

## 5 · The baseline — what this plan is pinned to, and how it is verified

| What | Pinned to | Verified how | Re-checked |
| --- | --- | --- | --- |
| {{BASELINE_ROW_1}} |
| {{BASELINE_ROW_2}} |

**The verification rule (Principle 6), in three faces:**

- **Versions.** Read the version live before pinning it. Record package, version, the date it was
  observed, the day that added it and why, in `docs/PINS.md`. A failed lookup leaves
  `TODO(<the exact command>)`, never a guess.
- **Interfaces.** Every symbol, flag, endpoint or field a day uses is checked against the official
  documentation **on the day it is used**, and the document names the page checked. If the live
  documentation disagrees with this plan, **stop and propose an amendment** — do not adapt
  silently.
- **Citations.** Every source a day teaches or cites is opened live and its title copied from the
  record, never from memory, with a dated row in `docs/SOURCES.md`. This is the strictest of the
  three, because it fails the most quietly: a wrong version pin breaks the next install, while a
  plausible identifier attached to the wrong title survives for years. **Cite by title and
  identifier, never by author** (§12.5).

---

## 6 · The tracks and the ID scheme

Every concept in this plan has an ID. A day **closes** an ID when the concept is built into the
artifact — or demonstrably exercised against it — and the day's gates are green.
`docs/TRACEABILITY.md` is regenerated from the day hubs; **an open ID from a completed phase is a
bug**, not a backlog item.

<!-- granth:tracks:start -->

| Track | Prefix | Count | What runs through it |
| --- | --- | --- | --- |
| {{TRACK_1_NAME}} | `{{TRACK_1_PREFIX}}` | {{TRACK_1_COUNT}} | {{TRACK_1_THREAD}} |
| {{TRACK_2_NAME}} | `{{TRACK_2_PREFIX}}` | {{TRACK_2_COUNT}} | {{TRACK_2_THREAD}} |

<!-- granth:tracks:end -->

**Total: {{ID_TOTAL}} concept IDs.**

> Some IDs are **parked** — awareness-level, deliberately not built. You learn the map, you do not
> build the thing. A parked ID is marked in its day document and still closes normally. Parking is
> a decision recorded in the open, which is the opposite of a gap.

The authoritative statement of what an ID *means* is the row that assigns it in §8. This section
gives the shape; §8 gives the contract.

---

## 7 · The phases

A phase is a run of days that share one theme and end at one gate. The gate is the point: it is
where the work stops being a set of documents and has to behave.

<!-- granth:phases:start -->

| Phase | Days | Theme | The gate |
| --- | --- | --- | --- |
| {{PHASE_0_NUM}} | {{PHASE_0_DAYS}} | {{PHASE_0_THEME}} | {{PHASE_0_GATE}} |
| {{PHASE_1_NUM}} | {{PHASE_1_DAYS}} | {{PHASE_1_THEME}} | {{PHASE_1_GATE}} |

<!-- granth:phases:end -->

Every phase gate also includes the freshness check (§9).

---

## 8 · The day map — day to IDs closed

> **The authoritative day-to-ID assignment.** A day document closes **exactly** these IDs — no
> more, no fewer. A day that wants to close a different ID is asking for a plan amendment, and the
> amendment is written before the day is.
>
> The table below is read by `granth.py` as well as by people, which is why it sits between
> markers. Keep the three columns and keep one row per day; everything else about it is free.

<!-- granth:day-map:start -->

### Phase {{PHASE_0_NUM}} — {{PHASE_0_THEME}} (days {{PHASE_0_DAYS}})

| Day | Title | IDs closed |
| --- | --- | --- |
| {{DAY_0_NUM}} | {{DAY_0_TITLE}} | {{DAY_0_IDS}} |

### Phase {{PHASE_1_NUM}} — {{PHASE_1_THEME}} (days {{PHASE_1_DAYS}})

| Day | Title | IDs closed |
| --- | --- | --- |
| {{DAY_1_NUM}} | {{DAY_1_TITLE}} | {{DAY_1_IDS}} |

<!-- granth:day-map:end -->

---

## 9 · Phase gates and the freshness check

A phase is **green** only when all six hold:

1. Every day in the phase has its row in `docs/PROGRESS.md`, with gates green.
2. `docs/TRACEABILITY.md` shows **no open IDs** from this or any earlier phase.
3. `{{DRIVER}} check` passes on the whole repository — the local toolchain, the depth contract for
   every written day, and the generated documents being current.
4. Every day in the phase has a `parts/` directory. A day with no `parts/` is not written (§11.2),
   so a phase containing one cannot be green.
5. The **freshness check** passes:
   - {{FRESHNESS_1}}
   - {{FRESHNESS_2}}
   - Anything this plan pinned in §5 is re-read at its source. Moved? Amend first (Principle 8).
6. Every deviation is recorded: an ADR for anything structural, `docs/CHANGELOG_PLAN.md` for plan
   text. A deviation that is written down is a decision; one that is not is a defect.

**Never** skip a day, merge two days, or reorder days without an ADR.

> A gate is never passed because time ran out (Principle 11). `{{DRIVER}} done N` is gated on a
> ticked checklist, a ledger row and green checks, and on nothing else.

---

## 10 · Ledgers and traceability

All ledgers live in `docs/`.

| File | Nature | The rule |
| --- | --- | --- |
| `docs/PROGRESS.md` | append-only | One row per completed day. **The last row is where we actually are.** |
| `docs/PINS.md` | append-only | Every version, tool or limit this project depends on: what, which value, the date observed, the day that added it, why. No invented values (Principle 6). |
| `docs/SOURCES.md` | append-only | Every source a document teaches or cites: exact title, identifier, year, URL, the date the record was checked, and which documents cite it. |
| `docs/GLOSSARY.md` | append-only | Every term, defined once, with the part that introduced it. This is what stops day 66 redefining a day 3 word slightly differently. |
| `docs/PROVENANCE.md` | append-only | Every third-party thing this project runs or vendors: source, licence, version, who audited it and when, and what it is permitted to touch — recorded **before** it first runs (Principle 12). |
| `docs/CHANGELOG_PLAN.md` | append-only | Every amendment to this plan (Principle 8). Newest last. |
| `docs/adr/` | append-only | One file per structural decision, numbered, never rewritten. Superseded, not deleted. |
| `docs/TRACEABILITY.md` | **generated** | Every ID, its planned day, whether it is closed. |
| `docs/CURRICULUM_INDEX.md` | **generated** | The reverse lookup: where do I learn `XX-14`? |
| `docs/TRACKER.md` | **generated** | What is written, how thick each day is, what is pending. |
| `docs/WIKI.md` + `docs/wiki/` | **generated** | One row per day, one page per day, plus the entity index. |

**Four are written by hand and five are generated — do not confuse them.** Editing a generated
file only means the next `{{DRIVER}} index` silently overwrites you. The generated files are an
index *over* the days; every line in them is copied from a day document, and nothing in them is
written by a model. **If an index ever disagrees with the day it indexes, the day is right and the
index is stale** — regenerate it.

The append-only ledgers are written by the day you are finishing. Every hub ends with the exact
rows to paste (§11.5, section 11).

---

## 11 · The depth contract — how a day is written

> **Read this section in full before writing a single line of any day.** It carries the judgement
> no checker can make for you: the one-idea test, the standalone test, and whether a story is one
> the reader has plausibly lived.

### 11.1 The three commitments

Everything below follows from three sentences.

**One idea per document.** A subtopic that cannot be read alone, understood without scrolling past
a different subtopic, and explained back out loud is not one subtopic — it is several, badly
stacked. If a document needs the word "also" to introduce its second half, it is two documents.

**No clocks.** Nothing in a day folder carries a time estimate, a duration, an "estimated hours"
field or a pace. A reader may spend five sittings on one part. An explanation is **never** trimmed
because a day is getting long; the day gets another part instead.

**Zero to production, in one document.** Each part opens where a reader who has never heard of the
idea can stand, and ends where a professional stands: the real-system version, what breaks at
scale or under pressure, what a senior reviewer says, what an interviewer probes.

### 11.2 The folder shape

```text
days/day-NN-<day-slug>/
├── LESSON.md      # the hub: story · part map · setup · build brief · check · budget · ledger
├── CHECKLIST.md   # the definition of done; `{{DRIVER}} done N` refuses until it is ticked
├── parts/         # THE TEACHING — one document per subtopic, numbered <section>.<subtopic>
│   ├── 01-<slug>/
│   │   ├── 1.1-<slug>.md
│   │   └── 1.2-<slug>.md
│   └── 02-<slug>/
│       └── 2.1-<slug>.md
├── sources/       # one document per primary source the day's ideas came from (§11.4.2)
│   └── 01-<source-slug>.md
└── lab/           # the learner's own work
```

**Line by line:**

- `days/day-NN-<day-slug>/` — the number zero-padded, then a kebab-case slug of **1–4 words** taken
  from the hub's `title` with articles dropped. A number alone is an address, not an answer, and
  {{TOTAL_DAYS}} of them are indistinguishable in a file tree, a tab strip or a `git log --stat`.
- `LESSON.md` — the hub. It orients and assembles; **it never teaches** (§11.5).
- `CHECKLIST.md` — the definition of done. Without it a day has no way to be finished.
- `parts/` — **mandatory**. A day without it is not written, and a phase containing such a day
  cannot be green.
- `parts/01-<slug>/` — a section folder: two digits, then a kebab-case slug of **1–3 words** taken
  from the section's heading in the hub's map. A bare `parts/01/` is rejected by the checker.
- `sources/` — beside `parts/`, never inside it. Present only on days whose ideas come from a
  citable primary document.
- `lab/` — the learner's own work. Usually gitignored; the teaching is in `parts/`, not here.

**The number is the identity; the slug is a label on it.** Every tool resolves a day by number and
accepts any slug, so a folder can be renamed to a better slug at any time with a `git mv` and
nothing downstream notices. Part *filenames* never change — they already carry a full slug, and
renaming them would break every cross-part link for no gain.

### 11.3 The numbering rule — what `1.1` and `2.3` mean

A part filename is `<section>.<subtopic>-<kebab-slug>.md`.

- The **section** number groups subtopics that share **one mental model** — usually one curriculum
  ID, one stage of a pipeline, or one phase of a mechanism. The hub's map states what each section
  means. An unexplained grouping is a bug.
- The **subtopic** number is reading order inside that section.
- Sections run `1..N` with no gaps, and so do the subtopics inside each section. A gap means a
  document was deleted or never written, and nothing else in the repository would say so.
- The section folder's number and the number before the dot must agree.
- **Every part lives in its section's folder.** Never loose in `parts/`.
- **Links between parts are relative to the part's own folder**: a sibling is `1.2-<slug>.md`,
  another section is `../01-<slug>/1.5-<slug>.md`, the hub is `../../LESSON.md`. From a source
  document one level up: a part is `../parts/01-<slug>/1.1-<slug>.md`, the hub is `../LESSON.md`.

### 11.4 What a part document must contain

Eleven sections, **in this order**. Three are conditional — each is required exactly when its
trigger is present, and never asked for otherwise.

| # | Section | Required | What it is |
| --- | --- | --- | --- |
| 0 | **frontmatter** | always | `day`, `part`, `title`, `ids`, `level`, `prerequisites`, `prev`, `next`. Optionally `sources`, and `failure: true` on the day's deliberate-failure part. **No duration field of any kind.** |
| 1 | **One-line answer** | always | The claim in one sentence, before anything else. A reader who stops here has still learned something true. |
| 2 | **The story** | always | A concrete scene first: a person, a machine, a failure, a decision. **No jargon at all.** Four rules — see §12.2. |
| 3 | **The idea in plain language** | always | The concept assuming zero prior knowledge; every term defined on first use, *including terms from earlier days*, with a link to the part that introduced them. No code. |
| 4 | **Why {{PROJECT_NAME}} needs it** | always | The concrete later day that breaks without this. Never "this is important". |
| 5 | **The source behind it** | when `sources:` is declared | An **address, not an explanation**: the citation block (exact title · identifier · year · URL, **no authors**), **one sentence** of the claim, and a **link to the source document that teaches it**. Nothing more. |
| 6 | **The mechanism** | always | How it actually works: runnable code, the exchange written out, or the diagram. Nothing skipped as "obvious". |
| 7 | **Line by line** | when the part carries code | A `**Line by line:**` list **immediately after each code block**: every non-obvious token, and *why that line and not another*. |
| 8 | **The source in one demo** | source documents only | The source made runnable and stripped to nothing but itself. See §11.4.2. |
| 9 | **When it breaks** | always | The **real** error text, verbatim — the traceback, the status code, the message body — never a paraphrase. What it means, and the smallest fix. |
| 10 | **In production** | always | The real-system version: what a professional writes instead of the teaching version, what degrades at scale or under pressure, the failure that only shows with real traffic, the review comment, the interview question. **Not optional.** |
| 11 | **Check yourself** | always | One thing to run now, one question to answer out loud. |

**Section 10 is the one that gets dropped, and dropping it halves the document.** A part that
shows the idea working on one small case and never says what happens at ten thousand has taught
half the subject.

#### 11.4.1 Five additional rules on every part

1. **Name what you checked.** The documentation page, the specification revision, the record — with
   the date. "Verified" without an address is not verified.
2. **State the version, or leave the lookup command.** Never a remembered number (Principle 6).
3. **Respect the constraints in §4** in every command a reader is told to run.
4. **Name the trap.** If the part touches a known breaking change, a deprecated form or a common
   wrong turn, say so where the reader would otherwise take it.
5. **Never invent a citation.** Look the record up live, copy the title from the record and not
   from memory, and add a dated row to `docs/SOURCES.md`. Cite by **title and identifier, never by
   author** (§12.5).

#### 11.4.2 Source documents — one per primary source

When a day's ideas come from public primary documents — a research paper, a numbered specification
revision, a standard, a formal technical report — the day gets **one document per source**, in
`days/day-NN-<slug>/sources/`, **beside `parts/` and not inside it**, named `NN-<source-slug>.md`
and numbered from `01` in reading order.

A source document is written to the same eleven-section contract as any other part, with a part's
frontmatter **minus `part`** — it is not a subtopic of anything — and **plus `source:`
(singular)**, the one identifier it teaches. Its `level` is almost always `production`. On a source
document the sections mean:

- **The story** — the problem the field had *before this document existed*. A scene, plain words,
  no jargon, no equations. Someone was stuck; this is what stuck looked like.
- **The idea in plain language** — the claim, stated so a reader who has never opened a document
  like this can hold it and repeat it. Define the terms the title itself uses.
- **The mechanism** — the method itself, written out at the depth the rest of the day is written
  at. **Not the abstract, paraphrased.**
- **When it breaks** — where the claim does **not** hold: what it assumed, what it was measured
  on, the scale it was never tried at, the follow-up that narrowed it. A source document with no
  limits section has taught a press release.
- **In production** — **what survived and what did not**: which half of this document is in
  shipped systems today, which half the field quietly dropped, and what replaced it. This is the
  section that makes a source document worth reading rather than citing.
- **The source in one demo** — the source made runnable and stripped to nothing but itself. Four
  rules, and the third is the one that makes it honest:
  1. **Only this source's contribution.** Not a small project that uses the idea — a small project
     whose entire reason to exist *is* the idea. Subtractive test: if a file could be deleted and
     the claim still lands, delete it. Two or three files is normal.
  2. **End to end and actually runnable.** The whole file tree, every file's contents, the one
     command, and its **real pasted output**. If you have not run it, leave the output block as a
     `TODO(<the exact command>)` — **never an invented transcript**. Principle 7 outranks the
     document's shape: a missing output is fixed by one run; a fabricated one is undetectable.
  3. **An ablation switch** — one flag that turns the contribution **off**, with **both runs'
     output shown**. A demo that cannot be switched off has proved that code ran, not that this
     idea mattered. It is also a check that can go RED (Principle 9).
  4. **Inside the constraints of §4**, like everything else.

  It lands in `lab/sources/<source-slug>/` and is given **complete**. It is teaching material, not
  an exercise: the unsolved `TODO(me)` exercises stay in the hub's build brief.

**Read source documents after the parts.** The hub's map says so and the last part's *Next* points
at them. That order is Principle 3 at the scale of a day: build the mechanism by hand, *then* read
the proposal, so "what survived and what did not" lands on something the reader has built rather
than on nothing.

**A source is taught once in the whole curriculum.** The day that first needs it carries the
document; every later day cites it and links back. Two documents declaring the same identifier is
a checker failure, not a style preference.

### 11.5 What the hub (`LESSON.md`) must contain

The hub orients and assembles. **It never teaches** — no walkthrough lives here.

| # | Section | What it carries |
| --- | --- | --- |
| 0 | frontmatter | `day`, `phase`, `title`, `ids`, `kind`, `plan_version`, `parts`, `generated`, `status`, and whatever else the project tracks. No duration field. |
| 0 | blockquote | Yesterday / today / tomorrow, in three lines. No time estimate. |
| §1 | **Where we are** | A scene and an analogy. Plain language, no code, no jargon. |
| §2 | **The map** | A table of every part: number, linked title, what it answers, `level` — grouped by section, with one line saying what each *section* means. **No minutes column, ever.** If the day has `sources/`, the map ends with a table of those, marked read-after-the-parts. |
| §3 | **Setup** | Every command the day needs, pinned and runnable. |
| §4 | **Build brief** | What to make, with `TODO(me)` markers left **unsolved**. |
| §5 | **The check that must be able to fail** | The check that is RED before the build brief is done and GREEN after. State how to make it go red on purpose. |
| §6 | **Budget** | What the day spends against the §4 constraints. `0` is an answer; state it. |
| §7 | **Traps** | The mistakes that eat an evening, including any named breaking change. |
| §8 | **Verify before you build** | The live URLs actually fetched today, with what each confirmed. |
| §9 | **Say it out loud** | One paragraph, spoken voice — the answer you would give an interviewer. |
| §10 | **Done when** | A pointer to `CHECKLIST.md`. Defined by understanding and green checks, never by elapsed effort. |
| §11 | **Ledger & commit** | The verbatim `PROGRESS.md` row, any `PINS.md` / `SOURCES.md` / `GLOSSARY.md` / `PROVENANCE.md` rows, and the commit message. **The hub ends here.** |

The ritual in §11 is the point: the repository is the memory, and a memory that depends on
remembering to write it down is not one.

### 11.6 The `level` field — how a day climbs

Every part declares one:

| Level | The reader afterwards |
| --- | --- |
| `foundation` | knows what the thing is and can recognise it |
| `working` | can use it on their own problem, unaided |
| `production` | knows what changes in a real system, and what breaks |

**A day climbs.** A day that is all `foundation` is a tutorial. A day that opens at `production`
has skipped the reader.

### 11.7 How finely to split

Split by **idea boundary, never by length or pace**. There is no target part count: four parts if
the subject needs four, twenty-two if it needs twenty-two.

Three tests, applied *before* writing:

- **The one-idea test.** If the part needs "also" to introduce its second half, it is two parts.
- **The standalone test.** A part must be readable cold. Name and link its prerequisite part.
- **The no-shortcut test.** "For now, just accept that" is banned unless it links forward to the
  part that explains it. A deferred explanation must have an address.

Useful default shapes:

| Day kind | Split by |
| --- | --- |
| setup | one part per tool or file |
| mechanism | mechanism → behaviour → edge case → failure mode → production use |
| concept | one claim per part |
| gate | one acceptance criterion per part |

**Every day carries at least one part whose subject is a deliberate failure** — break it on
purpose, read the real error, fix it. That part declares `failure: true` in its frontmatter, and
is usually `level: production`.

### 11.8 What "in depth" is not

The eight failure modes this format exists to prevent. If a part shows one, it is not done.

1. **Splitting without deepening** — the same wall of text, now in six files.
2. **Summary in place of explanation** — a description of the mechanism instead of the mechanism.
3. **Stopping at the toy example** — no `In production`, so the reader learned a demo.
4. **Assuming the previous day** — an undefined term from day 12 used on day 51.
5. **Code without failure** — a happy path with no real error text anywhere.
6. **Trimming to fit** — an explanation cut because the day was getting long. Add a part instead.
7. **Solved exercises** — the `TODO(me)` reps done for the reader, who then does none.
8. **A carried-over clock** — a duration field copied from an older draft.

### 11.9 Enforcement

Run `{{DRIVER}} depth N` after writing a day. It fails on: a missing or misordered section, a
numbering gap, a bare numeric folder, a part loose in `parts/`, a code block with no walkthrough,
a malformed or unledgered citation, a source taught twice, a smuggled-in clock, a missing
deliberate-failure part, a hub that carries teaching, and a hub whose IDs disagree with §8.

**Never hand-wave past a `depth` failure.** The checker only knows the things a script can know;
everything it cannot check — whether the story is lived, whether the explanation is any good,
whether `In production` is true — is checked by reading, and a repository that argues with its
own checker will not survive the reading either.

---

## 12 · The style guide

### 12.1 The register

**Storytelling is the default.** A scene before an abstraction, every time. The reader is learning
this in order to do real work, so no idea stops at the toy example.

**Simple language first.** Plain words → a concrete example → *only then* the terminology. If a
twelve-year-old could not follow the first sentence, rewrite the first sentence.

**Define every term on first use, including terms from earlier days**, with a link back to the
part that introduced them, and a row in `docs/GLOSSARY.md`. {{TOTAL_DAYS}} days is long enough
that day 3 is forgotten by day 66.

**Grammar and punctuation are part of the deliverable**, in every section of every document.
Correct full stops and commas, no run-on sentences, and no long chain of dashes where two ordinary
sentences would read better. A sentence the reader has to parse twice has failed.

### 12.2 The story rules

The story is the hook the definition hangs on, not decoration. Four rules, and the first is the
one that gets broken:

1. **A scene the reader has plausibly lived.** A parcel and a courier. A repair-shop job card. A
   bus route map. A used car checked by a mechanic. A monthly generator test. A tailor taking
   measurements. **Not** a nautical chart, a model railway, a theatre programme, a projection
   booth or a mediaeval siege. Test: *could the reader have been standing in this scene
   themselves?* If they must first be told what the setting **is**, the analogy is carrying the
   explanation instead of hooking it.
2. **Simple words.** Short sentences beat clever ones here.
3. **Realistic and load-bearing.** The scene must contain the actual failure or decision the part
   teaches, not a pretty image the part then abandons. Every later section that reaches back for
   the metaphor must still fit it.
4. **One metaphor family per day.** Before choosing, grep the day's other parts and the hub's §1.
   Two parts reaching for the same family — two restaurants, two receptionists — read as one idea
   repeated.

### 12.3 The scene format

For failures and motivations, four beats:

> **The scene** — what someone was doing.
> **The naive fix** — what they reached for first, and why it was reasonable.
> **Why it fails** — the real failure, with the real message.
> **The insight** — the thing that actually solves it.

### 12.4 Code and commands

- **Every code block is followed by a `**Line by line:**` walkthrough** of each non-obvious token,
  and why it is that line and not another. An unexplained line is a bug in the document.
- **Every mechanism has a matching "When it breaks"** with the **real error text, verbatim**.
- **Commands are runnable as written**, in the shell this project actually uses.
- **Diagrams whenever the concept is spatial, sequential or a state machine** — a lifecycle, a
  handshake, a retry ladder, an approval gate.
- **Tables for enumerable facts, prose for reasoning.** Never a table of one row.
- **Leave `TODO(me)` exercises unsolved.** Teach; do not do the reps for the reader.

### 12.5 Facts

- Never invent a version, an interface, a limit or a citation (Principle 6).
- **Cite by title and identifier, never by author** — `arXiv:1706.03762`, `doi:10.1145/…`,
  `RFC 9110`. The identifier is the stricter attribution anyway: it resolves to exactly one
  document, and it is what a reader types.
- An unrun command's output is a `TODO` naming the exact command. **Never a plausible transcript.**

### 12.6 The two things that are never written

1. **No clocks.** No duration, no "estimated hours", no "this should take about", no pace —
   anywhere, in any document, in any field (Principle 11).
2. **No person names, no course or creator brand names.** This curriculum is self-contained and
   promotes nobody: never name an instructor, author, channel, academy, bootcamp or training
   company — in a lesson, a checklist, a docstring or a commit message. Naming the **tools** you
   actually use is required and unaffected, as is citing a specification by its revision and a
   work by its exact title and identifier.

### 12.7 The ritual

Every day ends the same way: paste the ledger rows, tick the checklist, run the gate, commit. Not
because ritual is virtuous, but because a repository that records itself is a repository you can
return to after three weeks away and still trust.

---

## 13 · Amendment record

This plan is amended, never quietly edited. Every amendment lands in `docs/CHANGELOG_PLAN.md`
before any day or any code changes, and anything structural gets an ADR in `docs/adr/`.

| Version | Date | What changed |
| --- | --- | --- |
| {{PLAN_VERSION}} | {{DATE}} | Plan adopted. See `docs/adr/ADR-0001-the-plan-as-adopted.md`. |
````

### `CLAUDE.md`

The operating rules every session in that repository reads first.

````markdown
# {{PROJECT_NAME}} — operating rules

You are the daily instructor and pair-worker for a **{{TOTAL_DAYS}}-day curriculum** on
**{{TOPIC}}**.

The single source of truth is `docs/00_MASTER_PLAN.md` ("the plan"), currently **{{PLAN_VERSION}}**.
Progress is `docs/PROGRESS.md` — the last row is where we are. Amendments are logged in
`docs/CHANGELOG_PLAN.md`. Structural decisions are ADRs in `docs/adr/`.

**This file is the router, not the contract.** It tells you what to read and what never to do. The
standard itself — how a day is written — is the plan's §11, and it is never summarised here,
because a summary that drifts from the contract is worse than no summary.

---

## Read in this order

*Always, before anything:*

1. `{{DRIVER}} brief N` — day N's assignment, the phase gate, any ID that should already be
   closed, the sources already taught, and whether N is allowed yet. One command; it replaces
   reading the plan's §8, `docs/PROGRESS.md` and `docs/TRACEABILITY.md` when that is all you need.
   **It exits non-zero if N is out of order. That is a stop, not a warning.**
2. `docs/WIKI.md` — one row per day. For what an earlier day taught, `docs/wiki/day-NN.md`. For
   "which day taught X?" or "is this source already taught?", `docs/wiki/ENTITIES.md`.
3. `docs/GLOSSARY.md` — before defining any term, check whether it is already defined. A term
   defined twice, slightly differently, is worse than a term defined once badly.

*Additionally, in full, before writing or amending a day:*

4. **`docs/00_MASTER_PLAN.md` §11 — the depth contract — in full.** It carries the judgement no
   checker can make: the one-idea test, the standalone test, and whether a story is one the reader
   has plausibly lived. Never skim it, and never let the wiki stand in for it. **§12 is the style
   guide**, and its story rules are the ones most often broken.
5. `days/day-<last>-<slug>/LESSON.md` and its `CHECKLIST.md` — how the previous day ended. If the
   checklist has unticked boxes, say so and ask before moving on.

**The wiki and the brief are generated indexes over the days, never a substitute for them.** Every
line in them is copied from a source document; nothing in them is written by a model. If an index
ever disagrees with the day it indexes, **the day is right and the index is stale** — run
`{{DRIVER}} index`. Read a day's `parts/` when you need the teaching; read its wiki page when you
need the address.

---

## Non-negotiable rules (the plan's §2)

- **Doc-first.** The day document is written before the work; the work follows the document.
- **One day, one commit.** Traceable, append-only history. The repository is the memory.
- **Build first, compare after.** Hand-roll the mechanism once, then adopt the tool that does it
  for you — so the tool is a convenience and never a mystery.
- **Never invent a fact.** A version, an interface, a limit, a citation: look it up **live**, or
  leave a `TODO` containing **the exact lookup command**. Every pin gets a dated row in
  `docs/PINS.md`; every citation gets one in `docs/SOURCES.md`.
- **Never invent a citation.** Open the record, copy the title from the record and not from
  memory. A wrong version pin fails loudly on the next install; a plausible identifier attached to
  the wrong title fails **silently, for years**. Cite by title and identifier, never by author.
- **Fail honestly.** Errors surface, escalate and are logged. Never fabricate a result to cover an
  error — this applies to you as much as to anything you build. An unrun command's output is a
  `TODO`, never a plausible transcript.
- **Every day ends with at least one check that can go RED.**
- **Blast radius before capability.** Every new power arrives with its containment story.
- **If reality changes, the plan is amended first.** Ecosystem shift → `CHANGELOG_PLAN.md` (and an
  ADR if structural) → *then* the work. Never silently adapt; stop and say so.
- **Depth over density.** A day is a hub plus one document per subtopic. Never one long page.
- **No clocks.** A day is a unit of subject, not of time. Never write a time estimate, a duration,
  an "estimated hours" field or a pace — anywhere: frontmatter, prose or checklist. A topic is
  finished when it is understood, however many sittings that takes. **Never trim an explanation
  because a day is getting long; split it into another part instead.**
- **Assume no prior knowledge, finish at production.** Open where someone who has never met the
  idea can stand, define every term on first use, and carry it through to the real-system version:
  what changes at scale, what a senior reviewer says, what an interviewer probes.

---

## The day format, in one screen

The full contract is plan §11 — **read it before writing any day.** This is the shape only.

```text
days/day-NN-<day-slug>/
├── LESSON.md      hub: story · part map · setup · build brief · check · budget · ledger
├── CHECKLIST.md   definition of done; `{{DRIVER}} done N` refuses until ticked
├── parts/         THE TEACHING — one document per subtopic
│   └── 01-<slug>/1.1-<slug>.md
├── sources/       one document per primary source — beside parts/, read after them
└── lab/           the learner's own work
```

The rules that get broken most, and are therefore worth repeating here:

- **`parts/` is mandatory.** A day without it is not written.
- **Every folder name carries its subject.** The number is the identity, the slug is a label on
  it — every tool resolves a day by number and accepts any slug, so a folder can be renamed freely.
- **The hub never teaches.** No `**Line by line:**` in `LESSON.md`; it lives in the parts.
- **The story carries no jargon** and must be a scene the reader has plausibly lived. **One
  metaphor family per day** — grep the day's other parts before choosing.
- **`In production` is not optional.** A part that shows the idea working on one small case and
  never says what happens at ten thousand has taught half the subject.
- **Every day carries at least one part declaring `failure: true`** — break it, read the real
  error, fix it.
- **A source is taught once in the whole curriculum**, in its own document, with a demo carrying an
  **ablation switch** and its **real pasted output**. Every later day cites and links it.
- **Sources are read after the parts.** Build the mechanism by hand, *then* read the proposal.
- Run `{{DRIVER}} depth N` after writing a day. **Never hand-wave past a `depth` failure.**

### Generating a day

Use `/day-{{PROJECT_SLUG}} N`, at `.claude/skills/day-{{PROJECT_SLUG}}/SKILL.md`.

- Confirm **N is exactly one more than the last row in `docs/PROGRESS.md`.** If not, say so and
  stop.
- Write **only** the day folder. Do not do the work the learner is meant to do.
- Close **exactly** the concept IDs the plan's §8 assigns to day N. No more, no fewer.

**Never:** skip a day, merge two days, or reorder days without an ADR · invent a version, an
interface or a citation.

---

## Environment

{{ENVIRONMENT_BLOCK}}

```bash
# the day-N brief          → {{DRIVER}} brief N
# open day N               → {{DRIVER}} start N
# scaffold an empty day    → {{DRIVER}} new N [slug]
# depth contract           → {{DRIVER}} depth [N]
# regenerate the indexes   → {{DRIVER}} index
# whole-project gate       → {{DRIVER}} check
# finish a day             → {{DRIVER}} done N     (refuses on an unticked checklist)
# is the repo wired right? → {{DRIVER}} doctor
```

**Definition of done for any change:** the gate is green — and you actually ran it, not "should
pass."

---

## Style for generated teaching material

The full guide is plan §12. The operational core:

- **A scene before an abstraction, every time**, and the scene must be one the reader has
  plausibly lived — a parcel and a courier, a repair-shop job card, a used car checked by a
  mechanic. Not a nautical chart or a model railway. If the reader must first be told what the
  setting *is*, the analogy is carrying the explanation instead of hooking it.
- **Simple language first.** Plain words → concrete example → *only then* the terminology.
- **Grammar and punctuation are part of the deliverable**, in every section of every document. A
  sentence the reader has to parse twice has failed.
- **Define every term on first use, including terms from earlier days**, with a link back and a
  row in `docs/GLOSSARY.md`.
- **EVERY code block is followed by a `**Line by line:**` walkthrough** — every non-obvious token,
  and why it is that line and not another. An unexplained line is a bug in the doc.
- **Every mechanism has a matching "When it breaks"** with the **real error text**, verbatim.
- **Diagrams** whenever the concept is spatial, sequential, or a state machine.
- **Tables for enumerable facts, prose for reasoning.** Never a table of one row.
- Leave `TODO(me)` sections unsolved. Teach; don't do the reps for the learner.
- **No person names, no course or creator brand names** — not in a lesson, a checklist, a
  docstring or a commit message. Tool names are required and unaffected.

---

## How to work on this repository

1. **State assumptions out loud** before anything non-trivial. If you had to guess, the guess is a
   line the reader needs to see.
2. **If the request is ambiguous, ask** — or enumerate the readings and say which one you took.
3. **Push back when warranted.** A bad idea named early costs one paragraph; named late, a phase.
4. **Touch only what the task requires.** No drive-by refactors and no reformatting. Notice
   problems and *mention* them; do not silently fix them.
5. **Run the checks and report what actually happened.** Never claim something passes that you did
   not run.
6. **Three failed attempts at the same approach means the approach is wrong.** Stop and reconsider
   out loud rather than trying a fourth variation.
````

### `README.md`

````markdown
# {{PROJECT_NAME}}

**{{TOPIC}}** — {{TOTAL_DAYS}} days, {{PHASE_COUNT}} phases, {{ID_TOTAL}} concepts, one artifact.

{{ONE_PARAGRAPH_PITCH}}

## Where to start

| You want | Open |
| --- | --- |
| The contract everything obeys | [`docs/00_MASTER_PLAN.md`](docs/00_MASTER_PLAN.md) |
| Where the work actually is | [`docs/PROGRESS.md`](docs/PROGRESS.md) — the last row |
| What each day teaches | [`docs/WIKI.md`](docs/WIKI.md) |
| Where a concept is taught | [`docs/CURRICULUM_INDEX.md`](docs/CURRICULUM_INDEX.md) |
| What is written and what is not | [`docs/TRACKER.md`](docs/TRACKER.md) |
| Why something is the way it is | [`docs/adr/`](docs/adr/) |

## The commands

```bash
{{DRIVER}} status        # how many days are complete, and what is next
{{DRIVER}} brief N       # what day N must cover, and whether N is allowed yet
{{DRIVER}} start N       # open day N in reading order
{{DRIVER}} depth N       # check day N against the depth contract
{{DRIVER}} check         # the whole-repository gate
{{DRIVER}} done N        # finish a day: refuses on an unticked checklist, then commits
{{DRIVER}} doctor        # is this repository wired correctly?
```

## How a day is written

A day is a **hub plus one document per subtopic**, never one long page. Every subtopic document
opens where a reader who has never met the idea can stand and ends at the real-system version:
what breaks at scale, what a senior reviewer says, what an interviewer probes.

Three rules make that more than an aspiration:

- **No clocks.** No document carries a duration, an estimate or a pace. An explanation is never
  trimmed because a day is running long — the day gets another part instead.
- **Never invent a fact.** Versions, interfaces and citations are looked up live on the day they
  are used, with a dated ledger row. A failed lookup leaves the exact command, never a guess.
- **Every day ends with a check that can go RED**, and at least one part per day is a deliberate
  failure: break it, read the real error, fix it.

The full contract is [§11 of the plan](docs/00_MASTER_PLAN.md), and `{{DRIVER}} depth` enforces
the half of it a script can check.

## Layout

```text
docs/       the plan, the ledgers, the ADRs, the generated indexes
days/       the teaching — one folder per day
granth.py   the whole toolchain, one file, stdlib only
granth.toml this repository's identity and the contract's knobs
```

---

Scaffolded with [granth](https://github.com/{{GITHUB_USER}}/granth).
````

### `.gitignore`

Secrets are excluded before the first secret exists.

````text
# Secrets never touch git. This file exists before the first secret does.
.env
.env.*
!.env.example
*.key
*.pem
credentials.json
secrets.*

# The learner's own work. The teaching lives in parts/; lab/ is where you make mistakes.
days/*/lab/

# Generated locally, never committed
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.mypy_cache/
.venv/
venv/
node_modules/
dist/
build/
*.egg-info/

# Editors and operating systems
.DS_Store
Thumbs.db
.idea/
*.swp
````

### `.env.example`

Only if the topic needs secrets. One row per variable; drop the file entirely otherwise.

````bash
# Copy to .env and fill in. `.env` is gitignored; this file is not.
#
# Every variable here is documented on the day that introduced it. If you are looking at a name
# and cannot tell what it is for, that is a bug in that day's document — say so.

# {{ENV_VAR_1_COMMENT}}
{{ENV_VAR_1}}=
````

### `docs/PROGRESS.md`

````markdown
# Progress ledger — {{PROJECT_NAME}}

Append-only. **The last row is where we actually are.** One row per *completed* day, pasted from
that day's hub §11 before `{{DRIVER}} done N` will commit. A day with no row here is not finished,
whatever the folder looks like.

Nothing is ever deleted from this table. A day that went wrong gets a note under it saying what
went wrong — a ledger that only records successes is a ledger nobody can learn from.

| Day | Date | IDs closed | Parts | Commit | Gates green? |
| --- | ---- | ---------- | ----- | ------ | ------------ |
````

### `docs/PINS.md`

````markdown
# Pin ledger — {{PROJECT_NAME}}

Append-only. **Never invent a fact** (plan §2, Principle 6). Every version, tool, limit or quota
this project depends on gets a row here with the value **actually observed**, the date it was
observed, the day that added it, and why.

If a value could not be looked up, the row says `TODO(<the exact lookup command>)` — never a
guess. A guess that happens to be right is still a guess, and the next reader cannot tell which
kind they are holding.

A later row may **supersede** an earlier one: a dated observation superseding a dated observation
is not an amendment, it is the ledger doing its job. Say so in the `Why` column.

| What | Value | Date observed | Day | Why, and how it was observed |
| ---- | ----- | ------------- | --- | ---------------------------- |
````

### `docs/SOURCES.md`

````markdown
# Source ledger — {{PROJECT_NAME}}

Append-only. **Never invent a citation** (plan §11.4.1, rule 5). Every primary source a document
teaches or cites gets a row here, and the row is written **only after the record was opened
live** and the title copied from it rather than from memory.

This is the strictest of the three verification rules because it fails the most quietly. A wrong
version pin breaks the next install. A plausible identifier attached to the wrong title survives
for years, gets copied into other people's notes, and is never caught.

**Cite by title and identifier, never by author.** The identifier resolves to exactly one
document, and it is what a reader types.

Accepted identifier forms: `arXiv:2401.12345` · `doi:10.1145/3597503` · `RFC 9110` ·
`ISO/IEC 9899:2018` · `spec:<name>-<revision>`. Anything citation-shaped that matches none of
these is rejected by `{{DRIVER}} depth`.

| Identifier | Exact title | Year | URL | Record checked | Taught on | Cited by |
| ---------- | ----------- | ---- | --- | -------------- | --------- | -------- |
````

### `docs/GLOSSARY.md`

````markdown
# Glossary — {{PROJECT_NAME}}

Append-only. One row per term, defined **once**, with the part that introduced it.

This file exists because {{TOTAL_DAYS}} days is long enough that day 3 is forgotten by day 66. Its
real job is not to be read front to back; it is to be **checked before defining anything**, so
that a term is never defined twice, slightly differently, in two places. Two nearly-identical
definitions are worse than one bad definition, because the reader cannot tell which is current.

Before you define a term in a day document, search this file. If it is here, link the part that
introduced it instead of redefining it.

| Term | Plain-language definition | Introduced in | Also called |
| ---- | ------------------------- | ------------- | ----------- |
````

### `docs/PROVENANCE.md`

````markdown
# Provenance ledger — {{PROJECT_NAME}}

Append-only. Every third-party thing this project runs, vendors or depends on gets a row here
**before it is ever run** — source, licence, version, who audited it and when, and what it is
permitted to touch.

This is Principle 12, blast radius before capability, written as a table. A dependency you have
not audited is a capability you have granted without deciding to.

| What | Source | Version | Licence | Audited on | Audited by | Permitted scope |
| ---- | ------ | ------- | ------- | ---------- | ---------- | --------------- |
````

### `docs/CHANGELOG_PLAN.md`

````markdown
# Plan changelog — {{PROJECT_NAME}}

Principle 8: *if reality changes, the plan is amended first.* Every amendment lands here **before**
any day or any work changes. **Append-only. Newest last.**

An entry answers three questions in this order: **what moved in the world**, **what this plan now
says instead**, and **what that costs** — which days are affected, which IDs move, what has to be
rewritten. An entry that names the change but not its cost is a note, not an amendment.

Anything structural — a change to the day format, the ID scheme, the phase boundaries, the
toolchain — also gets an ADR in `docs/adr/`, and the entry here links it.

---

- {{DATE}} — Plan adopted at {{PLAN_VERSION}}. See `docs/adr/ADR-0001-the-plan-as-adopted.md`.
````

### `docs/adr/README.md`

````markdown
# Architecture Decision Records — {{PROJECT_NAME}}

One file per structural decision: `ADR-NNNN-<kebab-slug>.md`, numbered from `0001`, **never
renumbered and never rewritten**. A decision that turns out wrong is **superseded** by a later ADR
that says so; the original stays exactly as it was written.

That rule is the whole value. An ADR set you can edit is a set that always looks like it was right
from the start, which teaches nothing. An ADR set you cannot edit records what was known at the
time, which is the only thing that makes the next decision easier.

## When an ADR is required

Write one for anything **structural** — a change to the shape of the work rather than to its
content:

- the day format, the ID scheme, the phase boundaries, the numbering rule
- skipping, merging, reordering or inserting a day (the plan forbids doing this without one)
- adopting, replacing or dropping a tool the whole project depends on
- a change in scope: something the plan promised and no longer will, or the reverse
- a constraint that turned out to be wrong

Do **not** write one for: a version bump (that is `PINS.md`), a wording change (that is
`CHANGELOG_PLAN.md`), or a decision inside a single day (that belongs in the day).

Rule of thumb: **if someone six months from now would ask "why on earth is it like this?", it
needs an ADR.** If they would not notice, it does not.

## The relationship to the changelog

`CHANGELOG_PLAN.md` records **what the plan now says**. An ADR records **why, and what else was
considered**. A structural change gets both, and the changelog entry links the ADR.

## The template

Copy `ADR-0000-template.md`. Every section is required; an ADR with no *Options considered* is a
justification written after the fact, not a decision record.

| # | Title | Date | Status |
| --- | --- | --- | --- |
| [0001](ADR-0001-the-plan-as-adopted.md) | The plan as adopted | {{DATE}} | accepted |
````

### `docs/adr/ADR-0000-template.md`

The blank ADR. Its `<...>` markers are meant to stay — a writer fills them.

````markdown
# ADR-NNNN — <the decision, as a sentence in the present tense>

- **Date:** YYYY-MM-DD
- **Day:** <the day this came up, or "between days N and N+1">
- **Phase:** <phase number>
- **Status:** proposed | accepted | superseded by ADR-NNNN | rejected
- **Amends:** <plan version → plan version, and which sections>, or "nothing"
- **Related:** <other ADRs>

## Context

What is actually true right now that makes this a decision rather than a preference. Be concrete:
the file tree as it stands, the error as it reads, the number as it was measured. If the problem
compounds — costs more the longer it is left — say by how much and over what.

A reader six months from now has none of today's context. This section is the only place they can
get it.

## Decision

What we are doing, in the present tense, in as few sentences as it takes. Then the specifics: the
shape, the rule, the boundary. If the decision has a load-bearing half — the part that makes it
safe or reversible — say which half that is and why.

## Options considered

| Option | Why not |
| --- | --- |
| **<the status quo>** | Always list this one. "Do nothing" is a real option, and rejecting it is a real decision. |
| **<the cheaper option>** | |
| **<the more thorough option>** | |

## Consequences

What is better now. What is worse now — this row is required; a decision with no cost was not a
decision. What new failure mode this creates, and what catches it. What would have to be true for
this to be revisited.
````

### `docs/adr/ADR-0001-the-plan-as-adopted.md`

The founding record: the decisions taken in the interview, and what was rejected.

````markdown
# ADR-0001 — The plan as adopted

- **Date:** {{DATE}}
- **Day:** before day {{FIRST_DAY}}
- **Phase:** —
- **Status:** accepted
- **Amends:** nothing — this is the founding record
- **Related:** `docs/00_MASTER_PLAN.md` {{PLAN_VERSION}}

## Context

This repository teaches **{{TOPIC}}** over {{TOTAL_DAYS}} days, and it exists because the obvious
alternatives do not work:

- **Following a course** produces something that runs and understanding that evaporates the moment
  the inputs change. There is no artifact to defend and no record of why anything is as it is.
- **Reading documentation** covers the surface in the order the documentation was written, which
  is the vendor's order and not a learner's. Nothing forces the ideas to connect.
- **Building a project with no plan** teaches whatever the project happened to need, leaves the
  gaps invisible, and cannot tell a thin subject from a missing one.

The plan answers all three: a fixed day-to-concept map, so gaps are visible; one artifact, so every
concept is load-bearing; and a depth contract, so a subject is either covered properly or
mechanically flagged as not covered at all.

The decisions below were taken at the start, together, because each is expensive to change once
days exist.

## Decision

**{{PLAN_VERSION}} of `docs/00_MASTER_PLAN.md` is adopted as the single source of truth.** In
particular:

| Decision | As adopted | Why this and not the alternative |
| --- | --- | --- |
| **Scope** | {{TOTAL_DAYS}} days, {{PHASE_COUNT}} phases, {{ID_TOTAL}} concept IDs across {{TRACK_COUNT}} tracks | {{SCOPE_RATIONALE}} |
| **The artifact** | {{ARTIFACT_ONE_LINE}} | One artifact makes Principle 4 checkable: delete a concept and see whether the artifact still works. |
| **Day format** | A hub plus one document per subtopic (plan §11) | A single-file day silently becomes a wall of text under one heading. A reader cannot revisit one idea without re-reading four, and nothing distinguishes a thin subtopic from a missing one. |
| **No clocks** | No duration, estimate or pace in any document (Principle 11) | A duration field silently authorises the worst edit in technical writing: cutting an explanation because the day is running long. |
| **Verification** | Versions, interfaces and citations looked up live, with dated ledger rows (Principle 6) | Notes written from memory rot silently. A citation written from memory rots most silently of all. |
| **Constraints** | {{CONSTRAINTS_ONE_LINE}} | A constraint written down is a curriculum. A constraint discovered on day 40 is a rewrite. |

## Options considered

| Option | Why not |
| --- | --- |
| **No plan — build and see what comes up** | Teaches whatever the project happened to need. Gaps stay invisible, and there is no way to tell a subject covered thinly from one skipped entirely. |
| **A topic list instead of a day map** | A list has no order and no gate, so nothing ever has to work. The day map is what makes "am I allowed to start day 27?" a mechanical question. |
| **One file per day** | The format this plan explicitly replaces — see the day-format row above. |
| **A shorter curriculum** | Fewer days helps only if the subject is smaller. Trimming days without trimming scope is Principle 11's failure mode with extra steps. |

## Consequences

- **Better:** every concept has exactly one address; a thin day is visible from the tracker alone;
  the repository can be picked up after three weeks away, because the last ledger row says where
  we are.
- **Worse:** the format has real overhead. Eleven sections per part is a lot of structure, and some
  days will be slower to write than the subject strictly requires.
- **New failure mode:** the generated indexes can go stale and start disagreeing with the days.
  Caught by `{{DRIVER}} check`, which fails if any generated document is out of date.
- **Revisit if:** the eleven-section contract starts producing padding — sections filled to satisfy
  the checker rather than the reader. That is a signal the contract is wrong for this subject, and
  it gets its own ADR rather than a quiet exception.
````

### `days/README.md`

````markdown
# `days/` — the teaching

One folder per day, `day-NN-<slug>/`. The number is the identity; the slug is a label on it, so a
folder can be renamed to a better slug at any time and nothing downstream notices.

```text
days/day-NN-<day-slug>/
├── LESSON.md      # the hub — orients and assembles; it never teaches
├── CHECKLIST.md   # the definition of done
├── parts/         # THE TEACHING — one document per subtopic
│   └── 01-<slug>/1.1-<slug>.md
├── sources/       # one document per primary source (only on days that have one)
└── lab/           # your own work — gitignored
```

**Read a day in this order:** the hub's §1 and §2, then every part in number order, then the
sources. That last step is deliberate: you build the mechanism by hand first and read the original
proposal afterwards, so "what survived and what did not" lands on something you have built.

**Write a day** with `/day-{{PROJECT_SLUG}} N`, or scaffold an empty one with
`{{DRIVER}} new N <slug>`. The standard every day is held to is the plan's §11.

`_TEMPLATES/` holds the blank documents `{{DRIVER}} new` copies from. It is not a day and no tool
treats it as one.
````

### `days/_TEMPLATES/LESSON.md`

The hub template. `NN`, `S.T` and `<slug>` stay; the `{{...}}` placeholders do not.

````markdown
---
day: NN
phase: P
phase_name: "<the phase theme, from the plan's §7>"
title: "<the day's subject as a phrase — this is where the folder slug comes from>"
ids: [XX-00, XX-01]
kind: concept            # concept | mechanism | setup | gate
plan_version: "{{PLAN_VERSION}}"
parts: 0                 # must equal the number of documents in parts/
generated: "YYYY-MM-DD"
status: draft            # draft | written | complete
commit: ""               # filled in by the ledger row, after the commit exists
---

<!--
  THE HUB ORIENTS AND ASSEMBLES. IT NEVER TEACHES.

  No `**Line by line:**` in this file — a walkthrough here means a subtopic has been explained in
  the one document meant to be readable in a single pass. No duration, estimate or pace anywhere.

  Eleven numbered sections, in order. Delete every one of these comments before finishing.
-->

> **Yesterday:** <what day N-1 left you holding.>
> **Today:** <the one sentence version of this day.>
> **Tomorrow:** <what this unlocks.>

## §1 Where we are

<!-- A scene and an analogy. Plain language, NO CODE, NO JARGON. This is the only place in the day
     that is allowed to be purely orienting — use it. One metaphor family for the whole day: what
     you pick here, the parts must not collide with. -->

## §2 The map

<!-- One line saying what each SECTION means — the mental model its parts share — then the table.
     No minutes column, ever. -->

### 1 · <what this section is about>

<!-- one line: the mental model these parts share -->

| Part | Title | What it answers | Level |
| --- | --- | --- | --- |
| [1.1](parts/01-<slug>/1.1-<slug>.md) | <title> | <the question> | foundation |

### 2 · <what this section is about>

| Part | Title | What it answers | Level |
| --- | --- | --- | --- |
| [2.1](parts/02-<slug>/2.1-<slug>.md) | <title> | <the question> | working |

<!-- If the day has sources/, add this table and mark it read-after-the-parts. Build the mechanism
     by hand first; read the original proposal afterwards. -->

### Sources — read these **after** the parts

| # | Source | Identifier |
| --- | --- | --- |
| [01](sources/01-<slug>.md) | <title> | `<identifier>` |

## §3 Setup

<!-- Every command this day needs, pinned and runnable as written, in the shell this project
     actually uses. A command that has not been run is a TODO, not a step. -->

```bash
<!-- the setup commands -->
```

## §4 Build brief

<!-- What to make. Leave every `TODO(me)` UNSOLVED — teach, do not do the reps. -->

| File | What it must do |
| --- | --- |
| `<path>` | `TODO(me)`: <the rep> |

## §5 The check that must be able to fail

<!-- The check that is RED before the build brief is done and GREEN after. State how to make it go
     red on purpose — a check nobody has seen fail is a check nobody has tested. -->

## §6 Budget

<!-- What this day spends against the constraints in the plan's §4. `0` is an answer; state it. -->

## §7 Traps

<!-- The mistakes that eat an evening. Name any breaking change, deprecated form or common wrong
     turn exactly where the reader would otherwise take it. -->

## §8 Verify before you build

<!-- The live URLs actually fetched TODAY, and what each one confirmed. Never from memory. -->

| What | Where it was checked | Date | What it confirmed |
| --- | --- | --- | --- |

## §9 Say it out loud

<!-- One paragraph, spoken voice — the answer you would give an interviewer who asked what you did
     today and why it was done this way. -->

## §10 Done when

See [`CHECKLIST.md`](CHECKLIST.md). Defined by understanding and green checks, never by effort
spent.

## §11 Ledger & commit

<!-- The verbatim rows to paste, and the commit message. The hub ends here. -->

**`docs/PROGRESS.md`:**

```text
| NN | YYYY-MM-DD | XX-00, XX-01 | <parts> | <hash> | yes |
```

**`docs/GLOSSARY.md`** — one row per term this day defined for the first time:

```text
| <term> | <plain-language definition> | day NN part S.T | <also called> |
```

<!-- Add PINS.md / SOURCES.md / PROVENANCE.md rows here if this day earned any. -->

**Commit:**

```text
day NN: <title> — closes XX-00, XX-01
```
````

### `days/_TEMPLATES/CHECKLIST.md`

````markdown
# Day NN — definition of done

`{{DRIVER}} done NN` refuses to commit while any box below is unticked. That refusal is the point:
a day is finished when it is understood and the checks are green, and by nothing else.

No box here carries a time estimate, and none ever will.

## Read

<!-- One box per part document. Reading it is not enough — run its check and answer its question
     out loud, because "I followed that" and "I could explain that" are different states. -->

- [ ] `parts/01-<slug>/1.1-<slug>.md` — read · ran its check · answered its question out loud
- [ ] `parts/01-<slug>/1.2-<slug>.md` — read · ran its check · answered its question out loud

<!-- Sources come after the parts, deliberately. -->

- [ ] `sources/01-<slug>.md` — read · ran the demo · ran the ablation and saw the difference

## Build

<!-- One box per `TODO(me)` in the hub's §4. -->

- [ ] `<path>` — <the rep>

## Check

- [ ] The day's check is green: `<command>`
- [ ] **Break it on purpose, watch it go red, fix it.** <what to break>
- [ ] `{{DRIVER}} depth NN` — green
- [ ] `{{DRIVER}} check` — green across the whole repository

## Record

- [ ] Every term defined for the first time today has a row in `docs/GLOSSARY.md`
- [ ] Every version or limit observed today has a dated row in `docs/PINS.md`
- [ ] Every source cited today has a dated row in `docs/SOURCES.md`
- [ ] The `docs/PROGRESS.md` row is pasted from the hub's §11
- [ ] Committed with the message from the hub's §11
````

### `days/_TEMPLATES/PART.md`

The subtopic template — the eleven sections, with the guidance a writer needs in each.

````markdown
---
day: NN
part: "S.T"
title: "<what this part teaches, as a phrase — not 'Part 3'>"
ids: [XX-00]
level: foundation        # foundation | working | production — a day climbs
prerequisites: ["<the part that must be read first, or none>"]
prev: "S.T-<slug>.md"    # relative to this folder; "" on the first part
next: "S.T-<slug>.md"    # relative to this folder; "" on the last part
sources: []              # identifiers this part leans on; drop the key if none
# failure: true          # uncomment on the day's deliberate-failure part
---

<!--
  Eleven sections, in this order. Three are conditional:
    "The source behind it"    — required exactly when `sources:` above is non-empty
    "Line by line"            — required after every code block that carries logic
    "The source in one demo"  — source documents only; delete it here

  No duration field, no time estimate, no pace — anywhere in this file.
  Delete every one of these comments before the part is finished.
-->

## One-line answer

<!-- The claim in one sentence, before anything else. A reader who stops here has still learned
     something true. If you cannot write this sentence, the part is not one idea yet. -->

## The story

<!-- A concrete scene FIRST: a person, a machine, a failure, a decision. NO JARGON AT ALL.

     Four rules:
     1. A scene the reader has plausibly LIVED. A parcel and a courier. A repair-shop job card.
        A used car checked by a mechanic. Not a nautical chart, not a model railway. Test: could
        the reader have been standing in this scene themselves?
     2. Simple words. If a twelve-year-old could not follow the first sentence, rewrite it.
     3. Load-bearing. The scene must contain the ACTUAL failure or decision this part teaches —
        not a pretty image the part then abandons.
     4. One metaphor family per day. Grep the day's other parts before choosing. -->

## The idea in plain language

<!-- The concept assuming zero prior knowledge. Every term defined on first use — INCLUDING terms
     from earlier days, with a link to the part that introduced them and a row in
     docs/GLOSSARY.md. No code in this section. -->

## Why {{PROJECT_NAME}} needs it

<!-- The concrete later day that breaks without this, named and linked. Never "this is
     important" — that sentence carries no information. -->

## The source behind it

<!-- CONDITIONAL: present exactly when `sources:` in the frontmatter is non-empty; delete the
     heading otherwise. An ADDRESS, not an explanation:

       > **<Exact title>** · `<identifier>` · <year>
       > <url>

     One sentence of what it claimed, then a link to the source document that teaches it — in
     this day's sources/ or an earlier day's. Nothing more; the teaching happens there. -->

## The mechanism

<!-- How it ACTUALLY works: runnable code, the exchange written out, or the diagram. Nothing
     skipped as "obvious". A diagram whenever the concept is spatial, sequential or a state
     machine. -->

```
<!-- the code, the command, or the exchange -->
```

**Line by line:**

<!-- REQUIRED immediately after every code block that carries logic. Every non-obvious token, and
     WHY THAT LINE AND NOT ANOTHER. An unexplained line is a bug in this document: the reader can
     copy it but cannot change it. -->

- `<token>` — <what it does, and why this and not the obvious alternative>

## When it breaks

<!-- The REAL error text, verbatim — the traceback, the status code, the message body. Never a
     paraphrase, never a reconstruction from memory. Then: what it means, and the smallest fix.

     If you have not seen this error yet, go and cause it. -->

```text
<!-- the real, pasted error -->
```

## In production

<!-- NOT OPTIONAL. This is the section that makes the document professional rather than
     introductory, and it is the one that gets dropped.

     Cover: what a professional writes instead of the teaching version · what degrades at scale or
     under pressure · the failure that only shows with real traffic · the review comment a senior
     engineer leaves on the teaching version · the interview question that finds out whether you
     have actually used this. -->

## Check yourself

<!-- One thing to RUN right now, and one question to answer OUT LOUD. Not a quiz — a check that
     can go red, and a sentence you either can or cannot say. -->

- **Run:** `<command>` — expect `<what>`.
- **Say out loud:** <the question>

---

**Next:** [<title>](<S.T-slug>.md)
````

### `days/_TEMPLATES/SOURCE.md`

The primary-source template: a part's frontmatter minus `part`, plus `source`.

````markdown
---
day: NN
source: "<one identifier — arXiv:2401.12345 | doi:10.1145/… | RFC 9110 | spec:name-revision>"
title: "<the source's exact title, copied from the record and never from memory>"
ids: [XX-00]
level: production        # a source document is almost always production
prerequisites: ["../parts/01-<slug>/1.1-<slug>.md"]
prev: ""                 # relative to sources/
next: ""
---

<!--
  A source document carries a part's frontmatter MINUS `part` — it is not a subtopic of anything —
  and PLUS `source:` (singular), the one identifier it teaches.

  It carries the same eleven sections, but four of them mean something different here, and one
  more becomes required. Read the guidance in each section below.

  A SOURCE IS TAUGHT ONCE IN THE WHOLE CURRICULUM. Before writing this file, check
  docs/wiki/ENTITIES.md. If the identifier is already there, do not write this document — cite the
  existing one and link it.

  Before writing a single line: OPEN THE RECORD LIVE and copy the title from it. Then add a dated
  row to docs/SOURCES.md. Never a remembered citation.

  Delete every one of these comments before the document is finished.
-->

> **<Exact title>** · `<identifier>` · <year>
> <url> — record checked <YYYY-MM-DD>

## One-line answer

<!-- What this source claimed, in one sentence a reader can repeat. -->

## The story

<!-- The problem the field had BEFORE this document existed. A scene, plain words, no jargon and
     no equations. Someone was stuck; this is what stuck looked like.

     The four story rules still apply: a setting the reader has lived in, simple words,
     load-bearing, and no collision with another story in the same day. -->

## The idea in plain language

<!-- The claim, stated so a reader who has never opened a document like this can hold it and
     repeat it. Define the terms the title itself uses. -->

## Why {{PROJECT_NAME}} needs it

<!-- The part of THIS day, linked, that runs on this idea. -->

## The mechanism

<!-- The method itself, written out at the depth the rest of the day is written at.

     NOT THE ABSTRACT, PARAPHRASED. If this section could have been written without reading past
     the first page, it has not been written. -->

## The source in one demo

<!-- REQUIRED on a source document: the source made runnable and stripped to nothing but itself.

     Four rules, and the third is the one that makes it honest:

     1. ONLY this source's contribution. Not a small project that uses the idea — a small project
        whose entire reason to exist IS the idea. Subtractive test: if a file could be deleted and
        the claim still lands, delete it. Two or three files is normal.
     2. END TO END and actually runnable: the whole file tree, every file's contents, the one
        command, and its REAL PASTED OUTPUT. If you have not run it, leave the output block as a
        TODO naming the exact command — NEVER AN INVENTED TRANSCRIPT.
     3. AN ABLATION SWITCH — one flag that turns the contribution OFF, with BOTH runs' output
        shown. A demo that cannot be switched off has proved that code ran, not that this idea
        mattered. It is also a check that can go RED.
     4. Inside the project's constraints, like everything else.

     It lands in lab/sources/<source-slug>/ and is given COMPLETE. This is teaching material, not
     an exercise — the unsolved TODO(me) reps stay in the hub's build brief. -->

```text
lab/sources/<source-slug>/
├── <file>
└── <file>
```

**Line by line:**

- `<file>` — <why this file exists, and why nothing else does>

### With the idea on

```text
<!-- the real, pasted output -->
```

### With the idea off (the ablation)

```text
<!-- the real, pasted output of the same command with the switch flipped -->
```

<!-- Then one sentence: what changed between the two runs, and why that is the source's claim. -->

## When it breaks

<!-- Where the claim does NOT hold: what it assumed, what it was measured on, the scale it was
     never tried at, the follow-up that narrowed it.

     A source document with no limits section has taught a press release. -->

## In production

<!-- WHAT SURVIVED AND WHAT DID NOT. Which half of this document is in shipped systems today,
     which half the field quietly dropped, and what replaced it.

     This is the section that makes a source document worth reading rather than citing. -->

## Check yourself

- **Find:** <one thing to locate in the source itself — a figure, a limit, a caveat>.
- **Say out loud:** what did this source actually claim, and what do we do differently now?
````

### `.claude/settings.json`

Pre-allow only the read-only commands this project genuinely runs constantly. An allowlist copied from elsewhere is a permission grant nobody decided on.

````json
{
  "permissions": {
    "allow": [
      "Bash(python granth.py status)",
      "Bash(python granth.py brief:*)",
      "Bash(python granth.py depth:*)",
      "Bash(python granth.py index:*)",
      "Bash(python granth.py check)",
      "Bash(python granth.py doctor)"
    ]
  }
}
````

### `.claude/skills/day-{{PROJECT_SLUG}}/SKILL.md`

The project's own day-writing skill. This is what makes the generated repository stand alone: someone who clones it without granth installed can still write days in it.

````markdown
---
name: day-{{PROJECT_SLUG}}
description: Write day N of the {{PROJECT_NAME}} curriculum — the hub, the parts/ sub-documents, any source documents, the lab scaffold and the checklist — against the depth contract in docs/00_MASTER_PLAN.md §11. Use when asked to write, generate, draft or continue a day of this curriculum, or when the user types a bare day number.
argument-hint: "[day-number]"
---

# Write day $ARGUMENTS of {{PROJECT_NAME}}

> **Read `docs/00_MASTER_PLAN.md` §11 in full before writing a single line.** It is the depth
> contract this skill implements. This file is the *procedure*; §11 is the *standard*, and the
> standard wins wherever the two seem to disagree.

## The three commitments (§11.1 — everything below follows from these)

1. **One idea per document.** If it needs "also" to introduce its second half, it is two documents.
2. **No clocks.** Never a time estimate, a duration, an "estimated hours" field or a pace — not in
   frontmatter, not in prose, not in the checklist. **Never trim an explanation because the day is
   getting long; split it into another part instead.**
3. **Zero to production, in one document.** Open where a reader who has never heard of the idea
   can stand. End where a professional stands.

---

## Step 1 — gather

1. Run `{{DRIVER}} brief $ARGUMENTS`. **If it exits non-zero, stop and report why.** It carries the
   assignment, the phase gate, the IDs that should already be closed, the sources already taught,
   and the order guard. Do not argue with the guard: skipping, merging or reordering a day needs
   an ADR, written first.
2. Read the plan: **§2** (the principles), **§4** (the constraints every command must respect),
   **§5** (the baseline and how it is verified), **§8** (the day map — the authoritative ID list
   for day $ARGUMENTS), **§11** (the depth contract), **§12** (the style guide).
3. Read `docs/GLOSSARY.md`. Any term already defined there is **linked, not redefined**. Two
   nearly-identical definitions are worse than one bad one.
4. Read the previous day's `LESSON.md` and `CHECKLIST.md`. If the checklist has unticked boxes,
   say so and ask before proceeding. Build on what earlier days told the learner to make; never
   duplicate it and never rewrite it.
5. Read `docs/wiki/ENTITIES.md` before deciding this day teaches a source. **A source is taught
   once in the whole curriculum.** If it is already there, cite and link it instead.

## Step 2 — verify reality before you write (Principle 6)

6. **Never invent an interface.** For every symbol, flag, endpoint or field the day will use,
   fetch the live official page and note the URL and the date. The part that uses it names the
   page checked, and the hub's §8 tabulates them. If the live documentation disagrees with the
   plan, **stop and propose an amendment** — do not silently adapt.
7. **Never invent a version or a limit.** Read it live before pinning it, and record what, the
   value, the date, the day and why in `docs/PINS.md`. A failed lookup leaves `TODO(<the exact
   command>)` — never a guess.
8. **Never invent a citation.** For every source the day will teach or cite, **open the record
   live** and copy the title from it rather than from memory. Record identifier, exact title,
   year, URL and the date checked in `docs/SOURCES.md`. This is the rule that bites hardest: a
   wrong version pin fails loudly on the next install, while a plausible identifier attached to
   the wrong title fails **silently, for years**. Cite by **title and identifier, never by author**.

## Step 3 — plan the split (before writing any prose)

9. List the day's subtopics. Group them into **sections that share one mental model** — usually
   one curriculum ID, one stage of a pipeline, or one phase of a mechanism. State the grouping;
   an unexplained numbering is a bug.
10. Split by **idea boundary, never by length or pace** (§11.7). There is no target part count:
    four if the subject needs four, twenty-two if it needs twenty-two.
11. **Ask what the day's ideas came from.** Is there a public, citable origin document — a
    research paper, a numbered specification revision, a standard, a formal report? If so the day
    gets **one document per source in `sources/`**, beside `parts/` and not inside it, and every
    part leaning on that idea carries *The source behind it*. A subtopic about a tool, a command
    or a repository convention has no source; **do not manufacture one**.
12. **Every day gets at least one part whose subject is a deliberate failure** — break it on
    purpose, read the real error, fix it. That part declares `failure: true` in its frontmatter
    and is usually `level: production`. `{{DRIVER}} depth` fails the day without one.
13. Assign each part a `level` — `foundation`, `working`, `production`. A day climbs. A day that
    is all `foundation` is a tutorial; a day opening at `production` has skipped the reader.
14. Apply the **one-idea test**, the **standalone test** and the **no-shortcut test** to every
    planned part *before* writing it.
15. **Choose one metaphor family for the whole day.** Two parts reaching for the same family read
    as one idea repeated; two parts reaching for unrelated exotic families read as noise.
16. **Print the planned part list before writing.** If it looks thin, the user will say so, and
    that conversation is cheap now and expensive after twenty documents exist.

## Step 4 — write the parts

Path: `days/day-NN-<day-slug>/parts/<NN>-<section-slug>/<section>.<subtopic>-<slug>.md`

17. **Name the day folder `day-NN-<slug>`** — the number zero-padded, then a kebab-case slug of
    1–4 words from the hub's `title` with articles dropped. A number alone is an address, not an
    answer. A bare `days/day-NN/` is rejected by `{{DRIVER}} depth`.
18. **One folder per section**: two digits, then a kebab-case slug of 1–3 words saying what the
    section is about, taken from its heading in the hub's map. Every part lives inside its
    section's folder; none is ever loose in `parts/`, and the folder number must match the number
    before the dot.
19. **Links are relative to the part's own folder**: a sibling is `1.2-<slug>.md`, another section
    is `../01-<slug>/1.5-<slug>.md`, the hub is `../../LESSON.md`. `prev` and `next` use the same
    form. The hub's map links from the day folder: `parts/01-<slug>/1.1-<slug>.md`.
20. Every part carries **all eleven sections of §11.4, in order**. Three are conditional — *The
    source behind it*, *Line by line*, *The source in one demo* — each required exactly when its
    trigger is present and never otherwise. Start from `days/_TEMPLATES/PART.md`.
21. **The story is the section that gets written badly.** Four rules, and the first is the one
    that gets broken:
    1. **A scene the reader has plausibly lived.** A parcel and a courier, a repair-shop job card,
       a bus route map, a used car checked by a mechanic, a monthly generator test. **Not** a
       nautical chart, a model railway, a theatre programme, a projection booth. Test: *could the
       reader have been standing in this scene themselves?* If they must first be told what the
       setting **is**, the analogy is carrying the explanation instead of hooking it.
    2. **Simple words.** If a twelve-year-old could not follow the first sentence, rewrite it.
    3. **Load-bearing.** The scene contains the actual failure or decision the part teaches, and
       every later section that reaches back for it must still fit.
    4. **No metaphor collision inside a day.** Grep the day's other parts before choosing.
22. **`In production` is not optional and is not a paragraph of encouragement.** What a
    professional writes instead of the teaching version · what degrades at scale or under pressure
    · the failure that only shows with real traffic · the review comment · the interview question.
23. **`When it breaks` carries the real error text, verbatim.** If you have not seen the error,
    cause it. A reconstructed traceback is a fabricated result (Principle 7).
24. **Every code block is followed by `**Line by line:**`** — every non-obvious token, and why
    that line and not another.
25. A diagram whenever the concept is spatial, sequential or a state machine.

## Step 5 — write the sources last, and say they are read last

26. Path: `days/day-NN-<slug>/sources/NN-<source-slug>.md`, numbered from `01` with no gaps.
    Start from `days/_TEMPLATES/SOURCE.md`. Frontmatter is a part's **minus `part`** and **plus
    `source:`** (one identifier). Links run one level up: a part is
    `../parts/01-<slug>/1.1-<slug>.md`, the hub is `../LESSON.md`.
27. They are *read* after the parts too — the hub's map says so and the last part's *Next* points
    at them. That order is Principle 3 at the scale of a day: build the mechanism by hand, then
    read the proposal, so "what survived and what did not" lands on something the reader built.
28. **The demo is the section that makes a source document worth reading.** Only that source's
    contribution · end to end and actually runnable, with **real pasted output** (a `TODO` naming
    the exact command if it has not been run — **never an invented transcript**) · **an ablation
    switch** with both runs shown · inside the project's constraints.

## Step 6 — write the hub

29. `days/day-NN-<slug>/LESSON.md`, from `days/_TEMPLATES/LESSON.md`. **The hub never teaches** —
    no `**Line by line:**` anywhere in it. Eleven numbered sections in order (§11.5), ending at
    §11 Ledger & commit with the verbatim rows to paste and the commit message.
30. `frontmatter.parts` must equal the number of documents actually in `parts/`. The checker
    compares them.

## Step 7 — write the checklist

31. `days/day-NN-<slug>/CHECKLIST.md`, from `days/_TEMPLATES/CHECKLIST.md`: one box per part
    document (read it · run its check · answer its question out loud), one per source document,
    the build-brief boxes, **at least one "break it, watch it go red, fix it"**, the ledger rows,
    and the commit box. No time estimates.

## Step 8 — verify

32. Run `{{DRIVER}} depth $ARGUMENTS`. **Fix every failure; never hand-wave past one.**
33. Run `{{DRIVER}} index`, then `{{DRIVER}} check`.
34. Finish by printing: the IDs closed, the part count, the day's check command, the budget, and
    the live pages you actually fetched.

---

## Always

- Honour `CLAUDE.md`: doc-first · build-first-compare-after · never invent a fact · at least one
  check that can go red · every command inside the plan's §4 constraints.
- **Grammar and punctuation are part of the deliverable, in every section — not just the story.**
  Full stops and commas where they belong, no run-on sentences, and no long chain of dashes where
  two ordinary sentences would read better. A sentence the reader has to parse twice has failed.
- **Do not solve the `TODO(me)` sections, and do not do the learner's work.** Teach; don't do the
  reps. The exception is a source document's demo, which is given complete because it is teaching
  material rather than an exercise.
- **Never name a person, instructor, author, channel, academy, bootcamp or training company** —
  not in a lesson, a checklist, a docstring or a commit message. Tool and library names are
  required and unaffected, as is citing a specification by its revision and a work by its exact
  title and identifier.
- The eight failure modes this format exists to prevent (§11.8): splitting without deepening ·
  summary in place of explanation · **stopping at the toy example** · assuming the previous day ·
  code without failure · **trimming to fit** · solved reps · a carried-over clock. If a part
  gained no story, no mechanism, no real failure text and no production section, it is not done.
````

---

# Part 3 — finishing, and the other verbs

## Step 5 · Verify, and do not skip this

```bash
python granth.py doctor      # config, plan markers, ledgers, day map, duplicate IDs
python granth.py index       # generate TRACEABILITY, CURRICULUM_INDEX, TRACKER, WIKI, wiki/
python granth.py status      # should say: 0 of N days complete. Next: day <first>.
python granth.py brief <first>      # prints the assignment, exits 0
python granth.py brief <first + 5>  # prints STOP and exits non-zero — proves the guard works
python granth.py depth       # "no written days yet" is the correct answer at this point
```

Then confirm nothing was left half-substituted:

```bash
grep -rn "{{" --include="*.md" --include="*.toml" .
```

It should find nothing — the day templates get substituted too. Fix everything `doctor` reports
**before showing the user anything.** A scaffold that fails its own checks on the first run
teaches the user to ignore the checks.

## Step 6 · Report

Briefly:

1. What was created — the tree, one line per top-level entry.
2. The curriculum in three numbers: days, phases, IDs.
3. The **exact next command**: `python granth.py brief <first>`, then `/day-<slug> <first>`.
4. Anything you could not verify and left as a `TODO` — with the lookup command in it.
5. Anything you decided yourself that they might want to change, and where it lives.

**Do not commit** unless asked. The first commit of a curriculum repository is a decision, and it
is theirs.

---

## Writing a day

**The repository has its own day skill**, written at `.claude/skills/day-<slug>/SKILL.md` by
`initiate`, so the repository is self-contained for anyone who clones it without granth installed.

1. Run `python granth.py brief N`. **If it exits non-zero, stop and report why.** The order guard
   is not advisory: skipping, merging or reordering a day needs an ADR, written first.
2. Read that repository's `.claude/skills/day-<slug>/SKILL.md` and follow it.
3. If it is missing — a hand-made repository, or one scaffolded before that step existed — write
   it from the body in Part 2, offer it to the user, then follow it.

Never write a day from this file's summary. The project skill and the plan's §11 are the standard;
a paraphrase of them is how a curriculum drifts.

---

## adr

Use when a decision would make someone ask, six months from now, *"why on earth is it like this?"*
If they would not notice, it does not need one.

1. **Find the next number.** `ls docs/adr/` — numbers are never reused and never renumbered.
2. **Copy `docs/adr/ADR-0000-template.md`.** Every section is required.
3. **Write *Context* with real specifics** — the tree as it stands, the error as it reads, the
   number as it was measured. If the problem compounds, say by how much and over what. A reader in
   six months has none of today's context, and this section is the only place they can get it.
4. **Write *Options considered* with the status quo in it.** "Do nothing" is a real option, and
   rejecting it is a real decision. An ADR with one option is a justification written after the
   fact.
5. **Write *Consequences* including what is now worse.** A decision with no cost was not a
   decision; it was a preference.
6. **Add the row to `docs/adr/README.md`**, and a `CHANGELOG_PLAN.md` entry if plan text changed.

**Superseding.** A decision that turns out wrong is superseded, **never edited**: write the new
ADR, set the old one's `Status:` to `superseded by ADR-NNNN`, change nothing else in it. That one
line is the whole value of the practice — an ADR set you can edit always looks like it was right
from the start, and teaches nothing.

**Not an ADR:** a version bump (`PINS.md`), a wording change (`CHANGELOG_PLAN.md`), a decision
inside one day (the day document), or a shipped decision written up afterwards to look deliberate.

**The one people get wrong:** skipping, merging, inserting or reordering a day **needs an ADR**,
and this is the rule most often broken because it is always locally reasonable. What it costs: the
day map stops matching the folders, `brief` guards an order that no longer exists, traceability
reports IDs against days that moved, and every "on day 20 we will…" in every earlier day is off by
one. The ADR is what makes you notice the cost before paying it.

## amend

Use when reality moved: a version, a renamed interface, a changed limit, a superseded
specification, a tool that no longer exists.

1. **Establish what actually moved.** Fetch the source live. An amendment written from a
   recollection of a change is two guesses stacked.
2. **State the cost before the fix.** Which days are affected? Which IDs move? What has to be
   rewritten, and what merely re-checked? An entry naming the change but not its cost is a note.
3. **Decide whether it is structural.** If the shape of the work changes — day format, ID scheme,
   phase boundaries, toolchain, scope — write the ADR first.
4. **Edit the plan.** Bump its version: patch for a correction, minor for an added rule, major for
   a changed contract. Update the plan's `version:` frontmatter, `plan_version` in `granth.toml`,
   and the plan's §13 amendment record.
5. **Append the changelog entry**, linking the ADR if there is one.
6. **Only then** touch days or work.

> Principle 8 exists because the alternative is invisible. A day quietly patched around a moved
> API leaves no trace that the API moved; six days later someone hits the same wall and works
> around it differently, and the curriculum now contradicts itself in two places with no record.

**Note the version-bump cost.** Every hub carries `plan_version`, and `depth` fails a day whose
value does not match `granth.toml`. That is deliberate — a bump is meant to be visible. When you
bump, either update every written hub in the same commit, or do not bump: a wording fix is not a
version.

## audit

For an existing curriculum repository, granth-made or not. **Report findings; change nothing**
unless asked.

```bash
python granth.py doctor && python granth.py depth && python granth.py index --check && python granth.py status
```

Then read for what a script cannot see, in this order of value:

1. **Are the stories scenes the reader has plausibly lived?** The most-broken rule in the contract.
   A nautical chart, a model railway, a theatre programme: if the reader must first be told what
   the setting *is*, the analogy is carrying the explanation instead of hooking it.
2. **Does every part have a real `In production` section?** The one most often dropped, and
   dropping it halves the document.
3. **Is `When it breaks` carrying real, pasted error text** — or a plausible reconstruction? A
   reconstructed traceback is a fabricated result.
4. **Does each day climb?** All-`foundation` is a tutorial. Opening at `production` skipped the
   reader.
5. **Is anything defined twice, slightly differently?** Cross-check `docs/GLOSSARY.md`.
6. **Do the ledgers record failures as well as successes?** A ledger with no bad days in it is a
   ledger nobody has been honest in.

Report as: what is green, what is broken with file and line, and the three things worth fixing
first. Do not list forty nits.

## doctor

Run `python granth.py doctor`. It checks wiring only: config present, plan markers intact, ledgers
there, no ID assigned to two days. Run it before blaming a day for a tool's failure.

Common causes, if it or another command misbehaves:

| Symptom | Cause |
| --- | --- |
| `the plan carries no <!-- granth:day-map:start --> block` | The markers were deleted or renamed. Put them back around the day tables. |
| `needs Python 3.11 or newer` | `tomllib` is stdlib from 3.11. Upgrade, or run a newer interpreter explicitly. |
| `index --check` fails right after `index` | Something rewrote a generated file — usually an editor plugin or a formatter. |
| `plan_version ... but granth.toml says ...` | The plan was bumped without updating written hubs. Update them, or revert the bump. |
| A day passes `depth` but reads badly | Working as designed. The checker is a floor, not a standard. Run `audit`. |

---

## Always

- **Verify live, or leave the command.** Every version, interface and citation the plan names.
  Cite by title and identifier, **never by author**.
- **No clocks, anywhere.** Not in the plan, not in a day, not in a checklist, not in an estimate
  you volunteer in chat.
- **No person names, no course or creator brand names** in any generated document — not in a
  lesson, a checklist, a docstring or a commit message. Tool and library names are required and
  unaffected, as is citing a specification by its revision and a work by its exact title and
  identifier.
- **Copy `granth.py` verbatim.** It is tested; a rewritten-from-memory checker is a checker that
  passes everything.
- **Four ledgers are written by hand and five are generated.** `PROGRESS`, `PINS`, `SOURCES`,
  `GLOSSARY`, `PROVENANCE` and `CHANGELOG_PLAN` are append-only history; `TRACEABILITY`,
  `CURRICULUM_INDEX`, `TRACKER`, `WIKI` and `wiki/` are outputs. Editing a generated file only
  means the next `index` silently overwrites you. **If an index disagrees with the day it indexes,
  the day is right and the index is stale.**
- **Nothing is deleted from an append-only ledger.** A day that went wrong gets a note saying what
  went wrong, not a quiet correction. A ledger recording only successes teaches nothing.
- **Do not commit** unless asked.
- **Do not do the learner's reps.** `TODO(me)` markers are left unsolved. The one exception is a
  source document's demo, which is given complete because it is teaching material.
- **Say what you could not verify.** A `TODO` carrying the exact lookup command is a finished
  deliverable. A plausible guess is not.
