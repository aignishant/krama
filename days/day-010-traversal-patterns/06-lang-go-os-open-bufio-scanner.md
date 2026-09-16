---
day: 10
track: lang-go
title: "os.Open, bufio.Scanner, io.Reader and io.Writer"
theme: "Files and standard I/O"
phase: "Languages: every language, every basic"
status: written
---

# Day 010 · Go — os.Open, bufio.Scanner, io.Reader and io.Writer

**Today's theme:** Files and standard I/O

**After today you can:** You can read a file line by line, write one, and read from standard input in each language.

**The interviewer asks it as:** *How do you read a file that is bigger than memory?*

---

## 1. What this is, and why it matters

Go opens a file with `os.Open`, which returns the file and an error, and reads it a line at a time with a `bufio.Scanner`, which holds one buffered line in memory no matter how big the file is. Closing is done by `defer f.Close()`, a statement that schedules the close for the moment the surrounding function returns. Underneath all of it are two tiny ideas, `io.Reader` and `io.Writer`: anything you can pull bytes from, and anything you can push bytes into, so that a file, the keyboard, a network connection and a string all read the same way.

At work, `io.Reader` and `io.Writer` are the most important two names in Go's standard library, and half of what makes Go good at servers is that a request body, a file and a compressed stream are all just readers. Interviewers ask "how do you read a large file in Go", "what does `defer` do and when does it run", and "what is `io.Reader`", and all three are today.

## 2. The story

Lakshmi's colony gets water from a tanker every Tuesday morning, because the pipes have not worked properly for years. The tanker holds ten thousand litres. Her house has a tank on the roof that holds five hundred.

Nobody ever lifts the tanker. Nobody even tries to move ten thousand litres at once. The driver connects a hose, and water flows through it, a little at a time, for about twenty minutes, until the roof tank is full. Then he disconnects and moves to the next house. The hose is thin. The water that is in the hose at any one moment is a bucketful, maybe less. But over twenty minutes, a bucketful at a time, five hundred litres get up to the roof.

Before the tanker, when Lakshmi was small, they did it with actual buckets. A line of people from the well to the house, passing buckets hand to hand. Nobody in the line ever held more than one bucket. Nobody needed to know how much water was in the well, or how much the house needed. Each person had one job: take the full bucket from the left, pass it to the right, take the empty one back. You could fill a house or a whole street that way, one bucket at a time, and no single person ever carried more than they could hold.

Her grandfather used to say the well did not care who was at the other end of the line. Could be Lakshmi's house, could be the temple, could be a field. The line just moved buckets. And the house did not care where the water came from. Well, tanker, rain off the roof. Water arrived at the tap, and the tap did not ask.

There was one rule her grandfather was strict about. When you were done at the well, you put the cover back on. Not when you remembered. Not tomorrow. The moment the last bucket came up. An open well is how things fall in.

## 3. The idea in plain English

A **file** is a named block of bytes on disk. `os.Open("notes.txt")` connects to it and returns two things, in yesterday's shape: a `*os.File`, the hose, and an `error`, which is `nil` if the file opened. You check the error first, always.

**`defer f.Close()`** is how the cover goes back on the well. `defer` takes a call and postpones it until the surrounding function returns, by any route: a normal `return`, an early `return` on error, or a panic. You write it on the line right after the open succeeds, so that the close is guaranteed the moment you have something to close. That is Python's `with` and yesterday's `finally`, as a single word. Deferred calls run in reverse order of deferral, last in, first out.

Reading a line at a time is done by **`bufio.Scanner`**. `bufio.NewScanner(f)` wraps the file in a buffer; then `for scanner.Scan()` advances to the next line and returns `false` at the end, and `scanner.Text()` is the current line **without** its newline. The scanner holds one line at a time, so a file bigger than memory reads with a bucketful of memory. After the loop, `scanner.Err()` tells you whether it stopped because the file ended, `nil`, or because something went wrong. Check it.

The small-file shortcuts are `os.ReadFile(path)`, which returns the whole file as a `[]byte`, and `os.WriteFile(path, data, 0o644)`, which writes it. Lifting the tanker, fine for a config file. The `0o644` is the permission the new file gets; read it as "owner can read and write, everyone else can read".

Writing a stream: `os.Create(path)` opens for writing and empties the file. `f.WriteString("text\n")` writes; for many small writes, wrap in `bufio.NewWriter(f)`, write to that, and call `w.Flush()` at the end, or the buffered text never reaches the disk. `fmt.Fprintf(w, ...)` and `fmt.Fprintln(w, ...)` write formatted text to anything you can write to.

