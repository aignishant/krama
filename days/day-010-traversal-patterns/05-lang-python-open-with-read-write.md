---
day: 10
track: lang-python
title: "open, with, read/write, pathlib, and sys.stdin"
theme: "Files and standard I/O"
phase: "Languages: every language, every basic"
status: written
---

# Day 010 · Python — open, with, read/write, pathlib, and sys.stdin

**Today's theme:** Files and standard I/O

**After today you can:** You can read a file line by line, write one, and read from standard input in each language.

**The interviewer asks it as:** *How do you read a file that is bigger than memory?*

---

## 1. What this is, and why it matters

A file is a named block of bytes on disk, and reading it means pulling those bytes into your program a piece at a time, not all at once. Python opens a file with `open`, guarantees it is closed again with `with`, and lets you walk it one line at a time with a plain `for`, which is the answer to the interview question: a file bigger than memory is read the same way as a small one, line by line, and never all at once. Standard input is the same idea with no file: text arriving from whoever ran your program.

At work, every program reads a config, writes a log, or processes a data file, and the two bugs that follow you are the file you forgot to close and the file you read whole because it was small in testing. Interviewers ask "what does `with` do", "how would you process a 50 GB log", and "what is the difference between `read()`, `readline()` and iterating", and all three are today.

## 2. The story

Lakshmi's colony gets water from a tanker every Tuesday morning, because the pipes have not worked properly for years. The tanker holds ten thousand litres. Her house has a tank on the roof that holds five hundred.

Nobody ever lifts the tanker. Nobody even tries to move ten thousand litres at once. The driver connects a hose, and water flows through it, a little at a time, for about twenty minutes, until the roof tank is full. Then he disconnects and moves to the next house. The hose is thin. The water that is in the hose at any one moment is a bucketful, maybe less. But over twenty minutes, a bucketful at a time, five hundred litres get up to the roof.

Before the tanker, when Lakshmi was small, they did it with actual buckets. A line of people from the well to the house, passing buckets hand to hand. Nobody in the line ever held more than one bucket. Nobody needed to know how much water was in the well, or how much the house needed. Each person had one job: take the full bucket from the left, pass it to the right, take the empty one back. You could fill a house or a whole street that way, one bucket at a time, and no single person ever carried more than they could hold.

Her grandfather used to say the well did not care who was at the other end of the line. Could be Lakshmi's house, could be the temple, could be a field. The line just moved buckets. And the house did not care where the water came from. Well, tanker, rain off the roof. Water arrived at the tap, and the tap did not ask.

There was one rule her grandfather was strict about. When you were done at the well, you put the cover back on. Not when you remembered. Not tomorrow. The moment the last bucket came up. An open well is how things fall in.

## 3. The idea in plain English

A **file** is a named block of bytes on disk. `open("notes.txt")` connects your program to it and gives back a **file object**, the hose. Reading pulls bytes through the hose into your program; writing pushes them the other way. When you are done, the file must be **closed**, which flushes anything still in the hose and puts the cover back on the well.

`with open("notes.txt", encoding="utf-8") as f:` opens the file and guarantees it is closed when the indented block ends, whether the block finishes normally or raises. That is yesterday's `finally`, built in. You never call `close()` yourself; you write `with`. The `encoding="utf-8"` says how the bytes turn into text, and you write it every time, because the default differs between machines.

The **mode** is the second argument: `"r"` to read, which is the default; `"w"` to write, which **empties the file first**; `"a"` to append at the end. Add `"b"` for raw bytes instead of text.

Reading, three ways. `f.read()` pulls the **whole** file into one string: lifting the tanker. Fine for a config file, fatal for a log the size of your disk. `f.readline()` gives one line. And `for line in f:` walks the file **one line at a time**, holding only the current line in memory. That is the hose, and it is the answer to the interview question: iterating over the file object reads a file of any size using a bucketful of memory. Each `line` ends with its newline character, `"\n"`, so you usually strip it with `.rstrip("\n")`.

