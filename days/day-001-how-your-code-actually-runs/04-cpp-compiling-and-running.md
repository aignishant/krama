---
day: 1
track: cpp
title: "Compiling and running your first program"
phase: "C++ and competitive programming"
status: written
---

# Day 001 · C++ — Compiling and running your first program

**After today you can:** You can install a compiler, turn a text file into a running program, and read a compiler error instead of panicking at it.

**The interviewer asks it as:** *What is the difference between a compiled language and an interpreted one?*

---

> **This is the optional third track.** The course teaches Python, and you should do the
> Python first. C++ is here because contest time limits are set for it, and because some
> interviews are in it. Ten days out of the hundred and eighty carry a C++ lesson. This is
> the first. If you are not doing C++, skip straight to
> [03-practice.md](03-practice.md).

---

## 1. What this is, and why they ask it

C++ is a **compiled** language. You write text in a file, then you run a separate program —
a **compiler** — that translates the whole file into machine instructions and writes out a
second file. That second file is the program. You run it directly, and nothing translates
anything while it runs.

Python does not work this way. Python reads your file while it runs it, working out what each
line means as it arrives. That is why Python starts instantly and why it is slower once it is
going, and it is why a mistake on line 400 of a Python file only shows up when line 400 runs —
where in C++ it stops you before a single line has run.

Interviewers ask because it is the cheapest possible test of whether you know what your tools
are. It comes up in the first two minutes of a phone screen, it comes up when you say "I would
write this part in C++", and it comes up as the reason your contest solution passes at 400
milliseconds where the Python one timed out at two seconds. You need one clean paragraph on
it, ready to say.

Today's DSA lesson tells you where the time goes when your code runs. This tells you what has
to happen before it can run at all.

---

## 2. The story

Vikram is having the bathroom in his flat redone. The mason, Salim, arrives on a Monday
morning at half past seven with two helpers and a drill, and it becomes clear inside a minute
that they do not share a language. Salim speaks Bengali. Vikram speaks Marathi and some Hindi,
but not the kind of Hindi that covers where exactly the shower fitting goes.

For the first two days they manage with hands and pointing. It is slow. Every time Salim wants
to check something he has to stop, find Vikram, and the two of them stand there waving at a
wall until they agree. Half of Monday goes on this. Twice, Salim carries on based on a guess,
and on Tuesday evening Vikram comes home to a hole drilled eleven inches too low, which then
has to be filled and re-drilled.

On Tuesday night Vikram calls his cousin Anwar, who grew up in Kolkata and speaks both. Anwar
comes over after dinner. The two of them sit at the kitchen table and go through the entire
job, end to end — every measurement, every fitting, the order of the tiles, which wall gets the
mirror. Anwar turns all of it into Bengali and records it as a long string of voice notes on
Salim's phone.

It takes them an hour and forty minutes, and it is not a pleasant hour. Twice Anwar stops and
says, this does not make sense — you have said the mirror goes on the left wall and also that
the cabinet goes on the left wall, and they will not both fit. So they settle it there and
then, at the kitchen table, on Tuesday night, before anybody has picked up a drill.

Wednesday is a different job altogether. Salim arrives, puts his phone on the window sill, and
works. He does not stop. Nobody stands behind him translating. He plays the next note, does the
thing, plays the next one. The three of them get more done before lunch on Wednesday than in
the whole of Monday and Tuesday.

Vikram spends the hour and forty minutes once, on Tuesday night. He gets it back every single
hour of the rest of the week.

---

## 3. The idea in plain English

Every piece of that maps onto something with a name.

### Your file is not a program

What you write is **source code** — plain text in a file, in a language people can read.
`main.cpp` is a text file and nothing more. A processor cannot run it any more than Salim
could work from Vikram's Marathi.

The processor runs **machine code**: numbers that mean "add these two", "put this in that
slot", "jump back four instructions". Nobody writes that by hand any more.

### The compiler is Anwar

