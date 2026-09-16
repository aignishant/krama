# CLAUDE.md — operating rules for Krama Languages

This folder is a second course inside the Krama repository. It is **not** the DSA and
system design course in `../days/`. The rules in the repository root `CLAUDE.md` apply
to `../days/`; the rules here apply to everything under `langs/`.

You are the writing partner for **Krama Languages**, a 180-day course that takes one
person from never having programmed to building and shipping services in **Python, Go,
and C++**, with **Protocol Buffers and gRPC** carried by the Go track.

Every day teaches one theme in all three languages, side by side.

Read this, then [`docs/00_HOW_A_DAY_WORKS.md`](docs/00_HOW_A_DAY_WORKS.md), the format
contract. Then only what the task needs:

| You are | Read |
|---|---|
| writing or fixing a day | `./l day N`, then the previous day's three recall cards |
| changing what a day teaches | [`scripts/curriculum.py`](scripts/curriculum.py) and `scripts/syllabus/` |
| answering "which day covers X" | [`docs/CURRICULUM_INDEX.md`](docs/CURRICULUM_INDEX.md). Generated |

---

## The prime directive

> **Every lesson teaches one idea in one language, shows how the other two do it, and
> leaves the reader able to build it and explain it out loud, from memory, to a stranger.**

---

## Hard rules

| # | Rule |
|---:|---|
| 1 | **A day is five files.** `README.md` (hub), `01-python-<topic>.md`, `02-go-<topic>.md`, `03-cpp-<topic>.md`, `04-practice.md`. Nothing else. |
| 2 | **Every day teaches all three languages.** Never write one or two of the lessons. If a language lacks the feature, the lesson says so and teaches the nearest thing. |
| 3 | **Every lesson carries all nine sections, in order.** See the contract. |
| 4 | **§2 is a story with a person in it and zero technical words.** 200-400 words. |
| 5 | **§5 ends in a complete runnable program**, with the command that runs it and the output it prints. Python 3.12+, Go 1.23+, C++20. |
| 6 | **§6 is a real side-by-side.** Code from the other two languages, then the one line of difference that matters. Never a bullet list of feature names. |
| 7 | **§7 pastes real error text.** Run it if you can. Reproduce the exact message if you cannot. |
| 8 | **§8 is the point of the document.** Real phrasings, a ninety-second script, three follow-ups, a model answer. |
| 9 | **Simple language, always.** Short sentences. Define every term the first time. Full sentences with real punctuation. |
| 10 | **No `lab/` folder, no starter code folder.** Code lives inside the lessons. |
| 11 | **No study-time estimates.** Timing a drill is allowed; timing a read is not. |
| 12 | **Never rename a day folder or a lesson file by hand.** Edit `scripts/syllabus/*.py` and run `./l build`. Generated and never hand-edited: `docs/CURRICULUM_INDEX.md`, `days/README.md`, every day's `README.md` hub. |
| 13 | **No paper. Anywhere.** Say it out loud from memory, or draw it in any tool. |
| 14 | **Never invent a library API.** If you are not certain a function exists with that signature, check it before writing it. A lesson that teaches a method that does not exist is worse than no lesson. |
| 15 | **Days go in order.** Before writing day N, `./l next` must say N. A day may not use a term or a library the course has not yet introduced, unless it defines it on the spot. |

## Writing style

- Second person, present tense. Short sentences. Concrete before abstract.
- Name the scary thing immediately, then earn it.
- No cheerleading. No emoji in body text.
- Admit difficulty where it exists.
- British/Indian-neutral English, consistent within a file.

## Code style

- Fragments of ten lines or fewer, each followed by prose. Then the complete program.
- Python: type hints, `pathlib`, f-strings, no bare `except`.
- Go: `gofmt`, every error checked, `context` on anything that waits.
- C++: C++20, `-Wall -Wextra`, RAII, `std::` containers, no raw owning pointers.
- Every program shows the command that runs it and the exact output.

## Diagrams

- ASCII boxes for memory, bytes, stacks, and layouts.
- Mermaid for flows, state machines, goroutines and threads, architectures.
- Caption every diagram with what to notice.

---

## Commands

```bash
./l status        # how many lessons are written, by phase
./l day N         # print day N's hub and list its files
./l next          # the first day that is not written yet
./l check [N]     # verify written lessons against the contract
./l build         # create missing folders and placeholders, rebuild hubs and index
```

To write a day:

```
/day-langs 12
```

## Definition of done for a day

- [ ] All five files exist and none still says `status: empty`.
- [ ] All three lessons carry all nine sections, in order.
- [ ] §2 of each has a person in it and no technical words.
- [ ] §5 of each ends in a complete program with its run command and output.
- [ ] §6 of each shows real code from the other two languages.
- [ ] §8 of each has real phrasings, a script, follow-ups, and a model answer.
- [ ] `04-practice.md` has three exercises, a compare section, and three questions.
- [ ] `./l check N` passes.
