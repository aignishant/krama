# How a Krama day works

This is the format contract. Every one of the 900 lessons follows it.

---

## Who this is written for

Someone who has **never studied this before**. Not a computer science graduate.
Not someone brushing up. Someone who has to be told what a server is — and, on the
languages side, someone who has never written a program — and who will be sitting in
a product-company interview at the end of 180 days.

That single fact decides everything below.

---

## The prime directive

> **Every lesson answers one question an interviewer could actually ask,
> and leaves you able to answer it out loud, from memory, to a stranger.**

If a paragraph does not move you toward saying the answer out loud, it does not belong
in the file.

---

## The shape of a day

```
days/day-NNN-<topic>/
    README.md                       the hub — what today is, in one screen
    01-dsa-<topic>.md               the DSA lesson
    02-system-design-<topic>.md     the system design lesson
    03-practice.md                  problems to code, exercises to build, questions to say out loud
    05-lang-python-<topic>.md       the Python lesson on today's languages theme
    06-lang-go-<topic>.md           the Go lesson on the same theme
    07-lang-cpp-<topic>.md          the C++ lesson on the same theme
```

Seven files. Nothing else. No `lab/`, no test harness, no benchmark script, no oracle.

A day has two halves, and both run from day 1 to day 180, so you are never doing only
one of them. A day is **complete** only when both halves are written; `./k status`
counts it that way, and `./k next` will not move on until they are.

**The interview half** is files 01 and 02. The DSA track goes foundations → patterns →
data structures → algorithms. The system design track goes fundamentals → databases →
object-oriented design → low-level design → distributed systems → high-level design.

**The languages half** is files 05, 06 and 07. Every day has one **theme** (say,
"closures"), and each of the three lessons teaches that theme in its own language:
Python, Go, and C++. The same idea three ways, so the differences become the lesson.
When a language does not have the feature, the lesson says so plainly and teaches the
nearest thing it does have. "Go has no inheritance; here is embedding, and here is why
they chose that" is a lesson. Skipping the day for Go is not. Go carries the Protocol
Buffers and gRPC block; Python and C++ are its clients.

**The practice sheet**, `03-practice.md`, serves both halves: the named problems for
the DSA lesson, the three exercises built three times for the language lessons, one
oral drill covering all of today's questions, and one completion checklist.

Every day uses the single `03-practice.md` sheet. Never create a separate language
practice file. A partially authored sheet has `status: draft`: it is preserved by
the builder, including with `--force`, but does not count as finished. Set its
status to `written` only when every track's exercises are complete.

### The languages track, by kind of day

| Days | Kind | What changes |
|---|---|---|
| 1-15 | Foundations | Every basic, in all three. Short programs. After day 15 you can build a small tool in any of them. |
| 16-45 | Advanced features | The features that make each language itself. Interfaces, generics, closures, concurrency, memory. |
| 46-135 | Applied | Networking, data, Protocol Buffers and gRPC, performance, messaging, and design. |
| 136-180 | Builds and capstone | Six five-day builds, interview prep, and an eight-day capstone. The lessons become walkthroughs and the practice sheet becomes the deliverable. |

Project days are listed in `LANG_PROJECTS` in [`../scripts/curriculum.py`](../scripts/curriculum.py).

### The one exception: the C++ contest track

Twelve days out of the hundred and eighty carry an eighth file:

```
    04-cpp-<topic>.md               the C++ contest lesson
```

It is optional and it is deliberately small. The DSA track teaches in Python, because
Python gets a beginner to a working solution fastest. The contest track is for the
reader who also wants to solve DSA problems in C++ — because contest time limits are
set for C++, and because some interviews are in it. It is a different thing from the
languages track's C++ lesson: that one teaches C++ as a language, this one teaches the
STL you need to solve today's problem.

Twelve days, not a hundred and eighty. Five of them land in the first six days, which is
enough to start writing real C++ solutions. The rest sit at the head of the phase that
needs them, so the reader learns `priority_queue` on the day heaps arrive rather than
four months early.

The days that carry one live in `CPP_DAYS` in [`../scripts/curriculum.py`](../scripts/curriculum.py).
A day not listed there is seven files, exactly as above. The contest lesson carries the
same nine sections as a DSA lesson, and is held to the same rules — a story with no
technical words in it, the full compilable solution, the real compiler error pasted,
the arithmetic shown.

---

## The nine sections

