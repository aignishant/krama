---
day: 10
track: lang-cpp
title: "std::ifstream, std::ofstream, std::cin, std::cout, and buffering"
theme: "Files and standard I/O"
phase: "Languages: every language, every basic"
status: written
---

# Day 010 · C++ — std::ifstream, std::ofstream, std::cin, std::cout, and buffering

**Today's theme:** Files and standard I/O

**After today you can:** You can read a file line by line, write one, and read from standard input in each language.

**The interviewer asks it as:** *How do you read a file that is bigger than memory?*

---

## 1. What this is, and why it matters

C++ reads files through `std::ifstream` and writes them through `std::ofstream`, both from `<fstream>`, and both are **streams**, the same kind of thing as `std::cin` and `std::cout` that you have been using since day 1. `std::getline(stream, line)` pulls one line at a time, so a file of any size is read with one line's worth of memory, and the stream closes itself when it goes out of scope, so there is no `with`, no `defer`, and no `close` to forget. The word that ties today together is buffering: every stream keeps a bucket of bytes between your program and the disk or the screen, and knowing when that bucket empties is the difference between fast output and slow, and between a file that has your data and one that does not.

At work, the two mistakes are the file that silently failed to open, because C++ streams do not throw, and the `std::endl` in a hot loop that flushes the bucket a million times. Interviewers ask "how do you read a large file in C++", "what is the difference between `'\n'` and `std::endl`", and "why does `while (!in.eof())` read the last line twice", and all three are today.

## 2. The story

Lakshmi's colony gets water from a tanker every Tuesday morning, because the pipes have not worked properly for years. The tanker holds ten thousand litres. Her house has a tank on the roof that holds five hundred.

Nobody ever lifts the tanker. Nobody even tries to move ten thousand litres at once. The driver connects a hose, and water flows through it, a little at a time, for about twenty minutes, until the roof tank is full. Then he disconnects and moves to the next house. The hose is thin. The water that is in the hose at any one moment is a bucketful, maybe less. But over twenty minutes, a bucketful at a time, five hundred litres get up to the roof.

Before the tanker, when Lakshmi was small, they did it with actual buckets. A line of people from the well to the house, passing buckets hand to hand. Nobody in the line ever held more than one bucket. Nobody needed to know how much water was in the well, or how much the house needed. Each person had one job: take the full bucket from the left, pass it to the right, take the empty one back. You could fill a house or a whole street that way, one bucket at a time, and no single person ever carried more than they could hold.

Her grandfather used to say the well did not care who was at the other end of the line. Could be Lakshmi's house, could be the temple, could be a field. The line just moved buckets. And the house did not care where the water came from. Well, tanker, rain off the roof. Water arrived at the tap, and the tap did not ask.

There was one rule her grandfather was strict about. When you were done at the well, you put the cover back on. Not when you remembered. Not tomorrow. The moment the last bucket came up. An open well is how things fall in.

## 3. The idea in plain English

A **stream** is a hose: something bytes flow through, one direction, in order. `std::cout` is a stream to the screen, `std::cin` a stream from the keyboard, and you have used both since day 1. `std::ifstream` is a stream from a file and `std::ofstream` a stream to one, from the header `<fstream>`. Because they are all streams, everything you know about `<<` and `>>` works on files unchanged.

`std::ifstream in("notes.txt");` opens the file for reading. It does **not** throw if the file is missing. Instead the stream is left in a failed state, and you must ask: `if (!in)`. Forget that, and every read silently does nothing. That is the one habit today: open, then check.

`std::getline(in, line)` reads one line into a `std::string`, **without** the newline, and returns the stream, which counts as `true` if the read worked and `false` at the end or on error. So `while (std::getline(in, line))` is the hose: one line in memory at a time, any file size. It is the answer to the interview question, and the shape you write for the rest of your life.

`std::ofstream out("notes.txt");` opens for writing and **empties the file first**. `std::ofstream out("notes.txt", std::ios::app);` appends. Write with `<<`, exactly like `std::cout`.

**Closing**: when `in` or `out` goes out of scope, its destructor closes the file. The cover goes back on the well without anyone remembering. That is RAII, and day 13 is about it. You can call `.close()` early if you need the file closed before the scope ends; otherwise you write nothing.