Which brings you to the two ideas. **`io.Reader`** is anything with a `Read` method that fills a byte slice: a file, `os.Stdin`, a network connection, a `strings.NewReader("text")`. **`io.Writer`** is anything with a `Write` method: a file, `os.Stdout`, `os.Stderr`, a `bytes.Buffer`. `bufio.NewScanner` takes an `io.Reader`, not a file, so the same loop reads a file or the keyboard. `fmt.Fprintln` takes an `io.Writer`, so the same call writes to a file or the screen. The house does not care where the water came from. Day 16 explains the mechanism, interfaces; today, use them.

**Standard input** is `os.Stdin`, an `io.Reader`. `bufio.NewScanner(os.Stdin)` reads the tap line by line, whether a person is typing or a file is piped in with `<` or `|`.

## 4. The picture

```
 io.Reader: anything you can pull bytes from      io.Writer: anything you can push bytes into

   *os.File  ──┐                                    ┌──► *os.File
   os.Stdin  ──┼──► bufio.NewScanner(r)             ├──► os.Stdout
   net.Conn  ──┤    for scanner.Scan() {            ├──► os.Stderr
   strings.  ──┘        scanner.Text()   one line   └──► bufio.Writer  (Flush at the end!)
   NewReader                            at a time

 func readNotes() error {
     f, err := os.Open("notes.txt")      open
     if err != nil { return err }        check
     defer f.Close()                     schedule the close for when readNotes returns
     ...                                 use f
 }                                       ← Close runs here, on every path out
```

*Notice that the scanner and the print do not know or care whether a file or the terminal is behind them. Notice where the deferred `Close` actually runs: at the closing brace, not where it was written.*

## 5. The code, built step by step

Start `water.go` in a `day10` folder. Writing first, so there is a file to read.

```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func writeNotes(path string) error {
	f, err := os.Create(path)
	if err != nil {
		return err
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	fmt.Fprintln(w, "Tuesday: tanker came at 7")
	fmt.Fprintln(w, "Wednesday: no water")
	fmt.Fprintln(w, "Thursday: pipe repaired")
	return w.Flush()
}
```

`os.Create` opens for writing, emptying the file if it exists. `defer f.Close()` immediately after the check. `fmt.Fprintln(w, ...)` prints to the writer `w` instead of the screen. `w.Flush()` pushes the buffer to the file, and returning its error is the honest thing to do.

Reading a line at a time.

```go
func countTankers(path string) (int, error) {
	f, err := os.Open(path)
	if err != nil {
		return 0, err
	}
	defer f.Close()

	count := 0
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		if strings.Contains(scanner.Text(), "tanker") {
			count++
		}
	}
	return count, scanner.Err()
}
```

The loop holds one line at a time. `scanner.Err()` is returned as the function's error, so a read failure halfway through is not silently mistaken for the end of the file. Add `"strings"` to the imports.

The same loop, reading the tap.

```go
func countLines(r io.Reader) (int, error) {
	total := 0
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		total++
	}
	return total, scanner.Err()
}
```

`countLines` takes an `io.Reader`. Call it as `countLines(os.Stdin)` and it reads the keyboard or a pipe; call it as `countLines(f)` with an open file and it reads the file; call it as `countLines(strings.NewReader("a\nb\n"))` and it reads a string. One function, every source. Add `"io"` to the imports.

Putting it together in `main`.

```go
func main() {
	if err := writeNotes("notes.txt"); err != nil {
		fmt.Fprintln(os.Stderr, "write:", err)
		os.Exit(1)
	}

	data, err := os.ReadFile("notes.txt")
	if err != nil {
		fmt.Fprintln(os.Stderr, "read:", err)
		os.Exit(1)
	}
	fmt.Print(string(data))
```

```
Tuesday: tanker came at 7
Wednesday: no water
Thursday: pipe repaired
```

`os.ReadFile` is the whole tanker, fine for three lines. Errors go to `os.Stderr`, the second output stream, so they do not mix with real output when someone pipes your program into another. `os.Exit(1)` ends the program with a non-zero code, which tells the terminal it failed.

```go
	count, err := countTankers("notes.txt")
	if err != nil {
		fmt.Fprintln(os.Stderr, "count:", err)
		os.Exit(1)
	}
	fmt.Println("days with a tanker:", count)

	_, err = os.Open("missing.txt")
	fmt.Println("missing file:", err)
}
```

```
days with a tanker: 1
missing file: open missing.txt: no such file or directory
```

The error from `os.Open` already says which file and what went wrong. Wrapping it with the function's name, as yesterday, would make it `count: open missing.txt: no such file or directory`.

