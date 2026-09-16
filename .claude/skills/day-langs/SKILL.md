---
name: day-langs
description: Write a Krama Languages day under langs/ — the Python lesson, the Go lesson, the C++ lesson and the practice sheet, all under the nine-section format contract. Use this skill whenever the user asks to write, generate, draft, expand, rewrite, fix or review any day in langs/days/, mentions a language day number ("langs day 12", "write the pointers day", "do the gRPC streaming day"), asks for a Python/Go/C++ lesson, or asks about protobuf or gRPC lessons. Use it even when phrased casually as "next language day" or "continue the languages course".
---

# Writing a Krama Languages day

You are producing the teaching material for one day of a 180-day course. The reader is
a **complete beginner** on day 1, and by day 180 can build and ship services in Python,
Go, and C++. They read only these documents. If an idea is not in them, they never meet
it.

Every day carries **three lessons**, one per language, on one theme, plus a practice
sheet. You write all four. Never one or two.

**Read first, every time:** [`langs/docs/00_HOW_A_DAY_WORKS.md`](../../../langs/docs/00_HOW_A_DAY_WORKS.md)
and [`langs/CLAUDE.md`](../../../langs/CLAUDE.md).

All commands below run from `langs/`.

---

## The procedure

### Step 1 · Read the assignment

```bash
./l next          # must print N; if it prints a smaller number, write that day instead
./l day N
```

The hub names the theme, the three lesson titles, the "after today you can" line, and
the interviewer question. That is your brief. The syllabus decided it, not you. Do not
change the topic. If it is genuinely wrong, stop and say so; the fix is an edit to
`scripts/syllabus/*.py` in its own commit, then `./l build`.

### Step 2 · Check what the reader already knows

Read the three recall cards (section 9) of day N-1, and skim the hubs of the last five
days. You may use any term those lessons introduced. You may **not** use a term the
course has not yet met, unless you define it on the spot. The single most common failure
is writing for someone who already knows the subject.

On day 1 the reader knows nothing. Not what a file is, not what a terminal is.

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

### Step 4 · Write the practice sheet

Three exercises, easiest first, each with one line on what it is really testing, each
built three times. A **Compare** section, one sentence per language. Three questions
to answer out loud. On a project day the sheet is the deliverable: requirements, file
layout, commands, and what done looks like.

### Step 5 · Check

```bash
./l check N
```

Fix everything it reports. Then `./l status` to confirm the day counts as complete.

---

## Writing rules that get broken most

- **Section 2 with a technical word in it.** "She opened the file" is a technical word. "She opened the drawer" is not.
- **Section 5 without the output.** Every complete program shows what it prints.
- **Section 6 as a feature list.** It must be code, then the one difference that bites.
- **Section 7 paraphrasing an error.** Paste it.
- **Using a term the reader has not met.** Define it or drop it.
- **Any mention of paper.** Rule 13.
- **Any reading-time estimate.** Rule 11.
