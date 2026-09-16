# Krama

**180 days. DSA, system design, and three languages, side by side. One goal: crack a
product-company interview — and be able to build what you designed.**

Every day teaches one DSA topic and one system design topic, and one languages theme
three times over: in Python, in Go, and in C++. You do all of it, every day, for six
months. At the end you can answer either kind of interview question out loud, to a
stranger, without notes, and you have shipped ten projects in three languages — the
last of them an order platform with a Python gateway, Go services talking over gRPC
with Protocol Buffers, and a C++ pricing engine.

Written for someone starting from **zero**. Not a computer science graduate. Not someone
brushing up. If you need to be told what a server is, you are the reader.

---

## Start here

```bash
./k status        # where you are
./k day 1         # today's hub
```

Then open [`days/day-001-how-your-code-actually-runs/README.md`](days/day-001-how-your-code-actually-runs/README.md).

---

## What a day looks like

```
days/day-001-how-your-code-actually-runs/
    README.md                                        the hub — today in one screen
    01-dsa-how-your-code-actually-runs.md            the DSA lesson
    02-system-design-what-happens-when-you-type.md   the system design lesson
    03-practice.md                                   problems to code, exercises to build, questions to say aloud
    05-lang-python-python3-a-file-and.md             the Python lesson on today's theme
    06-lang-go-go-run-go-build.md                    the Go lesson on the same theme
    07-lang-cpp-g-a-file-and.md                      the C++ lesson on the same theme
```

Seven files. No lab folder, no test harness, no setup. You read, you code along, you
run the programs, you say the answers out loud. A day has two halves — the interview
half (01, 02) and the languages half (05, 06, 07) — and one practice sheet that serves
both. A day is complete when both halves are done.

**Twelve of the 180 days also carry** `04-cpp-<topic>.md`, the optional C++ contest
lesson — the STL you need to solve that day's DSA problem in C++.

> The languages course used to be a separate folder with its own practice sheet. That
> sheet is being folded into `03-practice.md` one block of days at a time; a day not
> folded yet still has an `08-lang-practice.md`. It reads the same either way.

Each lesson has the same nine sections, so you learn one reading rhythm and keep it
for six months:

| # | DSA lesson | System design lesson | Language lesson |
|---:|---|---|---|
| 1 | What this is, and why they ask it | What this is, and why they ask it | What this is, and why it matters |
| 2 | The story | The story | The story |
| 3 | The idea in plain English | The idea in plain English | The idea in plain English |
| 4 | The picture | The picture | The picture |
| 5 | The code, built step by step | How it actually works | The code, built step by step |
| 6 | What it costs | The numbers | How the other two languages do it |
| 7 | The traps | The trade-offs | The traps |
| 8 | **In the interview** | **In the interview** | **Say it out loud** |
| 9 | Recall card | Recall card | Recall card |

Section 2 is a scene from ordinary life with no technical words in it. Section 8 is what
the whole document exists for: the real phrasings, what to say in the first ninety
seconds, the follow-ups, and a model answer.

---

## The tracks

**DSA** — foundations and Big-O, then arrays, strings, two pointers, sliding window,
prefix sums, binary search, sorting, hashing, stacks and queues, linked lists, recursion
and backtracking, trees, heaps, tries, graphs, dynamic programming, greedy, bits and
maths, then mocks.

**System design** — how computers and the internet work, then APIs, databases,
object-oriented design, SOLID, design patterns, twenty low-level design case studies,
scaling, distributed systems, the building blocks of big systems, twenty-six high-level
design case studies, then reliability and the interview itself.

The system design track is deliberately ordered **fundamentals and LLD first, HLD second**.
Low-level design is what junior candidates actually get asked, and high-level design makes
no sense until you know what a database index and a message queue are.

**Languages — Python, Go, and C++, every day.** One theme a day, taught three times, so
the differences become the lesson. Days 1-15 are every basic in every language; 16-45
the features that make each language itself; 46-135 networking, data, Protocol Buffers
and gRPC (which Go carries), performance, messaging, and design; 136-180 six five-day
builds, interview prep, and an eight-day capstone. Ten projects along the way, listed in
`LANG_PROJECTS` in [`scripts/curriculum.py`](scripts/curriculum.py).

