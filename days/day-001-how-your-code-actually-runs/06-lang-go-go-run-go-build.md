---
day: 1
track: lang-go
title: "go run, go build, and the Go toolchain"
theme: "Toolchain and the first program"
phase: "Languages: every language, every basic"
status: written
---

# Day 001 · Go — go run, go build, and the Go toolchain

**Today's theme:** Toolchain and the first program

**After today you can:** You can install all three toolchains, run a program in each, and read the first error each one gives you.

**The interviewer asks it as:** *What actually happens between saving the file and seeing the output?*

---

## 1. What this is, and why it matters

Go is a compiled language: a tool called the compiler reads your whole file, checks every line, and writes out a new file that the machine runs directly. The single command `go` does everything: it compiles, runs, formats, and tests. Today you install it, write the smallest program that Go accepts, and see the compiler refuse a file with a single mistake in it.

At work, Go is what a great deal of server and infrastructure software is written in, and the reason people give is exactly today's lesson: the compiler catches a whole class of mistakes before the program exists. Interviewers ask "what is the difference between `go run` and `go build`", and they ask "why does Go refuse to compile when an import is unused". Both are answered today.

## 2. The story

Meera's grandmother cooks the best dal in the family, and the recipe lives only in her head, in Marathi. Meera's flatmate Tom wants to make it. Tom speaks no Marathi.

On Saturday, Meera stands in the kitchen with her grandmother on a video call. Her grandmother says one step. Meera turns to Tom and says it in English. Tom does it. Her grandmother says the next step. Meera translates. Tom does it. It works, and the dal is good, but it takes an hour, and Meera cannot leave the kitchen. If her grandmother says a word Meera does not know, everything stops right there, at that step, with the onions half done.

On Sunday, Tom wants to cook it again. Meera is out. So the whole thing cannot happen. The recipe still exists, in her grandmother's head, but without Meera standing between them, Tom cannot use it.

Meera thinks about this on the bus. The recipe is fine. The problem is that every single time, someone has to stand there and translate, step by step, live.

There is another way, and her cousin does it. Her cousin sat with the grandmother once, for an afternoon, and translated the entire recipe into English in one go, start to finish. She saved it as a note on her phone. Now anyone who reads English can cook the dal, any time, with nobody translating. The cousin does not need to be there. The one cost is that the afternoon of translating happened first, before anyone could cook anything, and if the grandmother changes one step, the cousin has to sit down and redo the translation.

Two ways to get the same dal. Translate live, every time, step by step, and stop the moment you hit a word you do not know. Or translate once, all of it, up front, and then run it as many times as you like without the translator in the room.

Today's Go is the cousin on the sofa.

## 3. The idea in plain English

A **program** is a list of instructions saved in a **file**. You will save yours as `hello.go`. A **terminal** is a window where you type **commands**, one per line, and press Enter.

A **compiler** is a program that reads your whole file, checks all of it, and writes out a new file that the machine can run directly, with nothing standing in between. That new file is called a **binary** or an **executable**. The compiler is the cousin: one afternoon of work up front, then a note anyone can use.

Go's compiler is inside a single tool called `go`. You will use it two ways today.

`go build hello.go` is the cousin's afternoon. It reads `hello.go`, checks every line, and writes a file called `hello`. If anything at all is wrong, it writes nothing and tells you what and where. You then run `./hello` yourself.

`go run hello.go` does the same compile, but into a hidden temporary place, and then runs the result immediately. It is a convenience for while you are writing. It is still the cousin's afternoon; it just happens fast and out of sight.

Because the compiler checks the whole file first, Go has a rule you will meet today and hate a little: if you bring in a tool you do not use, the compiler refuses. Not a warning. A refusal. That strictness is the point of the language.

## 4. The picture

```
  you type              the compiler                       the machine
  ────────              ────────────                       ───────────
  go build hello.go ──► reads ALL of hello.go
                        checks every line
                        any mistake? ──► print it, write nothing, stop
                        no mistakes?  ──► write file "hello"

  ./hello ───────────────────────────────────────────────► runs "hello"
                                                           prints Hello, world
```

*Notice the two separate arrows. Compiling and running are two different moments. A mistake found in the first one means the second one never happens.*

## 5. The code, built step by step

Check that Go is installed.

```bash
go version
```

You want `go version go1.23` or higher. If you see `command not found`, install it from the official go.dev download page, close the terminal, open a new one, and try again.

Make a folder and move into it. If you made `day01` for Python, use the same one.

```bash
mkdir day01
cd day01
```

Now the program. Go will not accept a single line the way Python does. The smallest Go program is five lines, and each one is required. Save this as `hello.go`.

```go
package main
```

Every Go file starts by saying which **package** it belongs to. A package is a named group of files. The special name `main` means "this is a program you can run", as opposed to a library that other programs borrow from.

```go
import "fmt"
```

`import` brings in a package that someone else wrote. `fmt` is short for format, and it is the standard package for printing. Without this line, the word `fmt` means nothing.

```go
func main() {
	fmt.Println("Hello, world")
}
```

`func main()` declares the starting point. When the program runs, it begins here. Everything between the curly braces `{` and `}` is what `main` does. `fmt.Println` means "the `Println` tool from the `fmt` package", and `Println` prints its text followed by a new line. The indentation is one tab, and Go is fussy about that, so a tool called `gofmt` fixes it for you, which you will meet on day 14.