A **compiler** is a program that reads your source code and writes out machine code. The one
you will use is called **g++**. You hand it `main.cpp`, it hands you back a file you can run —
`main.exe` on Windows, `./main` on Linux and macOS. That output file is the **executable**, or
the **binary**.

This is **compilation**, and it happens once. Wednesday morning does not involve Anwar.

### The two kinds of mistake, and when each one bites

This is the part that actually matters, and it is the reason C++ feels strict at first.

A **compile-time error** is a mistake the compiler catches while translating, before your
program has run at all. A missing semicolon. A misspelt variable name. Passing a word where a
number was wanted. The compiler refuses to produce an executable and tells you the line number.
That is Anwar stopping at the kitchen table to say the mirror and the cabinet cannot both go on
the left wall.

A **run-time error** is a mistake that only appears once the program is running. Reading past
the end of a list of values. Dividing by zero. Running out of memory. The compiler cannot see
these, because they depend on the actual data. That is the hole drilled eleven inches too low:
the instruction was well-formed, it was just wrong.

**C++ moves an enormous amount of work from run time to compile time**, and Python does the
opposite. In Python, `pritn("hello")` is a perfectly valid line until the moment it runs. In
C++, the equivalent mistake stops you at once. That is why C++ beginners see far more errors in
their first week — and why C++ programs, once they compile, fail in fewer stupid ways.

### Interpreted, for contrast

Python is **interpreted**. The Python interpreter reads your file line by line as the program
runs, works out what each line means, and does it. There is no separate translation step and no
executable file. That is Monday and Tuesday: someone standing there translating every
instruction, every time, while the work happens.

It is slower for the obvious reason — the translating is happening during the work, over and
over, including inside loops that run a million times. It is also more forgiving, because
nothing has to make sense until it is reached.

Neither is better. They are different trades, and being able to say what the trade is, in one
sentence, is the whole interview answer.

### The four things g++ actually does

When you run `g++ main.cpp`, four separate steps happen in order. You will meet all four in
error messages, so learn the names now.

1. **Preprocessing.** Every line starting with `#` is handled first — `#include <iostream>`
   literally pastes the entire contents of the `iostream` header file into your file. The
   preprocessor does not understand C++; it does text substitution.
2. **Compiling.** The real translation. Your C++ becomes assembly, then machine code, one
   source file at a time. This is where syntax errors and type errors appear.
3. **Assembling.** Machine code is written into an **object file** — `main.o` — which is
   machine code with the addresses not yet filled in.
4. **Linking.** All the object files, plus the library code your program uses, are stitched
   into one executable and the addresses are resolved. This is where "undefined reference"
   errors come from, and they read completely differently from compile errors.

The single most common beginner confusion in C++ is not knowing whether an error came from step
2 or step 4. Step 2 says `error: ... main.cpp:5:3`. Step 4 says `undefined reference to ...`
and names no line at all. Once you can tell them apart, you can fix them.

---

## 4. The picture

The whole pipeline, with the file at each stage:

```
  YOU WRITE                    g++ DOES THIS                       YOU RUN
  ---------                    -------------                       -------

  main.cpp                                                         ./main
  +-------------+     1        +-------------+
  | #include    | preprocess   | 30,000 lines|
  | int main()  | -----------> | of iostream |
  | { ... }     |              | + your code |
  +-------------+              +-------------+
   plain text                        |
   you can read                      | 2  compile
                                     v
                              +-------------+
                              |  assembly   |
                              +-------------+
                                     | 3  assemble
                                     v
                              +-------------+
                              |   main.o    |   machine code,
                              +-------------+   addresses not filled in
                                     | 4  link  (+ the standard library)
                                     v
                              +-------------+
                              | main / .exe | ------------------->  runs
                              +-------------+                       directly
                               machine code                         on the CPU
```

**What to notice:** the arrow into `./main` has no compiler in it. Once the executable exists,
g++ is out of the picture entirely. Wednesday has no Anwar.