**C++ for contests — optional, and twelve days long.** The DSA track teaches in Python,
because Python gets a beginner to a working solution fastest. The contest track is for
people who also want to compete, where the time limits are set for C++, or who will be
interviewed in it. Each lesson sits on the day the course first needs that piece of the
STL:

| Day | C++ lesson |
|---:|---|
| [001](days/day-001-how-your-code-actually-runs/04-cpp-compiling-and-running.md) | Compiling and running your first program |
| [002](days/day-002-counting-steps/04-cpp-types-numbers.md) | Types, numbers, and the overflow that costs contests |
| [003](days/day-003-big-o-in-plain-english/04-cpp-input-output.md) | Input, output, and the competitive template |
| [005](days/day-005-python-lists-and-tuples/04-cpp-vector-references.md) | `vector`, references, and the array you use for everything |
| [006](days/day-006-python-strings-dicts-sets/04-cpp-string-map-set.md) | `string`, `map`, `set`, and `pair` |
| [042](days/day-042-binary-search-idea/04-cpp-sort-lambdas.md) | `sort`, lambdas, and `lower_bound` |
| [068](days/day-068-stacks/04-cpp-stack-queue-deque.md) | `stack`, `queue`, `deque`, and `priority_queue` |
| [078](days/day-078-nodes-and-links/04-cpp-structs-pointers.md) | structs, pointers, and building your own nodes |
| [125](days/day-125-what-a-graph-is/04-cpp-graphs-and-recursion.md) | Graphs and recursion: adjacency lists, depth, and DSU |
| [143](days/day-143-what-dp-is/04-cpp-dp-tables.md) | DP tables, and the contest traps that are left |
| [171](days/day-171-binary-and-bits/04-cpp-shifts-builtins.md) | Shifts, builtins, and `bitset` |
| [178](days/day-178-thinking-out-loud/04-cpp-stress-testing.md) | Stress testing, and reading a judge's verdict |

Five of them land in the first six days, which is enough to start solving the course's
problems in C++ as well as Python. The rest arrive with the structure that needs them. The days that carry one are listed in `CPP_DAYS` in
[`scripts/curriculum.py`](scripts/curriculum.py) — edit that and run `./k build` to change
which.

Full syllabus: [`docs/CURRICULUM_INDEX.md`](docs/CURRICULUM_INDEX.md) ·
Every day at a glance: [`days/README.md`](days/README.md)

---

## Commands

```bash
./k status        progress on every track, computed from disk
./k day N         print day N's hub and list its files
./k next          the first day not complete, and which of its files are still to write
./k check [N]     verify written lessons against the format contract
./k build         create any missing day folders and placeholders
```

To write a day, ask Claude:

```
/day-krama 37        # the whole day
/day-langs 37        # only the languages half
```

---

## How the repo is put together

| Path | What it is |
|---|---|
| [`days/`](days/) | The 180 day folders. Seven files each, eight on the contest days. |
| [`docs/00_HOW_A_DAY_WORKS.md`](docs/00_HOW_A_DAY_WORKS.md) | The format contract every lesson follows. |
| [`docs/CURRICULUM_INDEX.md`](docs/CURRICULUM_INDEX.md) | The syllabus. **Generated** — do not hand-edit. |
| [`scripts/curriculum.py`](scripts/curriculum.py) | The syllabus as data. The source of truth. DSA and system design rows in `scripts/syllabus/`, languages rows in `scripts/syllabus/langs/`. |
| [`scripts/build_skeleton.py`](scripts/build_skeleton.py) | Turns the data into folders and placeholders. |
| [`CLAUDE.md`](CLAUDE.md) | The rules Claude follows when writing a day. |
| [`archive/`](archive/) | The previous 230-day version, kept for reference. |

To change what a day teaches, edit `scripts/curriculum.py` and run
`python scripts/build_skeleton.py`. Never rename a folder by hand.

---

## Progress

`./k status` is the only honest answer; it is computed from disk. All 180 days exist as
folders with their topics, section headings and interview questions already in place, so
you can see the whole road before walking it. The interview half is written for every
day; the languages half is being filled in one day at a time, and a day counts as done
only when both halves are.
