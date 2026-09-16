---
day: 1
track: lang-cpp
title: "g++, a file, and the compiler"
theme: "Toolchain and the first program"
phase: "Languages: every language, every basic"
status: written
---

# Day 001 · C++ — g++, a file, and the compiler

**Today's theme:** Toolchain and the first program

**After today you can:** You can install all three toolchains, run a program in each, and read the first error each one gives you.

**The interviewer asks it as:** *What actually happens between saving the file and seeing the output?*

---

## 1. What this is, and why it matters

C++ is a compiled language, and unlike Go it makes you do the two steps yourself: one command to turn your file into a runnable program, a second command to run it. The compiler you will use is called `g++`. Today you install it, write the smallest program, run the two commands, and read the compiler's first complaint.

At work, C++ is where the performance-critical parts of the world live: game engines, browsers, trading systems, the insides of databases. Interviewers ask "what does the compiler actually do", "what is the difference between a compile error and a runtime error", and, often on day one of a job, "what flags do you compile with". Today's answers are `-std=c++20 -Wall -Wextra`, and you should be able to say why.

## 2. The story

Meera's grandmother cooks the best dal in the family, and the recipe lives only in her head, in Marathi. Meera's flatmate Tom wants to make it. Tom speaks no Marathi.

On Saturday, Meera stands in the kitchen with her grandmother on a video call. Her grandmother says one step. Meera turns to Tom and says it in English. Tom does it. Her grandmother says the next step. Meera translates. Tom does it. It works, and the dal is good, but it takes an hour, and Meera cannot leave the kitchen. If her grandmother says a word Meera does not know, everything stops right there, at that step, with the onions half done.

On Sunday, Tom wants to cook it again. Meera is out. So the whole thing cannot happen. The recipe still exists, in her grandmother's head, but without Meera standing between them, Tom cannot use it.

Meera thinks about this on the bus. The recipe is fine. The problem is that every single time, someone has to stand there and translate, step by step, live.

There is another way, and her cousin does it. Her cousin sat with the grandmother once, for an afternoon, and translated the entire recipe into English in one go, start to finish. She saved it as a note on her phone. Now anyone who reads English can cook the dal, any time, with nobody translating. The cousin does not need to be there. The one cost is that the afternoon of translating happened first, before anyone could cook anything, and if the grandmother changes one step, the cousin has to sit down and redo the translation.

Two ways to get the same dal. Translate live, every time, step by step, and stop the moment you hit a word you do not know. Or translate once, all of it, up front, and then run it as many times as you like without the translator in the room.

Today's C++ is the cousin on the sofa, and this time you watch her work.

## 3. The idea in plain English

A **program** is a list of instructions saved in a **file**. You will save yours as `hello.cpp`. A **terminal** is a window where you type **commands** and press Enter.

A **compiler** reads your whole file, checks all of it, and writes a new file the machine runs directly. That new file is an **executable**. `g++` is the compiler you use for C++. It is the cousin: the whole translation happens first, and only then can anyone cook.

Where Go hides the two steps behind `go run`, C++ shows them. You type `g++ hello.cpp -o hello` and get a file called `hello`. Then you type `./hello` to run it. If the first step finds a problem, the second file is never written and the second step has nothing to run.

C++ has one more idea to meet today. The compiler is old and has learned many rules over the years, and by default it is quiet about most of them. **Flags** are extra words you add to the command to tell it how to behave. `-std=c++20` says "use the 2020 edition of the language". `-Wall -Wextra` says "tell me about everything that looks suspicious, not only the things that are outright wrong". You always compile with all three. A C++ programmer who compiles without warnings turned on is cooking with the lights off.

## 4. The picture

```
  you type                           g++                         the machine
  ────────                           ───                         ───────────
  g++ -std=c++20 -Wall -Wextra  ──►  reads ALL of hello.cpp
      hello.cpp -o hello             checks every line
                                     error?   ──► print it, write nothing
                                     warning? ──► print it, write hello anyway
                                     clean?   ──► write file "hello"

  ./hello ─────────────────────────────────────────────────────► runs "hello"
                                                                 prints Hello, world
```

