---
name: day-langs
description: Write the languages half of a Krama day — the Python lesson, the Go lesson and the C++ lesson (files 05-07 in days/day-NNN-*/) plus their exercises in the practice sheet, all under the nine-section format contract. Use this skill whenever the user asks to write, fix or review only the language lessons of a day ("langs for day 12", "write the pointers lessons", "do the gRPC streaming day", "the Go lesson on day 30 is thin"), asks for a Python/Go/C++ lesson, or asks about protobuf or gRPC lessons. day-krama hands off to this skill for the languages half of a whole day.
---

# Writing the languages half of a Krama day

You are producing the languages half of one day of a 180-day course. The reader is a
**complete beginner** on day 1, and by day 180 can build and ship services in Python,
Go, and C++. They read only these documents. If an idea is not in them, they never meet
it.

Every day's languages half is **three lessons**, one per language, on one theme —
`05-lang-python-*.md`, `06-lang-go-*.md`, `07-lang-cpp-*.md` in `days/day-NNN-*/` —
plus the language exercises in the practice sheet. You write all of them. Never one or
two. The interview half of the same day (files 01-03) is written by `/day-krama`, which
calls this skill for the languages half; a day is complete only when both halves are.

**Read first, every time:** [`docs/00_HOW_A_DAY_WORKS.md`](../../../docs/00_HOW_A_DAY_WORKS.md)
and [`CLAUDE.md`](../../../CLAUDE.md).

All commands below run from the repository root.

---

## The procedure

### Step 1 · Read the assignment

```bash
./k next          # must name N, and lists which of N's files are still to write
./k day N
```

The hub's **Languages** rows name the theme, the three lesson titles, the "after today
you can" line, and the interviewer question. That is your brief. The syllabus decided
it, not you. Do not change the topic. If it is genuinely wrong, stop and say so; the fix
is an edit to `scripts/syllabus/langs/*.py` in its own commit, then `./k build`.

### Step 2 · Check what the reader already knows

```bash
cat wiki/00-STATE.md                          # which lessons are written, per track
cat wiki/vocab.md                             # every term the reader knows, and its day
cat wiki/recall/languages-<phase>.md          # the recall cards for this day's languages phase
```

`./k day N` names the languages phase; take the slug from there. You may use any term
in `wiki/vocab.md` and any idea in that recall file. You may **not** use a term the
course has not yet met, unless you define it on the spot. The single most common failure
is writing for someone who already knows the subject.

On day 1 the reader knows nothing. Not what a file is, not what a terminal is. The DSA
lessons of the same day teach in Python, so a term the DSA track has defined by day N
is fair game — `wiki/vocab.md` lists those too.

### Step 3 · Write the three lessons

Nine sections each, in order, no exceptions:

1. **What this is, and why it matters** — three sentences, then where it shows up at work and in interviews.
2. **The story** — 200-400 words, a person, a scene almost anyone has lived, **zero technical words**. No paper props. The three lessons may share one story if the theme is the same idea in three coats.
3. **The idea in plain English** — map the story onto the idea, defining every term.
4. **The picture** — ASCII for memory and bytes, Mermaid for flows. Captioned.
5. **The code, built step by step** — fragments of ten lines or fewer, each explained, then the **complete program** with its run command and exact output.
6. **How the other two languages do it** — real code from the other two, then **the one line of difference that matters**. This is the section that makes this course different. Never a bullet list of feature names.
7. **The traps** — the near-miss that looks right plus the input that kills it, and **real pasted error text** (compiler errors count).
8. **Say it out loud** — real phrasings, a ninety-second script, three follow-ups with answers, a written-out model answer.
9. **Recall card** — five lines, maximum.

Language versions: Python 3.12+, Go 1.23+, C++20. If a language does not have today's
feature, the lesson says so in section 1 and teaches the nearest thing it does have.

**Never invent a library API.** If you are not sure a function exists with that
signature, look it up before writing it. This matters most on the protobuf, gRPC, and
third-party-library days (46-105).

### Step 4 · Write the language exercises

They go in the practice sheet, under **Build these, in all three languages**: three
exercises, easiest first, each with one line on what it is really testing, each built
three times. A **Compare** section, one sentence per language. The languages question
goes in the sheet's **Say these out loud** section, under its Languages heading. On a
project day this part is the deliverable: requirements, file layout, commands, and what
done looks like.

Which file: `03-practice.md` on a day that has been folded into the single sheet, and
`08-lang-practice.md` on a day that has not. `practice_name(day)` in
`scripts/build_skeleton.py` is the authority. Never create an `08-` file on a folded day.

### Step 5 · Check

```bash
./k check N
./k wiki
```

Fix everything it reports. Then `./k status` to confirm the day counts as complete —
it will not, if the interview half is still unwritten; that is `/day-krama`'s job.

---

## Writing rules that get broken most

- **Section 2 with a technical word in it.** "She opened the file" is a technical word. "She opened the drawer" is not.
- **Section 5 without the output.** Every complete program shows what it prints.
- **Section 6 as a feature list.** It must be code, then the one difference that bites.
- **Section 7 paraphrasing an error.** Paste it.
- **Using a term the reader has not met.** Define it or drop it.
- **Any mention of paper.** Rule 15.
- **Any reading-time estimate.** Rule 12.