Writing: `f.write("text\n")` pushes text into the file. It does not add a newline for you. `print("text", file=f)` does.

**`pathlib.Path`** is the modern way to name files: `Path("data") / "notes.txt"` builds a path with the right separator for the machine, `.exists()` asks whether it is there, `.read_text(encoding="utf-8")` and `.write_text(...)` do the small-file cases in one line, and `.open()` gives you the hose when you want to stream.

**Standard input**, `sys.stdin`, is the tap in the kitchen. Text arrives from whoever ran your program: a person typing, or another program's output piped in with `|`. It is a file object, so `for line in sys.stdin:` reads it line by line, exactly like a file. `input()` reads one line from it and strips the newline. Standard output, `sys.stdout`, is where `print` goes.

## 4. The picture

```
 disk file notes.txt (any size)          your program
 ┌──────────────────────────┐
 │ line 1\n                 │            with open(...) as f:
 │ line 2\n                 │  ── hose ──►   for line in f:        holds ONE line
 │ ...                      │                    process(line)
 │ line 40 000 000\n        │
 └──────────────────────────┘            f.read()  ◄── lifts the whole tanker into memory

 sys.stdin                                the tap: same hose, no file behind it
 keyboard ─┐
 pipe |  ──┼── hose ──►   for line in sys.stdin:
 file <  ──┘
```

*Notice that iterating and `read()` are two different pictures: one bucket at a time, or the whole tanker. Notice that the program reading from the tap cannot tell what is upstream, and does not need to.*

## 5. The code, built step by step

Start `water.py` in a `day10` folder. Write a file first, so there is something to read.

```python
from pathlib import Path

notes = Path("notes.txt")
with notes.open("w", encoding="utf-8") as f:
    f.write("Tuesday: tanker came at 7\n")
    f.write("Wednesday: no water\n")
    print("Thursday: pipe repaired", file=f)
```

Mode `"w"` creates the file or empties it. `write` needs the `\n`; `print(..., file=f)` adds one. When the block ends, the file is closed and everything is on disk.

Read it the small way and the right way.

```python
print(notes.read_text(encoding="utf-8"))

with notes.open(encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(number, line.rstrip("\n"))
```

```
Tuesday: tanker came at 7
Wednesday: no water
Thursday: pipe repaired

1 Tuesday: tanker came at 7
2 Wednesday: no water
3 Thursday: pipe repaired
```

`read_text` is the whole tanker, and it is fine for three lines. The `for` is the hose. `enumerate(f, start=1)` gives you a counter alongside each line. The blank line after the first print is the file's own final newline plus `print`'s.

Append, then count without holding the file.

```python
with notes.open("a", encoding="utf-8") as f:
    f.write("Friday: tanker again\n")

count = 0
with notes.open(encoding="utf-8") as f:
    for line in f:
        if "tanker" in line:
            count += 1
print("days with a tanker:", count)
```

```
days with a tanker: 2
```

That counting loop works identically on a four-line file and a forty-million-line file, with the same memory. This is the answer to "bigger than memory".

The file that is not there.

```python
with open("missing.txt", encoding="utf-8") as f:
    print(f.read())
```

```
Traceback (most recent call last):
  File "/home/you/day10/water.py", line 20, in <module>
    with open("missing.txt", encoding="utf-8") as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'
```

Yesterday's exceptions, applied. Catch `FileNotFoundError` when a missing file is expected; let it climb when it is a bug.

Standard input. Save this as `count_lines.py`.

```python
import sys

total = 0
for line in sys.stdin:
    total += 1
print(f"{total} lines")
```

```bash
python3 count_lines.py < notes.txt
```

```
4 lines
```

`<` in the terminal connects the file to your program's standard input. The program did not open anything; it read the tap. Run it without `<` and it waits for you to type lines, ending when you press Ctrl+D on Linux and Mac or Ctrl+Z then Enter on Windows. Run it as `cat notes.txt | python3 count_lines.py` and the tap is fed by another program.