Now the same picture for Python, drawn to the same scale:

```
  YOU WRITE                                              YOU RUN
  ---------                                              -------

  main.py                                    python main.py
  +-------------+                            +-------------------------+
  | print("hi") |  ------------------------> | interpreter reads  line |
  +-------------+                            | works out what it means |
   plain text                                | does it                 |
                                             | reads the next line ... |
                                             +-------------------------+
                                              every line, every time,
                                              including inside loops
```

**What to notice:** in the C++ picture the translation happens once, on the left, before any
running. In the Python picture the translation is inside the running. That single structural
difference is the whole speed story and the whole error-timing story.

---

## 5. The code, built step by step

### Getting a compiler

You need g++ on your machine. Pick the line that matches your computer.

**Windows.** The cleanest option is MSYS2. Install it from `msys2.org`, then open the "MSYS2
UCRT64" terminal it gives you and run:

```
pacman -S mingw-w64-ucrt-x86_64-gcc
```

Then add `C:\msys64\ucrt64\bin` to your PATH so that `g++` works from any terminal. The
alternative, if you would rather not deal with PATH at all, is **WSL** — run `wsl --install` in
PowerShell as administrator, then inside the Ubuntu it installs, run
`sudo apt update && sudo apt install g++`. WSL gives you the same environment the online judges
actually use, which is worth something.

**macOS.** Run `xcode-select --install`. You get `clang++`, which is a different compiler that
speaks the same language. Everything in this track works under it. Where a file says `g++`,
type `clang++`.

**Linux.** `sudo apt install g++` on Debian or Ubuntu, `sudo dnf install gcc-c++` on Fedora.

Check it worked:

```
g++ --version
```

You want a version number of 11 or higher, so that C++20 is fully available.

**If none of that is possible right now**, you can still do every exercise on this track. Use
`godbolt.org` for single files with output, or the C++ editor on LeetCode or Codeforces. You
lose the ability to run a debugger, which matters around
[day 078](../day-078-nodes-and-links/README.md), but nothing before that needs one.

### The smallest program that does something

Start with the one line that produces output.

```cpp
#include <iostream>
```

This is a **preprocessor directive** — the `#` says so. It finds the file called `iostream` in
the compiler's standard library and pastes its entire contents here. `iostream` is where
`std::cout`, the thing that prints, is declared. Without this line the compiler has never heard
of `cout`.

Now the function every C++ program must have.

```cpp
int main() {
    return 0;
}
```

`main` is where execution starts. Every C++ program has exactly one. The `int` in front says
`main` hands back a whole number when it finishes, and `return 0` is that number. **Zero means
the program succeeded.** Any other number means it failed, and the shell and the online judges
both read it. This is a real convention, not a formality — a judge that sees a non-zero exit
code reports a runtime error even if your output was perfect.