Standard input, from the terminal. Save this as `count_lines.go` in its own folder.

```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	total := 0
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		total++
	}
	fmt.Println(total, "lines")
}
```

```bash
go run count_lines.go < notes.txt
```

```
3 lines
```

Nothing was opened. The tap was read. Without `<`, it waits for typing until Ctrl+D on Linux and Mac or Ctrl+Z then Enter on Windows.

Here is the run and output for the complete program.

```bash
go run water.go
```

```
Tuesday: tanker came at 7
Wednesday: no water
Thursday: pipe repaired
days with a tanker: 1
lines in a string reader: 2
missing file: open missing.txt: no such file or directory
```

And the complete file.

```go
// water.go — day 10, files, defer, Scanner, Reader and Writer
// Run:  go run water.go
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

// writeNotes creates the file, writes through a buffer, and flushes.
func writeNotes(path string) error {
	f, err := os.Create(path)
	if err != nil {
		return err
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	fmt.Fprintln(w, "Tuesday: tanker came at 7")
	fmt.Fprintln(w, "Wednesday: no water")
	fmt.Fprintln(w, "Thursday: pipe repaired")
	return w.Flush()
}

// countTankers reads one line at a time; the file can be any size.
func countTankers(path string) (int, error) {
	f, err := os.Open(path)
	if err != nil {
		return 0, err
	}
	defer f.Close()

	count := 0
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		if strings.Contains(scanner.Text(), "tanker") {
			count++
		}
	}
	return count, scanner.Err()
}

// countLines reads any io.Reader: a file, os.Stdin, or a string.
func countLines(r io.Reader) (int, error) {
	total := 0
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		total++
	}
	return total, scanner.Err()
}

func main() {
	if err := writeNotes("notes.txt"); err != nil {
		fmt.Fprintln(os.Stderr, "write:", err)
		os.Exit(1)
	}

	data, err := os.ReadFile("notes.txt")
	if err != nil {
		fmt.Fprintln(os.Stderr, "read:", err)
		os.Exit(1)
	}
	fmt.Print(string(data))

	count, err := countTankers("notes.txt")
	if err != nil {
		fmt.Fprintln(os.Stderr, "count:", err)
		os.Exit(1)
	}
	fmt.Println("days with a tanker:", count)

	n, err := countLines(strings.NewReader("first\nsecond\n"))
	if err != nil {
		fmt.Fprintln(os.Stderr, "lines:", err)
		os.Exit(1)
	}
	fmt.Println("lines in a string reader:", n)

	_, err = os.Open("missing.txt")
	fmt.Println("missing file:", err)
}
```

## 6. How the other two languages do it

Python, where `with` does the closing and the file object is its own reader:

```python
with open("notes.txt", encoding="utf-8") as f:
    for line in f:                      # line keeps its "\n"
        if "tanker" in line:
            count += 1

for line in sys.stdin:                  # same loop, the tap
    total += 1
```

C++, where the stream closes itself in its destructor and `getline` strips the newline:

```cpp
std::ifstream in("notes.txt");
if (!in) {
    std::cerr << "could not open notes.txt\n";
    return 1;
}
std::string line;
while (std::getline(in, line)) {
    if (line.find("tanker") != std::string::npos) ++count;
}
```

The one line of difference that matters: **Go makes you write the close, Python makes you write the block, and C++ writes neither.** `defer f.Close()` is one line you can forget; `with` is a block you cannot leave; the C++ `ifstream` closes when it goes out of scope, which is RAII and day 13. The second difference is that Go's failure to open is a returned error you must check before `defer`, Python's is an exception that stops you reaching the loop, and C++'s is a silent flag on the stream that you test with `if (!in)`, and forgetting that test means a loop that runs zero times with no message.

## 7. The traps

**The near-miss: the missing `Flush`.** Write through a buffer and forget to flush.

```go
	f, _ := os.Create("log.txt")
	defer f.Close()
	w := bufio.NewWriter(f)
	fmt.Fprintln(w, "started")
```

`log.txt` is empty. The text is sitting in `w`'s buffer, and `f.Close()` closes the file underneath it without asking the buffer. `w.Flush()` before the function returns, and check its error. `defer w.Flush()` works too, but then its error is lost, so prefer the explicit call.

**The near-miss: `defer` inside a loop.** Open many files in one function.

```go
	for _, path := range paths {
		f, err := os.Open(path)
		if err != nil {
			return err
		}
		defer f.Close()
		// read f
	}
```

Every `defer` waits for the **function** to return, not the loop iteration. With ten thousand paths, ten thousand files are open at once, and the operating system refuses at some point with `too many open files`. Move the body into its own function, so each call's `defer` runs when that call returns.