*Notice the middle branch. Unlike Go, C++ has a category between "fine" and "refused": a warning prints a message but still writes the executable. That is why the flags matter, and why you read every warning.*

## 5. The code, built step by step

Check the compiler is installed.

```bash
g++ --version
```

You want the first line to show version 13 or higher, because some of the tools this course uses from day 3 onwards need it. If you see `command not found`: on Linux, install the package called `build-essential` or `gcc-c++` with your system's package manager. On a Mac, run `xcode-select --install`. On Windows, install MSYS2 and its `mingw-w64-ucrt-x86_64-gcc` package, or use WSL, which gives you a Linux terminal inside Windows. Then close the terminal, open a new one, and try again.

Make a folder and move into it, or reuse the one from earlier today.

```bash
mkdir day01
cd day01
```

Save this as `hello.cpp`.

```cpp
#include <iostream>
```

`#include` pulls in a library, a collection of tools someone else wrote. `iostream` is the one for reading input and writing output. Without it, the word `std::cout` below means nothing.

```cpp
int main() {
    std::cout << "Hello, world\n";
}
```

`int main()` is where the program starts. Every C++ program has exactly one. The `int` means it hands back a whole number when it finishes, which the operating system reads as "did it succeed"; zero means yes, and if you leave the number out, `main` returns zero for you.

`std::cout` is the screen. Read `<<` as "send this to". `"Hello, world\n"` is the text, and `\n` inside the quotes means "then start a new line". The line ends with a semicolon `;`, and every instruction in C++ does. Forgetting that semicolon is today's error.

Compile it.

```bash
g++ -std=c++20 -Wall -Wextra hello.cpp -o hello
```

If nothing prints, that is success. `-o hello` says "name the output file `hello`". Look, then run.

```bash
ls
./hello
```

```
hello  hello.cpp
Hello, world
```

On Windows with MSYS2 the file is `hello.exe` and you run it with `./hello.exe`.

Now break it on purpose. Remove the semicolon.

```cpp
int main() {
    std::cout << "Hello, world\n"
}
```

```
hello.cpp: In function 'int main()':
hello.cpp:4:35: error: expected ';' before '}' token
    4 |     std::cout << "Hello, world\n"
      |                                  ^
      |                                  ;
    5 | }
      | ~
```

Read it. `hello.cpp:4:35` is file, line, column. `error: expected ';' before '}' token` says exactly what is missing. The compiler even draws where it wanted the semicolon. And critically: `ls` shows no `hello` file was written, or if one was there from the earlier run, it is the old one, not this one. The program with the mistake never existed.

Here is the run and the output for the complete program for today, fixed.

```bash
g++ -std=c++20 -Wall -Wextra hello.cpp -o hello
./hello
```

```
Hello, world
This is line two
g++ checked this whole file before writing the executable
```

And the complete file that produces it. The line starting with `//` is a **comment**, a note for humans that the compiler skips. `return 0;` is written out this time so you can see it; it is the "I succeeded" the operating system reads.

```cpp
// hello.cpp — day 1, the first program
// Build: g++ -std=c++20 -Wall -Wextra hello.cpp -o hello
// Run:   ./hello
#include <iostream>

int main() {
    std::cout << "Hello, world
";
    std::cout << "This is line two
";
    std::cout << "g++ checked this whole file before writing the executable
";
    return 0;
}
```

## 6. How the other two languages do it

The same program in Python, with no compile step at all:

```python
print("Hello, world")
```

```bash
python3 hello.py
```

And in Go, where the compile is real but `go run` hides it:

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

