---
day: 1
track: lang-python
title: "python3, a file, and the interpreter"
theme: "Toolchain and the first program"
phase: "Languages: every language, every basic"
status: written
---

# Day 001 · Python — python3, a file, and the interpreter

**Today's theme:** Toolchain and the first program

**After today you can:** You can install all three toolchains, run a program in each, and read the first error each one gives you.

**The interviewer asks it as:** *What actually happens between saving the file and seeing the output?*

---

## 1. What this is, and why it matters

A program is a list of instructions saved in a file. Python is a language for writing those instructions, and `python3` is a separate program, called an interpreter, that reads your file one line at a time and does what each line says. Today you install it, write one line, run it, and break it on purpose.

At work you will run `python3 something.py` hundreds of times a week, and you will read its error messages far more often than you read its output. Interviewers rarely ask "how do you run Python", but they do ask "what is the difference between an interpreted and a compiled language", and the honest answer starts with what you do today.

## 2. The story

Meera's grandmother cooks the best dal in the family, and the recipe lives only in her head, in Marathi. Meera's flatmate Tom wants to make it. Tom speaks no Marathi.

On Saturday, Meera stands in the kitchen with her grandmother on a video call. Her grandmother says one step. Meera turns to Tom and says it in English. Tom does it. Her grandmother says the next step. Meera translates. Tom does it. It works, and the dal is good, but it takes an hour, and Meera cannot leave the kitchen. If her grandmother says a word Meera does not know, everything stops right there, at that step, with the onions half done.

On Sunday, Tom wants to cook it again. Meera is out. So the whole thing cannot happen. The recipe still exists, in her grandmother's head, but without Meera standing between them, Tom cannot use it.

Meera thinks about this on the bus. The recipe is fine. The problem is that every single time, someone has to stand there and translate, step by step, live.

There is another way, and her cousin does it. Her cousin sat with the grandmother once, for an afternoon, and translated the entire recipe into English in one go, start to finish. She saved it as a note on her phone. Now anyone who reads English can cook the dal, any time, with nobody translating. The cousin does not need to be there. The one cost is that the afternoon of translating happened first, before anyone could cook anything, and if the grandmother changes one step, the cousin has to sit down and redo the translation.

Two ways to get the same dal. Translate live, every time, step by step, and stop the moment you hit a word you do not know. Or translate once, all of it, up front, and then run it as many times as you like without the translator in the room.

Today's Python is Meera in the kitchen.

## 3. The idea in plain English

A **program** is a list of instructions, written in a language a machine can follow. Your grandmother's recipe is a program.

A **file** is a named thing saved on your computer that holds text. You will save your program in a file called `hello.py`. The `.py` at the end is a convention that says "this file holds Python".

A **terminal** is a window where you type commands instead of clicking. A **command** is one line you type and then press Enter. The computer runs it and prints whatever comes back. Everything today happens in a terminal.

An **interpreter** is a program that reads your file one line at a time and carries out each line as it reads it. `python3` is the interpreter for Python. It is Meera in the kitchen: it translates live, step by step, and if it hits a line it does not understand, it stops right there and tells you which line.

The other way, translate the whole thing once up front into something the machine can run directly, is called **compiling**. That is the cousin's afternoon on the sofa. Go and C++ work that way, and you will do both later today. Python does not compile in that sense. Every time you run a Python file, the interpreter reads it from the top.

So when you type `python3 hello.py` and press Enter, three things happen. The terminal finds the program called `python3`. It hands it your file. The interpreter reads the file from the first line, does what each line says, and prints anything the lines tell it to print.

## 4. The picture

```
  you type                 the interpreter                the screen
  ─────────                ───────────────                ──────────
  python3 hello.py  ───►   opens hello.py
                           reads line 1: print("Hello")
                           does it            ────────►   Hello
                           reads line 2: print("Bye")
                           does it            ────────►   Bye
                           reaches the end, exits
```

*Notice that the file is read top to bottom, once, every time you run it. Nothing is saved between runs. If you run it again tomorrow, it reads the file again from line 1.*

## 5. The code, built step by step

First, check that Python is installed. In a terminal, type this and press Enter.

```bash
python3 --version
```

You want to see something like `Python 3.12.10`. Any `3.12` or higher is fine. If you see `command not found`, install Python from the official python.org download page for your system, then close the terminal, open a new one, and try again. On Windows the command may be `python` instead of `python3`; either is fine as long as the version starts with 3.12 or more.

Now make a folder to work in. A **folder** is a named container for files. These two commands make one called `day01` and move you into it.

```bash
mkdir day01
cd day01
```

Open any text editor. Not a word processor, which adds hidden formatting; a plain text editor. Notepad on Windows, TextEdit in plain-text mode on a Mac, or a code editor like VS Code. Type exactly this and save the file as `hello.py` inside `day01`.

```python
print("Hello, world")
```

`print` is a built-in instruction that shows text on the screen. The round brackets hold what to print. The double quotes mark where the text starts and ends. The quotes themselves are not printed.

Run it.

```bash
python3 hello.py
```

You should see `Hello, world`. That is your first program. Now add a second line, so you can see the interpreter go top to bottom.

```python
print("Hello, world")
print("This is line two")
```

Run it again. Two lines appear, in order. Now the most important part of today: break it on purpose. Change the second line to misspell `print`.

```python
print("Hello, world")
prnt("This is line two")
```

Run it. You get this.