Every lesson carries all nine, in this order. All tracks share sections 2-4 and 9, and
the interview and language lessons differ only in the wording of headings 1 and 8, so
you only ever learn one reading rhythm. Sections 5, 6 and 7 are where the tracks differ.

| # | DSA lesson | System design lesson | Language lesson |
|---:|---|---|---|
| 1 | What this is, and why they ask it | What this is, and why they ask it | What this is, and why it matters |
| 2 | The story | The story | The story |
| 3 | The idea in plain English | The idea in plain English | The idea in plain English |
| 4 | The picture | The picture | The picture |
| 5 | The code, built step by step | How it actually works | The code, built step by step |
| 6 | What it costs | The numbers | How the other two languages do it |
| 7 | The traps | The trade-offs | The traps |
| 8 | In the interview | In the interview | Say it out loud |
| 9 | Recall card | Recall card | Recall card |

### 1. What this is, and why they ask it

Three sentences saying what the idea is, then one short paragraph on why this shows up
in interviews. Name the companies or the round type if it is specific. In a language
lesson the heading reads "why it matters", and the paragraph says where you meet the
idea at work as well as in the interview.

No build-up. The reader should know what they are learning by the end of the first line.

### 2. The story

A scene from ordinary life, 200-400 words, with a person in it, where this idea already
exists without anyone calling it by its technical name. Matching socks after the laundry.
A queue at a canteen counter. Laying tables before a wedding.

**Pick a scene almost anyone has lived.** Not a trade the reader has never seen. If the
scene only works for someone who has run a particular kind of shop, or kept a particular
kind of record, it is the wrong scene. The reader should recognise it in the first line.

**Simple words, and realistic detail.** Short sentences. The kind of vocabulary you would
use talking to a friend. Real numbers, real times of day, and the small true details that
make a scene rather than an example — what he is holding when he stops, what time the
shutters went up.

**No jargon. No code. No technical vocabulary at all.** Not one word.

**No paper props.** If the person in the story has to store something, they save it in
their phone. See the writing rules below.

The three language lessons of one day may share a story, or each carry their own.
Sharing is better when the theme is the same idea in three coats; separate stories are
better when the languages genuinely disagree.

The test: if you delete this section and lose nothing, it was decoration, not a story.

### 3. The idea in plain English

Take the story apart and map each piece onto the technical idea, one step at a time.
This is where the technical words are introduced — each one defined the first time it
appears, in a sentence a fifteen-year-old could read.

Concrete before abstract, always. A seven-element array before "an array of size n".
The number 5 before the variable `k`.

### 4. The picture

At least one diagram, captioned with what to notice in it.

- **ASCII boxes** for arrays, memory, pointers, bit patterns — anything where adjacency
  is the point. Indices above, values below, boundaries marked.
- **Mermaid** for trees, graphs, architectures, state machines, request flows, goroutine
  and thread diagrams.

### 5. The code, built step by step *(DSA and languages)*

Small fragments, **ten lines or fewer**, each followed by prose explaining what it does
and why. Never a forty-line block with a comment on top.

Then the complete, working, copy-pasteable solution at the end of the section.

For a DSA lesson: Python 3.12+, type hints on the signature, comments on the lines that
are not obvious.

For a language lesson: the complete program, **with the exact command that runs it and
the exact output it prints**.

- Python 3.12+, type hints on every public signature.
- Go 1.23+, `gofmt` formatting, errors handled, never `_` for an error.
- C++20, compiled with `-Wall -Wextra -std=c++20`, no raw `new` unless the day is about it.

**Show the whole solution.** This repository does not hide answers from you.

### 5. How it actually works *(system design)*

The mechanics. What the component really does, what it stores, what happens on failure,
and which real products work this way. Name them: Redis, Kafka, Postgres, S3, Cassandra.

### 6. What it costs *(DSA)*

Time and space, counted out from the loops in front of you. Show the counting:
"the outer loop runs n times, the inner loop runs n times for each of those, so n × n".

State the space separately, and say whether it is extra space or total space.

### 6. The numbers *(system design)*

The arithmetic, with the multiplication shown. Users → requests per second. Records →
bytes → storage per year. Fan-out multipliers. Replica counts.

"It will be a lot of data" is not an answer. `50M users × 20 posts × 2KB = 2TB` is.

### 6. How the other two languages do it *(languages)*