Now print something.

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, world\n";
    return 0;
}
```

Read `std::cout << x` as "send x to the output". `cout` is the **standard output stream** —
your terminal. The `<<` is not a shift here; it has been given a second meaning for streams,
and it chains, so you can write `std::cout << a << b << c;`.

`std::` in front means "the one from the standard library". The standard library lives in a
**namespace** called `std`, which is a named box that keeps its names from colliding with
yours. Writing `std::cout` says *that* `cout`, the library's one.

### Compiling it

Save it as `hello.cpp`. Then:

```
g++ -std=c++20 -O2 -Wall -Wextra -o hello hello.cpp
```

Every flag earns its place:

- `-std=c++20` — which version of the language. Without it, older g++ versions default to C++14
  or C++17 and reject perfectly good modern code.
- `-O2` — optimise. This is the flag that makes C++ fast. Without it your program can run three
  to ten times slower, and every benchmark you read online assumes it is on. Online judges
  compile with `-O2`.
- `-Wall -Wextra` — turn on warnings. Not errors: warnings. These catch the mistakes that
  compile fine and then behave wrongly, and a beginner should never compile without them.
- `-o hello` — name the output file `hello`. Leave this out and you get `a.out`, which is a
  historical accident from 1971 and tells you nothing.

Then run it. On Linux, macOS, WSL or Git Bash:

```
./hello
```

On Windows PowerShell or cmd:

```
.\hello.exe
```

The `./` is not decoration. It means "the file called `hello`, here in this folder". Without it
the shell only looks in the system directories and reports that the command was not found.

### About `using namespace std;`

You will see this line at the top of every contest solution:

```cpp
using namespace std;
```

It means "if I write a name you do not recognise, try it with `std::` in front". After it you
write `cout` instead of `std::cout`, `vector` instead of `std::vector`, `sort` instead of
`std::sort`. In a 60-line contest solution written against a clock, this is worth having.

It is also, in real code, discouraged — because `std` contains several thousand names and some
of them are words you would plausibly use yourself. Write `int count = 0;` after it and you are
now competing with `std::count`, which is a real function in the library. Sometimes it compiles
anyway. Sometimes it produces an error message five hundred characters long.

**The rule this track uses:** `using namespace std;` in contest files, where speed of typing is
the whole point and the file lives for two hours. Explicit `std::` in anything you would show
an interviewer in a design round. If an interviewer sees `using namespace std;`, some of them
will ask about it — and "I use it in contests, not in code that ships" is the answer that
lands.

### The complete first program

This one is worth typing rather than pasting, because typing it is how the semicolons get into
your fingers.

```cpp
// hello.cpp — the first program. Compile with:
//   g++ -std=c++20 -O2 -Wall -Wextra -o hello hello.cpp
// Run with:
//   ./hello        (Linux, macOS, WSL, Git Bash)
//   .\hello.exe    (Windows PowerShell)

#include <iostream>   // std::cout, std::cin
#include <string>     // std::string

int main() {
    // A variable: a name for a piece of storage, with a type fixed at compile time.
    std::string name = "world";
    int year = 2026;

    // Send things to standard output. '\n' ends the line.
    std::cout << "Hello, " << name << "\n";
    std::cout << "It is " << year << " and this program was translated once,\n";
    std::cout << "before it ran even a single line.\n";

    // Arithmetic, to prove the types are real.
    int a = 7;
    int b = 2;
    std::cout << a << " / " << b << " = " << a / b << "\n";       // 3, not 3.5
    std::cout << a << " % " << b << " = " << a % b << "\n";       // 1, the remainder

    return 0;   // 0 means success. The shell and every online judge read this.
}
```

Expected output, exactly:

```
Hello, world
It is 2026 and this program was translated once,
before it ran even a single line.
7 / 2 = 3
7 % 2 = 1
```

`7 / 2 = 3` is not a bug, and it is the first thing that surprises a Python programmer. When
both sides of `/` are whole numbers, C++ does **integer division** and throws the fraction away
— it does not round, it truncates towards zero.
[Tomorrow's C++ lesson](../day-002-counting-steps/04-cpp-types-numbers.md) does this properly.
For now, notice it, because it will cost you a wrong answer within your first week.

### `\n` or `endl`

You will see both. They are not the same.

```cpp
std::cout << "line\n";              // writes a newline
std::cout << "line" << std::endl;   // writes a newline AND flushes the buffer
```

**Flushing** means forcing everything held back to be written out right now, rather than when
the holding area fills. That is a request to the operating system, and it is slow —
meaningfully slow if you do it a hundred thousand times in a loop.

**Use `\n`.** Use `endl` only when you genuinely need the output to appear immediately.
[Day 003's C++ lesson](../day-003-big-o-in-plain-english/04-cpp-input-output.md) measures the
difference.

---

## 6. What it costs

The point of C++ is speed, so put a number on it.

A modern processor core runs at roughly 3 GHz, which is 3 × 10^9 clock ticks per second. A
simple operation — one addition, one memory read, one comparison — is one to a few ticks, but
memory access and loop overhead eat into that badly. The number every competitive programmer
works from is:

> **C++ does about 10^8 simple operations per second.** One hundred million.

That is the working figure, not the theoretical peak, and it is deliberately pessimistic so
that estimates made with it come out safe. It is the same figure today's DSA lesson uses when
it counts steps.

Python, running the same loop, does about **10^6 to 10^7 operations per second**. Call it
**fifty times slower** for straight loop-and-arithmetic code. The gap comes from exactly the
Monday-and-Tuesday problem: for every one of your additions, the interpreter is doing tens of
operations of its own, checking types, looking up names, building objects.

So take a contest problem with n = 10^6 and a two-second limit, needing an n log n solution:

```
  operations   = n log2(n)
               = 1,000,000 x 20
               = 2 x 10^7

  C++          = 2 x 10^7 / 10^8      = 0.2 seconds        passes, easily
  Python       = 2 x 10^7 / 5 x 10^6  = 4 seconds          fails at a 2s limit