Here is the run and output for the complete program.

```bash
python3 water.py
```

```
wrote 3 lines
whole file:
Tuesday: tanker came at 7
Wednesday: no water
Thursday: pipe repaired

line by line:
  1 Tuesday: tanker came at 7
  2 Wednesday: no water
  3 Thursday: pipe repaired
after append, days with a tanker: 2
missing.txt: [Errno 2] No such file or directory: 'missing.txt'
```

And the complete file.

```python
# water.py — day 10, files, with, pathlib, stdin
# Run:  python3 water.py
#       python3 water.py < notes.txt     (to feed standard input; see count_stdin below)
import sys
from pathlib import Path

notes = Path("notes.txt")

with notes.open("w", encoding="utf-8") as f:
    f.write("Tuesday: tanker came at 7\n")
    f.write("Wednesday: no water\n")
    print("Thursday: pipe repaired", file=f)
print("wrote 3 lines")

print("whole file:")
print(notes.read_text(encoding="utf-8"))

print("line by line:")
with notes.open(encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        text = line.rstrip("
")
        print(f"  {number} {text}")

with notes.open("a", encoding="utf-8") as f:
    f.write("Friday: tanker again\n")

count = 0
with notes.open(encoding="utf-8") as f:
    for line in f:
        if "tanker" in line:
            count += 1
print(f"after append, days with a tanker: {count}")

try:
    with open("missing.txt", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError as error:
    print(f"missing.txt: {error}")


def count_stdin() -> int:
    """Read the tap line by line; whoever is upstream does not matter."""
    total = 0
    for _ in sys.stdin:
        total += 1
    return total
```

`count_stdin` is defined but not called, so that `water.py` runs without waiting for input; call it from a second script, or paste its body into `count_lines.py` as above, and feed it with `<` or a pipe.

## 6. How the other two languages do it

Go, where the hose is a `bufio.Scanner`, closing is `defer`, and the tap is `os.Stdin`:

```go
f, err := os.Open("notes.txt")
if err != nil {
	return err
}
defer f.Close()

scanner := bufio.NewScanner(f)
for scanner.Scan() {
	line := scanner.Text()       // no trailing newline
	fmt.Println(line)
}
```

C++, where the hose is `std::ifstream` and closing happens in the destructor:

```cpp
std::ifstream in("notes.txt");
if (!in) {
    std::cerr << "could not open notes.txt\n";
    return 1;
}
std::string line;
while (std::getline(in, line)) {     // no trailing newline
    std::cout << line << "\n";
}
```

The one line of difference that matters: **all three read line by line with a loop, but only Python hands you the newline still attached.** `for line in f` gives `"Tuesday...\n"`; Go's `scanner.Text()` and C++'s `getline` strip it. A Python programmer forgetting `.rstrip("\n")` prints double-spaced output; a Go or C++ programmer moving to Python compares `line == "Tuesday"` and it is never true. The second difference is how the file gets closed: Python's `with` block, Go's `defer f.Close()` line, and C++'s nothing at all, because the `ifstream` closes itself when it goes out of scope, which is day 13.

## 7. The traps

**The near-miss: the newline that came along.** Look for an exact line.

```python
with notes.open(encoding="utf-8") as f:
    for line in f:
        if line == "Wednesday: no water":
            print("found it")
```

Prints nothing. The line is `"Wednesday: no water\n"`. Strip it, or compare with `line.rstrip("\n") ==`, or use `in` when a substring is enough.

**The near-miss: no `with`.** Open, write, forget.

```python
f = open("log.txt", "w", encoding="utf-8")
f.write("started\n")
# program continues for a long time, then crashes
```

`log.txt` may be empty when you look at it. Writes sit in a buffer until the file is closed or the buffer fills, and a crash before either loses them. `with` closes on every exit path. If you must hold a file open, call `f.flush()` after important writes.

