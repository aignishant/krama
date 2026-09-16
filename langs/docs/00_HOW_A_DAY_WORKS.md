# How a Krama Languages day works

This is the format contract. Every one of the 540 lessons follows it.

---

## Who this is written for

Someone who has **never programmed before** on day 1, and who by day 180 can build,
ship, and defend a production service in Python, Go, or C++, and pick between them with
a reason.

That single fact decides everything below.

---

## The prime directive

> **Every lesson teaches one idea in one language, shows how the other two do it, and
> leaves you able to build it and explain it out loud, from memory, to a stranger.**

The course is three languages side by side on purpose. The differences are the lesson.
A reader who learns pointers in C++ on the same day they learn that Python has none and
Go has them but hides the arithmetic will understand pointers better than anyone who
learned them in one language alone.

---

## The shape of a day

```
days/day-NNN-<theme>/
    README.md                     the hub — today in one screen
    01-python-<topic>.md          the Python lesson
    02-go-<topic>.md              the Go lesson
    03-cpp-<topic>.md             the C++ lesson
    04-practice.md                three exercises, built three times, then said out loud
```

Five files. Nothing else. No `lab/`, no harness, no starter code folder. Code lives
inside the lessons, complete and runnable.

All three tracks run every day, from day 1 to day 180. Every day has one **theme**
(say, "closures") and each lesson teaches that theme in its own language. When a
language does not have the feature, the lesson says so plainly and teaches the nearest
thing it does have. "Go has no inheritance; here is embedding, and here is why they
chose that" is a lesson. Skipping the day for Go is not.

### The four kinds of day

| Days | Kind | What changes |
|---|---|---|
| 1-15 | Foundations | Every basic, in all three. Short programs. After day 15 you can build a small tool in any of them. |
| 16-45 | Advanced features | The features that make each language itself. Interfaces, generics, closures, concurrency, memory. |
| 46-135 | Applied | Networking, data, Protocol Buffers and gRPC, performance, messaging, and design. Go carries the protobuf and gRPC block; Python and C++ are its clients. |
| 136-180 | Builds and capstone | Six five-day builds, interview prep, and an eight-day capstone. The lessons become walkthroughs and the practice sheet becomes the deliverable. |

Project days are listed in `PROJECTS` in [`../scripts/curriculum.py`](../scripts/curriculum.py).

---

## The nine sections

Every lesson carries all nine, in this order.

| # | Section |
|---:|---|
| 1 | What this is, and why it matters |
| 2 | The story |
| 3 | The idea in plain English |
| 4 | The picture |
| 5 | The code, built step by step |
| 6 | How the other two languages do it |
| 7 | The traps |
| 8 | Say it out loud |
| 9 | Recall card |

### 1. What this is, and why it matters

Three sentences saying what the idea is, then one short paragraph on where you meet it
at work and how an interviewer asks about it. No build-up. The reader should know what
they are learning by the end of the first line.

### 2. The story

A scene from ordinary life, 200-400 words, with a person in it, where this idea already
exists without anyone calling it by its technical name. A queue at a canteen. Laying
tables for a wedding. Handing a house key to a neighbour.

**Pick a scene almost anyone has lived.** If the scene only works for someone who has
run a particular kind of shop, it is the wrong scene.

**Simple words, and realistic detail.** Short sentences. Real numbers, real times of day,
and the small true details that make a scene rather than an example.

**No jargon. No code. No technical vocabulary at all.** Not one word.

**No paper props.** If the person has to store something, they save it in their phone.

The three lessons of one day may share a story, or each carry their own. Sharing is
better when the theme is the same idea in three coats; separate stories are better when
the languages genuinely disagree.

### 3. The idea in plain English

Take the story apart and map each piece onto the technical idea, one step at a time.
This is where the technical words are introduced, each one defined the first time it
appears, in a sentence a fifteen-year-old could read.

Concrete before abstract, always. A seven-element list before "a list of size n".

### 4. The picture

At least one diagram, captioned with what to notice in it.

- **ASCII boxes** for memory, stacks, bytes, pointers, and layouts. Addresses or indices
  above, values below.
- **Mermaid** for request flows, state machines, goroutine and thread diagrams,
  architectures.

### 5. The code, built step by step

Small fragments, **ten lines or fewer**, each followed by prose explaining what it does
and why. Never a forty-line block with a comment on top.

Then the complete, working, copy-pasteable program at the end of the section, with the
exact command that runs it and the exact output it prints.

- Python 3.12+, type hints on every public signature.
- Go 1.23+, `gofmt` formatting, errors handled, never `_` for an error.
- C++20, compiled with `-Wall -Wextra -std=c++20`, no raw `new` unless the day is about it.

**Show the whole program.** This course does not hide answers.

### 6. How the other two languages do it

This section is the reason the course exists. A short side-by-side, never more than a
screen: the same idea in the other two languages, in code, followed by **the one line of
difference that matters**. Not a feature comparison. The one thing that will bite the
reader when they switch.

A table is fine. Three columns, one row per aspect, each cell one short phrase.

### 7. The traps

At least two:

- **The near-miss** — the version that looks correct, and the exact input that kills it.
- **The real error** — actual pasted output, never a paraphrase. `panic: runtime error:
  index out of range [3] with length 3`, not "you get a panic".

Compiler errors count. Paste the compiler's exact words.

### 8. Say it out loud

The section the whole document exists for.

- **How it gets asked** — two or three real phrasings.
- **What to say out loud** — a script for the first ninety seconds.
- **The follow-ups** — the three questions that come next, with short answers.
- **A model answer** — what a strong candidate actually says, written out.

### 9. Recall card

Five lines, maximum. What survives if you forget everything else.

---

## The practice sheet

`04-practice.md` carries three exercises, easiest first, each with one line on what it is
really testing. Every exercise is built **three times**, once per language. Then a
**Compare** section, one sentence per language on what was easy and what was hard. Then
three questions to answer out loud.

On a project day the practice sheet is the deliverable: the requirements, the file
layout, the commands, and what "done" looks like.

---

## Writing rules

- **Second person, present tense.** "You keep a pointer." Never "we will now consider".
- **Short sentences, one idea each.** The subject is hard; the prose must not be.
- **Define every term the first time it appears.** If a word has not been defined in
  this lesson or an earlier day, define it here or do not use it.
- **No cheerleading.** No "Great!", no emoji in the body.
- **Admit difficulty.** "This is the step people get wrong, and here is why it looks
  right" is worth more than confidence.
- **No study-time estimates.** A day is a unit of subject, not of hours.
- **No paper.** Say it out loud from memory, or draw it in any tool you like.
- **British/Indian-neutral English**, consistent within a file.
- **Real output.** Every program shows what it prints. Every error is pasted, not described.