```

That single sum is why this track exists. The method was identical. The step count was
identical. One passed and one did not.

Two more costs, which are the price you pay for that:

**Compile time.** A small file compiles in about half a second with `-O2`. Add
`#include <bits/stdc++.h>`, which day 003 explains, and it becomes one to three seconds. That
is a real tax on your edit-compile-run loop, and it is Tuesday night at the kitchen table.

**Development time.** You will write more lines to do the same thing, and you will spend the
first fortnight reading error messages. This is the actual cost of C++, it is much larger than
the compile time, and it is why the course teaches Python first and this track second.

---

## 7. The traps

### The near-miss: forgetting to recompile

This one gets everybody exactly once, and it is maddening because there is nothing wrong with
your code.

```
$ g++ -std=c++20 -O2 -o hello hello.cpp
$ ./hello
Hello, world
```

You edit `hello.cpp`, change the message, save, and run:

```
$ ./hello
Hello, world
```

Unchanged. You edit again. Still unchanged. You start to doubt the editor.

The executable is a separate file. Editing the source does not touch it. You ran the Wednesday
recording without asking Anwar to redo it. **Every single change needs the `g++` command again
before `./hello` means anything.** This is the deepest habit difference from Python, where
`python main.py` always runs what you just saved.

The fix is to make it one command, so you cannot forget:

```
g++ -std=c++20 -O2 -Wall -Wextra -o hello hello.cpp && ./hello
```

`&&` means "and only if that succeeded". If compilation fails, the program does not run, so you
never again see stale output from a build that did not happen.

### The real error: the missing semicolon

Delete the semicolon at the end of the `cout` line and compile. This is what g++ 13 prints:

```
hello.cpp: In function 'int main()':
hello.cpp:5:31: error: expected ';' before 'return'
    5 |     std::cout << "Hello, world\n"
      |                               ^
      |                               ;
    6 |     return 0;
      |     ~~~~~~
```

Read it properly, because this is the shape of nearly every C++ error you will ever see:

- `hello.cpp:5:31` — **file, line, column**. Line 5, column 31.
- `error: expected ';' before 'return'` — what it wanted, and what it found instead.
- The `^` marks the exact column, and the `;` printed underneath it on its own line is g++
  telling you what to insert there.
- The last two lines show line 6 with `~~~~~~` under `return`, which is the word that surprised
  it.

**The line number is where the compiler noticed, not always where you erred.** A missing
semicolon on line 5 is reported at the end of line 5 here, but a missing closing brace can be
reported forty lines later, at the end of the file. When an error makes no sense on the line it
names, look upwards.

### The real error: the missing include

Delete `#include <iostream>` and compile:

```
hello.cpp: In function 'int main()':
hello.cpp:4:10: error: 'cout' is not a member of 'std'
    4 |     std::cout << "Hello, world\n";
      |          ^~~~
hello.cpp:1:1: note: 'std::cout' is defined in header '<iostream>'; this is probably fixable by adding '#include <iostream>'
  +++ |+#include <iostream>
    1 | int main() {
```