**The real error: ignoring `scanner.Err()`.** A line longer than the scanner's buffer.

```go
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fmt.Println(len(scanner.Text()))
	}
	fmt.Println("done")
```

```
done
```

The loop ended early and said nothing, because a line was longer than 64 KB and `Scan` returned `false`. Add the check and you see why:

```go
	if err := scanner.Err(); err != nil {
		fmt.Println("scan:", err)
	}
```

```
scan: bufio.Scanner: token too long
```

For files with very long lines, raise the limit with `scanner.Buffer(make([]byte, 1024*1024), 1024*1024)` before scanning, or use `bufio.NewReader(f).ReadString('\n')`. Either way, `scanner.Err()` after every loop, always.

## 8. Say it out loud

**How it gets asked**

- "How do you read a file that is bigger than memory in Go?"
- "What does `defer` do, and when does the deferred call run?"
- "What are `io.Reader` and `io.Writer`, and why does everything use them?"

**What to say out loud, the first ninety seconds**

"I open with `os.Open`, check the error, and immediately `defer f.Close()` so the file is closed when the function returns on any path. Then I wrap the file in a `bufio.Scanner` and loop `for scanner.Scan()`, reading `scanner.Text()` one line at a time; the scanner keeps a single buffered line, so memory is bounded by line length, not file size. After the loop I check `scanner.Err()`, because `Scan` returns false both at end of file and on error, including a line longer than the default 64 KB buffer. For small files, `os.ReadFile` returns the whole thing as a byte slice.

`defer` schedules a call for function exit, last deferred first run, which makes cleanup live next to acquisition. The trap is `defer` in a loop, which holds every resource until the function ends, so I extract the loop body into a function.

`io.Reader` and `io.Writer` are one-method interfaces: `Read(p []byte)` and `Write(p []byte)`. Files, `os.Stdin`, `os.Stdout`, network connections, `strings.NewReader` and `bytes.Buffer` all satisfy them, so a function that takes an `io.Reader` works on any source. That is why `bufio.NewScanner` accepts a reader and the same loop reads a file or standard input."

**The follow-ups**

1. *"Why check the error from `Close` on a file you wrote?"* — Because buffered data may only reach the disk at close, and a full disk or a network filesystem can fail there. For files you only read, ignoring `Close`'s error is acceptable; for files you wrote, check it or at least log it.
2. *"What is the difference between `bufio.Scanner` and `bufio.Reader`?"* — `Scanner` splits input into tokens, lines by default, with a fixed maximum size; `Reader` gives you `ReadString`, `ReadLine` and `ReadBytes` with no size limit and more control. Scanner for ordinary text, Reader for very long lines or byte-level work.
3. *"How do you copy a file?"* — `io.Copy(dst, src)`, which streams from any reader to any writer in chunks and never holds the whole file. It is the same idea as the scanner loop, generalised.

**A model answer**

"Go streams files: `os.Open` returns `(*os.File, error)`; after checking the error, `defer f.Close()` guarantees closure at function exit. `bufio.NewScanner(f)` with `for scanner.Scan()` yields lines without their newline, holding one buffered line, so arbitrarily large files read in constant memory; `scanner.Err()` must be checked after the loop because a too-long token or read failure also ends it. Small files use `os.ReadFile` and `os.WriteFile`. Writes go through `os.Create` and optionally `bufio.NewWriter`, which requires `Flush`. Everything is built on `io.Reader` and `io.Writer`, single-method interfaces satisfied by files, standard streams, network connections and in-memory buffers, so code written against them is source-agnostic; `os.Stdin` is a reader and `os.Stderr` a writer. `defer` in a loop leaks descriptors until the function returns, so loop bodies that open resources become separate functions."

## 9. Recall card

- `f, err := os.Open(path)`; check `err`; then `defer f.Close()` on the next line; it runs when the function returns, on every path.
- `scanner := bufio.NewScanner(f)`; `for scanner.Scan() { scanner.Text() }`; one line at a time, no newline attached; then `if err := scanner.Err(); err != nil`.
- `os.ReadFile` and `os.WriteFile` for small files; `os.Create` plus `bufio.NewWriter` plus `w.Flush()` for streams, or the file stays empty.
- `io.Reader` is anything with `Read`, `io.Writer` anything with `Write`: files, `os.Stdin`, `os.Stdout`, `strings.NewReader`; write functions against them.
- `defer` in a loop holds every file until the function ends; a long line stops the scanner with `token too long`, which only `Err()` reveals.