**Buffering**: every stream keeps a bucket. Writes go into the bucket, and the bucket is emptied to the disk or screen when it fills, when the stream closes, or when you **flush** it. `'\n'` puts a newline in the bucket. `std::endl` puts a newline in the bucket **and empties it**. In a loop writing a million lines, `std::endl` empties the bucket a million times and is dramatically slower. Use `'\n'`, and flush on purpose with `std::flush` when you need the output visible now, for instance before a long pause. `std::cerr`, the error stream, is unbuffered, so errors always appear immediately.

**Standard input**: `std::cin` is the tap. `std::cin >> word` reads one whitespace-separated word; `std::getline(std::cin, line)` reads a whole line. Mixing the two leaves a newline in the bucket that the next `getline` reads as an empty line, and that is in the traps.

## 4. The picture

```
 the same hose, four ends

   file ─────► std::ifstream in("notes.txt")   ─┐
   keyboard ─► std::cin                          ├─► std::getline(stream, line)   one line at a time
                                                 ┘
   std::ofstream out("notes.txt")  ─┐
   std::cout                        ├─► stream << "text" << '\n'        into the bucket
   std::cerr (no bucket)           ─┘

 the bucket (buffer)
   out << "a" << '\n';      ┌──────────────┐
   out << "b" << '\n';      │ a\n b\n      │   still here, not on disk
   out << std::endl;        └──────┬───────┘   endl: newline AND empty the bucket
                                   ▼ disk
   }  ← scope ends: destructor flushes and closes, whatever happened
```

*Notice that `getline` does not care which stream is behind it. Notice that the bucket empties on three events only: full, flushed, closed.*

## 5. The code, built step by step

Start `water.cpp` in a `day10` folder. Writing first.

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    {
        std::ofstream out("notes.txt");
        if (!out) {
            std::cerr << "could not open notes.txt for writing\n";
            return 1;
        }
        out << "Tuesday: tanker came at 7\n";
        out << "Wednesday: no water\n";
        out << "Thursday: pipe repaired\n";
    }
```

The extra pair of braces makes a scope. When it ends, `out` is destroyed, the bucket is flushed, and the file is closed, all before the next line runs. `return 1` from `main` tells the terminal the program failed.

Reading, one line at a time.

```cpp
    std::ifstream in("notes.txt");
    if (!in) {
        std::cerr << "could not open notes.txt\n";
        return 1;
    }
    std::string line;
    int number = 0;
    while (std::getline(in, line)) {
        ++number;
        std::cout << number << " " << line << '\n';
    }
```

```
1 Tuesday: tanker came at 7
2 Wednesday: no water
3 Thursday: pipe repaired
```

`line` never contains the newline. `getline` returns something that is `false` when the file is finished, so the loop ends cleanly. This loop is the same on a three-line file and a three-billion-line file.

Append, and count without holding the file.

```cpp
    {
        std::ofstream more("notes.txt", std::ios::app);
        more << "Friday: tanker again\n";
    }

    std::ifstream again("notes.txt");
    int count = 0;
    while (std::getline(again, line)) {
        if (line.find("tanker") != std::string::npos) {
            ++count;
        }
    }
    std::cout << "days with a tanker: " << count << '\n';
```

```
days with a tanker: 2
```

`std::ios::app` opens for appending. `find` and `npos` are day 3. One line in memory throughout.

The file that is not there, and what C++ does about it.

```cpp
    std::ifstream missing("missing.txt");
    std::cout << std::boolalpha << "opened? " << static_cast<bool>(missing) << '\n';
    std::string nothing;
    std::getline(missing, nothing);
    std::cout << "read: [" << nothing << "]\n";
```

```
opened? false
read: []
```

No exception, no message. The open failed, the stream is in a failed state, and `getline` on it quietly reads nothing. Python raised `FileNotFoundError`; Go returned an error you could not ignore; C++ set a flag and waited for you to ask. This is why `if (!in)` comes right after every open.

Standard input, and the two ways to read it. Save this as `count_lines.cpp`.

```cpp
#include <iostream>
#include <string>