Modern g++ tells you the header to add and even shows the line it would insert, marked with
`+`. Read the `note:` lines. Beginners skim to the first `error:` and stop, and the fix is
usually sitting in the note underneath.

### The real error: fix the first one only

Make two mistakes at once and g++ produces a wall of text. A missing `}` alone can produce
sixty lines of output. This is normal and it is not sixty problems.

**Fix the first error. Recompile. Look again.** Errors cascade: one confused the compiler, and
everything after it is the compiler being confused, not new information. It is very common for
one fix to clear thirty reported errors.

### The one that is not a compile error at all

Call a function you declared but never wrote the body for:

```
/usr/bin/ld: /tmp/ccXXXXXX.o: in function `main':
hello.cpp:(.text+0x1f): undefined reference to `greet()'
collect2: error: ld returned 1 exit status
```

No `hello.cpp:5:12`. No `^` pointing at a column. The tool named is `ld`, the **linker**, and
this is step 4 from section 3, not step 2. The compiler was happy — you declared `greet()`, so
calling it is legal — but at link time nobody could find the machine code for it.

**Compile error = you wrote something that is not valid C++. Link error = it was valid, but the
code you referred to does not exist anywhere.** Telling these apart at a glance is a real skill
and it takes about a week to acquire.

---

## 8. In the interview

### How it gets asked

- *"What's the difference between a compiled and an interpreted language?"* — the direct
  version, and the most common opening question of any C++ screen.
- *"You've written this in C++ — why?"* — asked when your résumé says both. They are checking
  whether you chose or defaulted.
- *"Your Python solution is correct but it's timing out. What now?"* — the applied version, and
  much more common than the theory one.
- *"What happens when you run `g++ main.cpp`?"* — the systems-flavoured version, and the one
  where naming the four steps puts you ahead of the room.

### What to say out loud, in the first ninety seconds

1. **Say what compilation is.** *"C++ is compiled. A separate program, the compiler, reads my
   whole source file and writes out machine code before anything runs. That file is the
   program."*
2. **Say what interpretation is, in contrast.** *"Python is interpreted — the interpreter reads
   and works out each line while the program runs, so there is no separate build step and no
   executable."*
3. **Name the consequence for speed.** *"That translation cost is paid once in C++ and on every
   iteration in Python, which is why the same approach runs roughly fifty times faster in
   C++."*
4. **Name the consequence for errors.** *"It also moves error detection earlier. A type mistake
   or a typo in a name is a compile error in C++ — it stops me before the program runs. In
   Python the same mistake waits until that line executes."*
5. **Give the four steps if there is room.** *"g++ actually does four things: preprocess,
   compile, assemble, link. Worth knowing because compile errors and link errors read
   completely differently."*
6. **Land the trade-off.** *"So the trade is development speed against run speed and early
   error detection. I reach for Python when the problem is the bottleneck and C++ when the
   machine is."*

Steps 4 and 6 are what make this sound like an opinion rather than a memorised definition.

### The follow-ups

**"Is Java compiled or interpreted?"**
Both, and that is the point of the question. Java compiles to **bytecode** — an intermediate
form that is not machine code — and the Java Virtual Machine then interprets that bytecode, and
compiles the hot parts to real machine code while the program runs. That last step is
**just-in-time compilation**, or JIT. So Java has a build step like C++ and a runtime translator
like Python, which is why it sits between them on speed. C# works the same way. Python has a
version of this too: the `.pyc` files are bytecode, and PyPy adds the JIT that CPython lacks.

**"Then why is C++ still faster than a JIT-compiled language?"**
Three reasons. C++ compiles ahead of time, so it can spend a long time optimising — the JIT has
to be fast because it is competing with the program it is compiling. C++ has no garbage
collector, so there are no pauses and no memory management you did not ask for. And C++ lets
you control how data is laid out in memory directly, which means you can keep it packed
together, and that matters more than instruction count on modern hardware.