```
Hello, world
Traceback (most recent call last):
  File "/home/you/day01/hello.py", line 2, in <module>
    prnt("This is line two")
    ^^^^
NameError: name 'prnt' is not defined
```

Read it bottom to top. The last line is the error and it is the one that matters: `NameError: name 'prnt' is not defined`. Python does not know a word called `prnt`. Above it, the file and line number: `hello.py`, line 2. And above that, the line itself, with little carets pointing at the problem.

Now notice something. `Hello, world` was printed **before** the error. Line 1 ran. Line 2 failed. That is Meera in the kitchen: the dal got as far as the onions, then stopped. A compiled language would have refused to start at all. Hold on to that, because it is the whole point of the day.

Here is the run and the output for the complete program for today, fixed.

```bash
python3 hello.py
```

```
Hello, world
This is line two
Python read this file from the top, one line at a time
```

And the complete file that produces it. The line starting with `#` is a **comment**: a note for humans that the interpreter skips.

```python
# hello.py — day 1, the first program
# Run:  python3 hello.py

print("Hello, world")
print("This is line two")
print("Python read this file from the top, one line at a time")

# Every run starts again at the top of this file.
# Nothing is remembered from the previous run.
```

## 6. How the other two languages do it

The same program, in Go:

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, world")
}
```

```bash
go run hello.go
```

And in C++:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, world\n";
}
```

```bash
g++ -std=c++20 -Wall -Wextra hello.cpp -o hello
./hello
```

The one line of difference that matters: **Python runs the file; Go and C++ first turn the file into a separate program, then run that.** Notice that the C++ version is two commands. The first, `g++ ... -o hello`, is the cousin's afternoon: it reads the whole file, checks all of it, and writes out a new file called `hello` that the machine can run directly. The second command runs that new file. Go's `go run` hides the two steps behind one command, but they still both happen. Python has only the one step, every time.

The bite: in Python, a misspelling on line 200 is not found until line 200 runs, which might be next Tuesday, in production. In Go and C++, a misspelling on line 200 means the program does not exist yet, and nobody can run it until it is fixed.

## 7. The traps

**The near-miss: running the file from the wrong folder.** You save `hello.py` in `day01`, but your terminal is still in your home folder. You type `python3 hello.py` and get this:

```
python3: can't open file '/home/you/hello.py': [Errno 2] No such file or directory
```

The file exists. Python is looking in the wrong place. The fix is `cd day01` first, then run. Read the path in the message: it tells you exactly where Python looked.

**The real error: the quote you forgot.** Delete the closing quote.

```python
print("Hello, world)
```

```
  File "/home/you/day01/hello.py", line 1
    print("Hello, world)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

This one is different from the `NameError` above. A `SyntaxError` is Python saying "I cannot even read this line", and Python does check for those before running anything. So with a `SyntaxError`, nothing prints, not even line 1. With a `NameError`, the lines above it do run. Being able to tell these two apart is the first real skill of the course.

**The near-miss: a word processor.** If you write your program in a word processor and save, it often replaces your straight quotes `"` with curly ones `“ ”`. Python does not accept curly quotes. You get `SyntaxError: invalid character '“' (U+201C)`. Use a plain text editor.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between an interpreted and a compiled language?"
- "Walk me through what happens when you run `python3 script.py`."
- "Why does Python let a typo on line 50 survive until line 50 runs?"

**What to say out loud, the first ninety seconds**

"When I run `python3 hello.py`, the terminal starts a program called the Python interpreter and hands it my file. The interpreter reads the file from the top and carries out each line as it reads it. It does not translate the whole file into machine instructions first. That is the difference from a compiled language like Go or C++, where a separate step reads the whole file, checks it, and produces a new runnable file before anything runs.

The practical consequence is where mistakes are caught. Python does check for syntax errors before it starts, so a missing quote stops it immediately. But a misspelled name is only discovered when that line runs. So line 1 can print successfully and line 2 can fail. In a compiled language, that misspelling stops the program from being built at all."

**The follow-ups**

1. *"So does Python do no checking up front at all?"* — It parses the whole file first, so syntax errors are found before any line runs. What it does not do is check that every name you use exists. That happens at run time.
2. *"Is one approach better?"* — They trade speed of feedback for speed of iteration. Python lets you change one line and run again instantly. Compiled languages catch more mistakes before the program exists, and the built program usually runs faster.
3. *"What is the file that C++ produces?"* — A file the operating system can run directly, with no interpreter in between. On Linux and Mac it has no extension; on Windows it ends in `.exe`.

**A model answer**

"Python is interpreted: `python3` reads the source file and executes it line by line, so there is no separate build step and no second file. The interpreter does parse the whole file before starting, which is why a syntax error stops everything before line 1 runs. But anything beyond syntax, like a name that does not exist, is only discovered when that line is reached. Go and C++ are compiled: a compiler reads all of the source, rejects it if anything is wrong, and writes a runnable file, which you then run separately. The trade is fast iteration and late errors against slower iteration and early errors."

## 9. Recall card

- `python3 hello.py` starts the interpreter and hands it the file; the file is read top to bottom every run.
- Interpreted means translate live, line by line; compiled means translate everything once, up front, into a new file.
- `SyntaxError` is caught before anything runs; `NameError` is caught when that line runs, so earlier lines have already printed.
- Read a traceback bottom up: the last line names the error, the line above it names the file and line number.
- Plain text editor, straight quotes, run from the folder the file is in.