int main() {
    std::string line;
    int total = 0;
    while (std::getline(std::cin, line)) {
        ++total;
    }
    std::cout << total << " lines\n";
}
```

```bash
g++ -std=c++20 -Wall -Wextra count_lines.cpp -o count_lines
./count_lines < notes.txt
```

```
4 lines
```

The same loop as the file version with `std::cin` in place of `in`. The tap does not ask what is upstream.

Here is the build, run, and output for the complete program.

```bash
g++ -std=c++20 -Wall -Wextra water.cpp -o water
./water
```

```
wrote 3 lines
1 Tuesday: tanker came at 7
2 Wednesday: no water
3 Thursday: pipe repaired
days with a tanker: 2
missing.txt opened? false, read: []
```

And the complete file.

```cpp
// water.cpp — day 10, file streams, getline, buffering
// Build: g++ -std=c++20 -Wall -Wextra water.cpp -o water
// Run:   ./water
#include <fstream>
#include <iostream>
#include <string>

int main() {
    {
        std::ofstream out("notes.txt");
        if (!out) {
            std::cerr << "could not open notes.txt for writing\n";
            return 1;
        }
        out << "Tuesday: tanker came at 7\n";
        out << "Wednesday: no water\n";
        out << "Thursday: pipe repaired\n";
    }   // out is destroyed here: flushed and closed
    std::cout << "wrote 3 lines\n";

    std::ifstream in("notes.txt");
    if (!in) {
        std::cerr << "could not open notes.txt\n";
        return 1;
    }
    std::string line;
    int number = 0;
    while (std::getline(in, line)) {
        ++number;
        std::cout << number << " " << line << '\n';
    }

    {
        std::ofstream more("notes.txt", std::ios::app);
        more << "Friday: tanker again\n";
    }

    std::ifstream again("notes.txt");
    int count = 0;
    while (std::getline(again, line)) {
        if (line.find("tanker") != std::string::npos) {
            ++count;
        }
    }
    std::cout << "days with a tanker: " << count << '\n';

    std::ifstream missing("missing.txt");
    std::string nothing;
    std::getline(missing, nothing);
    std::cout << std::boolalpha << "missing.txt opened? " << static_cast<bool>(missing)
              << ", read: [" << nothing << "]\n";
    return 0;
}
```

## 6. How the other two languages do it

Python, where a missing file raises and `with` closes:

```python
with open("notes.txt", encoding="utf-8") as f:    # FileNotFoundError if missing
    for line in f:                                # line keeps its "\n"
        if "tanker" in line:
            count += 1
```

Go, where a missing file is a returned error and `defer` closes:

```go
f, err := os.Open("notes.txt")
if err != nil {                                   // cannot be skipped without _
	return err
}
defer f.Close()
scanner := bufio.NewScanner(f)
for scanner.Scan() {                              // Text() has no newline
	if strings.Contains(scanner.Text(), "tanker") {
		count++
	}
}
```

The one line of difference that matters: **a missing file is loud in Python, unignorable in Go, and silent in C++.** Python stops you with an exception. Go's compiler stops you from taking the file without the error. C++ hands you a stream in a failed state and lets every read on it do nothing, so the `if (!in)` check is a discipline, not a feature. On closing, the order reverses: C++ is the safest, because the destructor closes the file with no line of code to forget, where Python needs the `with` block and Go needs the `defer` line.

## 7. The traps

**The near-miss: the `eof` loop.** Test for end of file before reading.

```cpp
    std::ifstream in("notes.txt");
    std::string line;
    while (!in.eof()) {
        std::getline(in, line);
        std::cout << line << '\n';
    }
```

```
Tuesday: tanker came at 7
Wednesday: no water
Thursday: pipe repaired
Friday: tanker again
Friday: tanker again
```

The last line prints twice. `eof()` only becomes true **after** a read fails, so after the last successful `getline`, `eof()` is still false, the loop runs once more, `getline` fails and leaves `line` unchanged, and you print it again. Put the read in the condition: `while (std::getline(in, line))`. Every C++ programmer has written the `eof` loop once, and it is a standard interview question.

**The near-miss: `>>` then `getline`.** Read a number, then a line, from the keyboard.

```cpp
    int age;
    std::string name;
    std::cin >> age;
    std::getline(std::cin, name);
    std::cout << "[" << name << "]\n";
```

Type `30`, Enter, and the program prints `[]` without waiting for a name. `>>` read the `30` and left the Enter, a newline, in the bucket. `getline` read up to that newline and got an empty string. After a `>>`, discard the rest of the line with `std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');` from `<limits>`, or read everything with `getline` and convert.

**The real error: a stream is not a value.** Try to copy-initialise a stream from a name.

```cpp
    std::ofstream out = "notes.txt";
```