This section is the reason the languages track exists. A short side-by-side, never more
than a screen: the same idea in the other two languages, in code, followed by **the one
line of difference that matters**. Not a feature comparison. The one thing that will
bite the reader when they switch.

A table is fine. Three columns, one row per aspect, each cell one short phrase.

### 7. The traps *(DSA and languages)*

At least two:

- **The near-miss** — the version that looks correct, and the exact input that kills it.
- **The real error** — actual pasted output, never a paraphrase.
  `IndexError: list index out of range`, not "you get an index error".
  `panic: runtime error: index out of range [3] with length 3`, not "you get a panic".

Compiler errors count. Paste the compiler's exact words.

### 7. The trade-offs *(system design)*

What you give up by choosing this. When you would choose something else instead. The
sentence that begins "I would not use this if..." is the one that separates candidates.

### 8. In the interview *(DSA and system design)* · Say it out loud *(languages)*

The section the whole document exists for. Same content under either heading.

- **How it gets asked** — two or three real phrasings.
- **What to say out loud** — a script for the first ninety seconds.
- **The follow-ups** — the three questions that come next, with short answers.
- **A model answer** — what a strong candidate actually says, written out.

### 9. Recall card

Five lines, maximum. What survives if you forget everything else. This is what you
re-read the night before the interview.

---

## The practice sheet

`03-practice.md` has four parts, in this order.

1. **Code these, in this order.** Named problems for the DSA lesson — title, source, one
   line on what each is really testing — and never a pasted statement. Four problems,
   easiest first, findable by LeetCode number or standard name.
2. **Build these, in all three languages.** Three exercises for the languages theme,
   easiest first, each with one line on what it is really testing. Every exercise is
   built **three times**, once per language. Then a **Compare** section, one sentence
   per language on what was easy and what was hard.
3. **Say these out loud.** Every question the day answers — DSA, system design, and
   languages — each to be answered in two minutes, standing up, no notes.
4. **Before you move on.** One checklist covering both halves.

On a languages project day the "build these" part is the deliverable: the requirements,
the file layout, the commands, and what "done" looks like.

---

## Writing rules

- **Second person, present tense.** "You keep two pointers." Never "we will now consider".
- **Short sentences, one idea each.** The subject is hard; the prose must not be.
- **Define every term the first time it appears.** No unearned vocabulary — if a word has
  not been defined in this lesson or an earlier day, define it here or do not use it.
- **No cheerleading.** No "Great!", no "Now for the fun part!", no emoji in the body.
- **Admit difficulty.** "This is the step people get wrong, and here is why it looks
  right" is worth more than confidence.
- **No study-time estimates.** No "≈45 minutes to read", no "quick". A day is a unit of
  subject. Timing a drill is different and is allowed — that is the interview clock.
- **Grammar and punctuation are part of the job.** Full sentences. Commas where the sense
  needs them, full stops at the end of them. A dropped comma makes a beginner re-read a
  line, and re-reading is the thing this course exists to prevent.
- **No paper, anywhere.** Never ask the reader to draw it on paper, write it on a blank
  page, or work it through with pen and paper. The compliant versions are "say it out loud
  from memory", "name the six beats in order without looking", or "draw it in any tool you
  like". This applies to lesson prose, to §9, and to every checklist in `03-practice.md`.
- **Real output.** Every program shows what it prints. Every error is pasted, not described.
- **Never invent a library API.** If you are not certain a function exists with that
  signature, check it before writing it. A lesson that teaches a method that does not
  exist is worse than no lesson. This matters most on the protobuf, gRPC, and
  third-party-library days.
- **British/Indian-neutral English**, consistent within a file.

## When a lesson gets long

Depth over density. A long lesson is fine. If it genuinely will not fit in one file,
split it into a folder:

```
01-dsa-<topic>/
    1-<part>.md
    2-<part>.md
```

Do **not** compress. Compressing is how the material got too hard the first time.

---

## Generating and checking

```bash
python scripts/build_skeleton.py     # create any missing day folders and placeholders
./k status                           # how many lessons are written, on every track
./k check N                          # does day N follow the nine-section contract
```

The syllabus itself lives in [`scripts/curriculum.py`](../scripts/curriculum.py) — the
DSA and system design rows in `scripts/syllabus/`, the languages rows in
`scripts/syllabus/langs/`. To change what a day teaches, edit those and re-run the
builder — never rename a folder or a lesson file by hand.