The one line of difference that matters: **C++ has warnings; Go and Python do not have that middle category.** In Go, everything the compiler dislikes is an error and the build stops. In Python, there is no build to stop. In C++, the compiler can dislike something, tell you, and build the program anyway. That is what a warning is. Without `-Wall -Wextra`, most of those messages are simply not shown, and the program is built in silence with the problem inside it. So the C++ habit that the other two languages never had to teach you: turn every warning on, and treat each one as an error you have not been forced to fix yet.

## 7. The traps

**The near-miss: forgetting `-o`.** This compiles fine.

```bash
g++ -std=c++20 -Wall -Wextra hello.cpp
ls
```

```
a.out  hello.cpp
```

There is no `hello`. Without `-o`, the compiler names the output `a.out`, for historical reasons nobody is proud of. `./a.out` runs it. Not an error, but the first time it happens you will spend a minute wondering where your program went.

**The real error: a missing include.** Delete the `#include <iostream>` line.

```
hello.cpp: In function 'int main()':
hello.cpp:3:10: error: 'cout' is not a member of 'std'
    3 |     std::cout << "Hello, world\n";
      |          ^~~~
hello.cpp:1:1: note: 'std::cout' is declared in header '<iostream>'; did you forget to '#include <iostream>'?
```

The compiler knows what you meant and says so in the `note:` line. Get used to reading past the first `error:` line to the notes; they are often the actual fix.

**The near-miss: running the old executable.** You edit `hello.cpp`, run `./hello`, and see the old output. You forgot to recompile. Python never has this problem, because it reads the source file every time. In C++, the executable is a separate file that does not know the source has changed. The habit: compile and run as one line, `g++ ... -o hello && ./hello`, so the run only happens if the compile succeeded.

## 8. Say it out loud

**How it gets asked**

- "What does the compiler do?"
- "What is the difference between a compile-time error and a runtime error?"
- "What flags do you compile with, and why?"

**What to say out loud, the first ninety seconds**

"C++ is compiled ahead of time. I run `g++` on the source file, it reads and checks all of it, and if it is correct it writes an executable, which is a separate file I then run. If there is an error, no executable is written. So a compile-time error is one the compiler finds before the program exists, like a missing semicolon or a name it has never heard of. A runtime error is one that happens while the executable is running, with input the compiler could not have known about.

I always compile with `-std=c++20` so I am using the current language, and `-Wall -Wextra` so the compiler tells me about everything it finds suspicious. Those are warnings rather than errors: the compiler builds the program anyway. Without those flags the warnings are hidden and the mistakes ship. With them, I read every line the compiler prints and fix it."

**The follow-ups**

1. *"What is `a.out`?"* — The default name for the executable when you do not pass `-o`. It is the same file; it just has an unhelpful name.
2. *"Why does the Go compiler not have warnings?"* — Go decided a warning nobody reads is worse than none, so everything it dislikes is an error. C++ kept warnings for compatibility: decades of existing code would stop compiling otherwise.
3. *"What does `int main()` return, and who reads it?"* — An integer the operating system receives when the program ends. Zero means success. Scripts and other programs that launch yours can check it.

**A model answer**

"g++ reads the source, checks it against the language rules, and produces a self-contained executable, or produces nothing and reports the file, line and column of each error. Compile-time errors are found then; runtime errors need the program to actually run with real input. C++ also has warnings, a middle category where the compiler flags something suspicious but still builds, and since most of them are off by default I always compile with `-std=c++20 -Wall -Wextra` and treat every warning as a bug. The two-step compile-then-run cycle also means I must recompile after every edit, since the executable does not track the source the way an interpreter does."

## 9. Recall card

- `g++ -std=c++20 -Wall -Wextra hello.cpp -o hello` then `./hello`; two steps, always.
- Every instruction ends with `;`, and `#include <iostream>` is what makes `std::cout` exist.
- Error means no executable is written; warning means it is written anyway, which is why the `-W` flags are not optional.
- Read past the first `error:` line to the `note:` line; the fix is usually there.
- Edited the source and saw old output? You ran the old executable. Recompile.