```
water.cpp: In function 'int main()':
water.cpp:6:24: error: conversion from 'const char [10]' to non-scalar type 'std::ofstream' {aka 'std::basic_ofstream<char>'} requested
    6 |     std::ofstream out = "notes.txt";
      |                        ^~~~~~~~~~~
```

The stream's constructor is marked `explicit`, which forbids this quiet conversion. Write `std::ofstream out("notes.txt");` or `std::ofstream out{"notes.txt"};`. Streams also cannot be copied at all, `std::ofstream b = a;` is an error, because two hoses cannot share one bucket; they can be moved, which day 38 covers.

**The near-miss: `std::endl` in a loop.** Write a million lines.

```cpp
    for (int i = 0; i < 1'000'000; ++i) {
        out << i << std::endl;
    }
```

It works, and it is several times slower than the same loop with `'\n'`, because each `std::endl` empties the bucket to disk. The bucket exists so that a million small writes become a few thousand large ones; `std::endl` defeats it. `'\n'` in loops, `std::flush` when you specifically need the output now.

## 8. Say it out loud

**How it gets asked**

- "How do you read a file that is bigger than memory in C++?"
- "What is the difference between `'\n'` and `std::endl`?"
- "Why does `while (!in.eof())` read the last line twice?"

**What to say out loud, the first ninety seconds**

"I open an `std::ifstream`, check it with `if (!in)` because a failed open sets a flag rather than throwing, and then loop `while (std::getline(in, line))`. `getline` reads one line into a string without its newline and returns the stream, which converts to `false` when the read fails, so the loop holds one line at a time and the file can be any size. The classic mistake is testing `in.eof()` before the read: end-of-file is only set after a read fails, so the loop body runs once more with stale data and the last line appears twice. The stream closes itself in its destructor, so there is no `close` to forget.

Streams are buffered. `'\n'` writes a newline into the buffer; `std::endl` writes a newline and flushes the buffer to the device. In a loop, `std::endl` turns thousands of cheap buffered writes into thousands of system calls, so I use `'\n'` and flush explicitly with `std::flush` only when I need output visible immediately. `std::cerr` is unbuffered, which is why errors appear at once. `std::cin` is the same kind of stream, so the same `getline` loop reads standard input from a keyboard, a pipe or a redirected file."

**The follow-ups**

1. *"How do you make streams throw on failure instead of setting flags?"* — `in.exceptions(std::ifstream::failbit | std::ifstream::badbit)` before the open. Most code does not, because end-of-file also sets `failbit` on the final read, which makes the normal loop end with an exception.
2. *"How do you read a file as raw bytes?"* — Open with `std::ios::binary` and use `in.read(buffer, size)` in a loop, checking `in.gcount()` for how many bytes actually arrived. Text mode can translate newlines on some systems; binary mode never does.
3. *"How do you read a whole small file into a string?"* — `std::string content((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());` from `<iterator>`. Ugly but standard; only for files you know are small.

**A model answer**

"C++ file I/O is stream-based: `std::ifstream` and `std::ofstream` share the `<<`, `>>` and `getline` interface with `std::cin` and `std::cout`. A failed open does not throw; it sets the fail state, so every open is followed by `if (!stream)`. Large files are read line by line with `while (std::getline(in, line))`, which tests the read itself and so avoids the double-last-line bug of `while (!in.eof())`. Streams are closed by their destructors at scope exit, an instance of RAII. All streams buffer; `'\n'` appends to the buffer and `std::endl` also flushes it, so `std::endl` in loops is a well-known performance mistake, and `std::cerr` is unbuffered for immediacy. Mixing `>>` and `getline` on `std::cin` leaves a newline in the buffer that must be discarded with `ignore`. Streams are non-copyable and constructed explicitly from a path."

## 9. Recall card

- `std::ifstream in("file");` then `if (!in)` immediately: a missing file sets a flag and every read silently does nothing.
- Bigger than memory: `std::string line; while (std::getline(in, line)) { ... }`; one line at a time, no newline attached; never `while (!in.eof())`.
- `std::ofstream out("file")` empties the file; `std::ios::app` appends; the destructor flushes and closes at scope end, no `close` needed.
- `'\n'` goes in the bucket; `std::endl` also empties it; use `'\n'` in loops and `std::flush` on purpose; `std::cerr` has no bucket.
- `std::cin >> x` leaves the newline behind; `ignore` it before `getline`; `std::ofstream out = "file";` is a compile error because the constructor is `explicit`.