**The real error: the whole tanker.** Read a large file with `read()` and split it.

```python
with open("huge.log", encoding="utf-8") as f:
    lines = f.read().split("\n")
```

```
MemoryError
```

That is the entire message, and it arrives after the machine has spent a while swapping. The file was bigger than memory, and `read()` asked for all of it, and `split` then asked for a second copy as a list. Iterate instead: `for line in f:`. Every Python programmer does this once, on a file that was small in development.

## 8. Say it out loud

**How it gets asked**

- "How do you read a file that is bigger than memory?"
- "What does `with` do, and why use it for files?"
- "What is the difference between `read()`, `readline()`, and iterating over the file?"

**What to say out loud, the first ninety seconds**

"I open the file with `with open(path, encoding='utf-8') as f:` so that it is closed on every exit path, including exceptions, and I iterate over the file object: `for line in f:`. That reads one line at a time through a small buffer, so memory use is bounded by the longest line, not the file size. A file larger than memory is processed exactly the same way as a small one; the only thing I must not do is call `f.read()` or `f.readlines()`, which load everything. For binary data or files without line structure, I read fixed-size chunks with `f.read(65536)` in a loop until it returns empty.

`with` is a context manager: it calls `close()` when the block ends, which flushes buffered writes to disk, so a crash cannot lose them and the operating system handle is released. Each line from iteration keeps its trailing newline, so I strip it when comparing. `pathlib.Path` builds paths portably and has `read_text` and `write_text` for the small cases. Standard input is `sys.stdin`, also a file object, so the same `for line in sys.stdin:` handles a pipe, a redirected file or a keyboard without knowing which."

**The follow-ups**

1. *"What happens if two `with` statements are nested and the inner one raises?"* — Both files are closed, inner first, then the exception continues to propagate. `with` is `try`/`finally` in disguise, and they nest the same way.
2. *"How would you read a 50 GB CSV and compute one column's average?"* — Stream it: open with `with`, use the `csv` module's reader over the file object, which is itself line-buffered, and keep a running sum and count. Never build a list of rows.
3. *"Why pass `encoding='utf-8'` explicitly?"* — The default encoding depends on the operating system's settings. On some Windows machines it is not UTF-8, and a file with Hindi text written on Linux fails to read with `UnicodeDecodeError`. Saying it explicitly makes the program behave the same everywhere.

**A model answer**

"Reading a file larger than memory means streaming it: `with open(path, encoding='utf-8') as f: for line in f:` yields one line at a time from an internal buffer, so memory is bounded by line length, and for unstructured data `f.read(chunk_size)` in a loop does the same. `read()` and `readlines()` load the whole file and are only for small inputs. `with` guarantees `close()` and therefore the flush of buffered writes on all exit paths. Modes are `r`, `w` which truncates, `a` which appends, plus `b` for bytes; iterated lines retain `\n`. `pathlib.Path` handles paths portably and offers `read_text`/`write_text` for one-liners. `sys.stdin` is a file object too, so the same streaming loop reads a pipe or redirected file, and `print(..., file=f)` writes to any file object including `sys.stderr`."

## 9. Recall card

- `with open(path, mode, encoding="utf-8") as f:` opens and guarantees `close()`; modes `r`, `w` (empties first), `a`; always name the encoding.
- Bigger than memory: `for line in f:` holds one line; never `f.read()` on a large file; chunks with `f.read(65536)` for binary.
- Each iterated `line` keeps its `\n`; strip with `.rstrip("\n")` before comparing; `f.write` adds no newline, `print(..., file=f)` does.
- `Path("dir") / "file.txt"`, `.exists()`, `.read_text()`, `.write_text()`, `.open()`; missing file is `FileNotFoundError: [Errno 2] No such file or directory`.
- `sys.stdin` is a file object: `for line in sys.stdin:` reads a pipe, a `< file`, or the keyboard the same way.