Run it.

```bash
go run hello.go
```

```
Hello, world
```

Now the other way. Build a binary, look at it, run it.

```bash
go build hello.go
ls
./hello
```

```
hello  hello.go
Hello, world
```

There is a new file called `hello` next to your source. That is the cousin's note. You could copy it to another computer with no Go installed and it would still run. On Windows it is called `hello.exe` and you run it as `hello.exe`.

Now break it on purpose. Misspell `Println`.

```go
func main() {
	fmt.Printn("Hello, world")
}
```

```bash
go run hello.go
```

```
# command-line-arguments
./hello.go:6:6: undefined: fmt.Printn
```

Nothing printed except the error. Not even a partial run. `./hello.go:6:6` is file, line 6, column 6. `undefined: fmt.Printn` means the `fmt` package has nothing by that name. Compare this with Python, where line 1 printed and line 2 failed. In Go, the program never existed.

Here is the run and the output for the complete program for today, fixed.

```bash
go run hello.go
```

```
Hello, world
This is line two
Go checked this whole file before running any of it
```

And the complete file that produces it. The line starting with `//` is a **comment**, a note for humans that the compiler skips.

```go
// hello.go — day 1, the first program
// Run:   go run hello.go
// Build: go build hello.go && ./hello
package main

import "fmt"

func main() {
	fmt.Println("Hello, world")
	fmt.Println("This is line two")
	fmt.Println("Go checked this whole file before running any of it")
}
```

## 6. How the other two languages do it

The same program in Python is one line, and there is no build step:

```python
print("Hello, world")
```

```bash
python3 hello.py
```

And in C++, where the two steps are visible as two commands:

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

The one line of difference that matters: **Go and C++ both compile, but Go's compiler refuses things C++ merely warns about.** Add `import "os"` to the Go program without using it and the build fails: `"os" imported and not used`. Add `#include <vector>` to the C++ program without using it and nothing happens at all. Python has no build step to refuse anything, so an unused import just sits there. Go took the position that a warning nobody reads is worth nothing, and made every warning a stop.

## 7. The traps

**The near-miss: the unused import.** This looks completely correct.

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("Hello, world")
}
```

```
# command-line-arguments
./hello.go:5:2: "os" imported and not used
```

You will hit this every day of your Go life: you delete the one line that used a package and forget to delete the import. The fix is to remove the import. Editors with Go support do it for you on save.

**The real error: a missing `package main`.** Delete the first line.

```
hello.go:1:1: expected 'package', found 'import'
```

Every Go file must begin with a package line. The compiler will not read further without it.

**The near-miss: the opening brace on its own line.** Coming from other languages, people write this:

```go
func main()
{
	fmt.Println("Hello, world")
}
```

```
./hello.go:5:6: missing function body
./hello.go:6:1: syntax error: unexpected semicolon or newline before {
```

Go inserts an invisible end-of-statement at the end of a line that looks finished. `func main()` alone looks finished, so the compiler ends the statement there and the `{` on the next line makes no sense. The opening brace goes on the same line, always. `gofmt` enforces it.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between `go run` and `go build`?"
- "Why does Go refuse to compile a file with an unused import?"
- "Is Go compiled or interpreted, and what does that change in practice?"

**What to say out loud, the first ninety seconds**

"Go is compiled. When I run `go build hello.go`, the compiler reads the whole file, checks every line, and if it is all correct it writes a binary, a file the operating system runs directly with no interpreter. If anything is wrong, it writes nothing and prints the file, line and column of each problem. `go run` does exactly the same compile but into a temporary location, then runs the result straight away, so it is for while I am writing and `go build` is for producing something to ship.

The practical difference from Python is when errors appear. In Python a misspelled name on line 50 is found when line 50 runs. In Go, a misspelled name means the program is never built. Go pushes that further than most languages: an unused import or an unused variable is a compile error, not a warning, because the designers decided that warnings get ignored."

**The follow-ups**

1. *"Where does `go run` put the binary?"* — In a temporary folder that the tool cleans up afterwards. You never see it. `go build` puts it in the current folder, named after the file or the module.
2. *"Can I run the binary on a machine without Go?"* — Yes. It is self-contained. That is one of the main reasons Go is chosen for command-line tools and services.
3. *"What does `package main` mean?"* — It marks the file as part of a runnable program rather than a library. A runnable program must have a `package main` with a `func main()` in it, and that function is where execution starts.

**A model answer**

"Go compiles ahead of time. `go build` reads all the source, type-checks it, and emits a self-contained binary; `go run` does the same compile into a temporary directory and executes it immediately, which is convenient while developing. Because the whole file is checked before anything runs, mistakes like an undefined name or an unused import stop the build with a file, line and column. Go treats many things other compilers warn about as hard errors, on the principle that an ignored warning is worse than no warning. The result is slower first feedback than Python but a much smaller class of mistakes that can reach production."

## 9. Recall card

- `go run hello.go` compiles to a temporary place and runs; `go build hello.go` writes a binary named `hello` that you run yourself.
- Every runnable Go file begins `package main`, imports what it needs, and has `func main()` where execution starts.
- The compiler checks the whole file before anything runs: an error means nothing prints, not even line 1.
- Unused import and unused variable are compile errors, not warnings.
- Opening brace on the same line as `func main()`, or the compiler ends the statement early.