**"What does `-O2` actually do?"**
It turns on the optimiser: inlining small functions, unrolling loops, keeping values in
registers instead of memory, removing computations whose results are never used, and doing
several elements at once where it can. It typically makes the program three to ten times faster
than `-O0`, at the cost of compile time and of a debugger showing you confusing line numbers.
`-O3` is more aggressive and is sometimes *slower*, because bigger code fits the instruction
cache worse. Online judges use `-O2`, so that is what you should measure with.

**"What's the difference between a compile error and a link error?"**
A compile error means the text is not valid C++ or does not type-check — the compiler names a
file, a line and a column. A link error means every file compiled fine, but when the linker went
to stitch them together, some function or variable you referred to had no definition anywhere.
The classic causes are declaring a function and never writing its body, forgetting to compile
one of your `.cpp` files, or forgetting to link a library — `undefined reference to
'pthread_create'` means you needed `-pthread` on the command line.

### A model answer

The interviewer has seen "C++ and Python" on the résumé and asks how they differ.

> "The core difference is when the translation to machine code happens.
>
> C++ is compiled ahead of time. I run g++, it reads my whole source file, and it writes out an
> executable containing machine code. Nothing translates anything after that — the processor
> runs those instructions directly. Python is interpreted: the interpreter reads my file while
> the program is running and works out what each line means as it reaches it. There is no
> separate build step and no executable.
>
> That has two consequences I actually care about day to day.
>
> The first is speed. In C++ the translation cost is paid once, before the program starts. In
> Python it is paid on every line, every time — including inside a loop that runs a million
> times. In practice the same approach runs about fifty times faster in C++ for tight numeric
> loops. Concretely: about 10^8 simple operations per second in C++ against maybe 5 × 10^6 in
> Python. That is exactly why a correct n log n solution at n = 10^6 finishes in a fifth of a
> second in C++ and times out in Python at a two-second limit.
>
> The second is when I find out I was wrong. C++ checks types and names at compile time, so a
> typo in a variable name or passing a string where a number was wanted stops me before a single
> line runs. In Python that same mistake sits there quietly until the line executes, which might
> be in production, on the one branch nobody tested.
>
> The cost is development speed. I write more lines in C++, I spend time on memory questions
> that Python simply does not ask, and the first fortnight in a new C++ codebase is largely
> spent reading compiler errors.
>
> So I choose by where the bottleneck is. If the hard part is the problem, I write Python and
> get to a correct answer faster. If the hard part is the machine — a tight time limit, a
> latency budget, something running a hundred million times — I write C++.
>
> One nuance, since it usually comes up: Java and C# are both. They compile to bytecode ahead of
> time and then JIT-compile the hot paths at run time, which is why they land between the two on
> speed."

That answer defines both terms, gives the mechanism rather than the slogan, puts real numbers on
the claim, names a cost as well as a benefit, states a decision rule, and pre-empts the
follow-up. It is about ninety seconds spoken.

---

## 9. Recall card

1. **C++ is compiled: translated once, ahead of time, into a separate executable.** Python is
   interpreted: translated line by line, while running. Everything else follows from that.
2. **g++ does four things: preprocess, compile, assemble, link.** Compile errors name a file,
   line and column. Link errors say `undefined reference` and name no line.
3. **The command is** `g++ -std=c++20 -O2 -Wall -Wextra -o prog prog.cpp && ./prog`. `-O2` is
   the speed, `-Wall -Wextra` are the warnings, `&&` stops you running a stale build.
4. **C++ does about 10^8 simple operations per second; Python about 5 × 10^6.** Fifty times.
   That sum decides which language passes a two-second limit.
5. **Fix the first error, then recompile.** Errors cascade — one mistake commonly reports
   thirty. And `7 / 2` is `3`, because whole numbers divide into whole numbers.

---

**Next in C++:** [day 002 — types, numbers, and
overflow](../day-002-counting-steps/04-cpp-types-numbers.md).
